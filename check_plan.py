"""Check an Instagram workflow plan and print a Markdown review."""

import argparse
import csv
from collections import Counter
from html import escape
from pathlib import Path


FIELDS = ("account", "workflow", "device", "profile", "owner", "status")
STATUSES = ("ready", "review", "paused")
MARKDOWN_CHARS = str.maketrans({char: f"&#{ord(char)};" for char in "\\|`*_[]~!"})


def read_plan(path):
    rows = []
    errors = []
    workflows = {}
    account_slots = {}
    slot_accounts = {}

    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, strict=True)
        headers = reader.fieldnames or []
        if len(headers) != len(FIELDS) or set(headers) != set(FIELDS):
            return [], [f"Use these six column names: {', '.join(FIELDS)}."]

        for raw in reader:
            line = reader.line_num
            if None in raw:
                errors.append(f"Line {line}: too many fields. Quote values containing commas.")
                continue

            row = {field: (raw[field] or "").strip() for field in FIELDS}
            missing = [field for field in FIELDS if not row[field]]
            if missing:
                errors.append(f"Line {line}: fill in {', '.join(missing)}.")
                continue

            row["status"] = row["status"].casefold()
            if row["status"] not in STATUSES:
                errors.append(f"Line {line}: status must be ready, review, or paused.")
                continue

            account = row["account"].casefold()
            workflow = (account, row["workflow"].casefold())
            slot = (row["device"].casefold(), row["profile"].casefold())

            first_workflow_line = workflows.setdefault(workflow, line)
            if first_workflow_line != line:
                errors.append(f"Line {line}: this account and workflow repeat line {first_workflow_line}.")

            first_slot, slot_line = account_slots.setdefault(account, (slot, line))
            if first_slot != slot:
                errors.append(f"Line {line}: this account has a different device/profile on line {slot_line}.")

            first_account, account_line = slot_accounts.setdefault(slot, (account, line))
            if first_account != account:
                errors.append(f"Line {line}: another account uses this device/profile on line {account_line}.")

            rows.append(row)

    if not rows and not errors:
        errors.append("Add at least one workflow row below the header.")
    return rows, errors


def render_review(rows):
    counts = Counter(row["status"] for row in rows)
    summary = " · ".join(f"{counts[status]} {status}" for status in STATUSES)
    lines = [
        "# Instagram workflow review",
        "",
        f"{len(rows)} workflow row(s) · {summary}",
        "",
        "| Account | Workflow | Android device | Device profile | Owner | Status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        values = [row[field] for field in FIELDS[:-1]] + [row["status"].capitalize()]
        cells = [escape(" ".join(value.split())).translate(MARKDOWN_CHARS) for value in values]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="CSV file to check")
    parser.add_argument("--output", type=Path, help="save the review to a new Markdown file")
    args = parser.parse_args()

    try:
        rows, errors = read_plan(args.plan)
    except (OSError, UnicodeError, csv.Error) as error:
        parser.error(f"Could not read the plan: {error}")

    if errors:
        parser.exit(2, "Fix the following rows before sharing the plan:\n- " + "\n- ".join(errors) + "\n")

    review = render_review(rows)
    if args.output is None:
        print(review, end="")
        return

    try:
        with args.output.open("x", encoding="utf-8", newline="\n") as file:
            file.write(review)
    except OSError as error:
        parser.error(f"Could not save the review: {error}")


if __name__ == "__main__":
    main()
