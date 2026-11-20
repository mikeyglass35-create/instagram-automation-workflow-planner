# Instagram Automation Workflow Planner

Plan Instagram automation for multiple accounts on Android. Give every workflow an account alias, device, profile, owner, and review status before anyone starts it.

This free planning kit from [SMTasker](https://smtasker.com/) includes a spreadsheet-ready CSV and a local Python checker. It flags account and device assignments that disagree, then produces a Markdown handoff you can share with your team. The checker runs offline and works with aliases. It needs no Instagram or SMTasker login.

## Try the example

1. Download this repository using **Code → Download ZIP**, then extract it.
2. Open a terminal in the extracted folder. Use Python 3.10 or later. No packages are required.
3. Run the checker with the [sample plan](example-plan.csv). The example uses fictional accounts and device labels.

```sh
python check_plan.py example-plan.csv
```

| Account | Workflow | Android device | Device profile | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| studio-a | Weekly publishing review | phone-01 | studio-a | Content lead | Ready |
| studio-b | Reel approval | phone-01 | studio-b | Account manager | Review |
| studio-c | Campaign handoff | phone-02 | default | Operations lead | Paused |

In this example, the account manager still needs to review `studio-b`'s Reel. The two workflows on `phone-01` are assigned to distinct profiles.

## Plan your own workflow

1. Copy [plan-template.csv](plan-template.csv) to `my-plan.csv`. Keep the six headers and add one row per workflow.
2. Use stable labels such as `studio-a` and `phone-01`. Use `default` if the device has one relevant profile.
3. Set `review` for work that needs a decision, `ready` once your team has reviewed the plan, or `paused` for work on hold.
4. Run `python check_plan.py my-plan.csv`. To save the handoff as a new file, run `python check_plan.py my-plan.csv --output review.md`.

The checker flags missing fields, repeated account and workflow pairs, an account assigned to multiple device profiles, and a device profile assigned to two account aliases. A successful check means the CSV passes these rules. Your team decides what to start.

## From the plan to SMTasker

SMTasker runs supported Instagram automations on connected Android devices. The product's Workflows setup lets you choose accounts and actions, review the configuration, and save a draft before starting. Use your CSV as a handoff while you configure the workflow in SMTasker. The Python checker reads the CSV and writes the report locally.

- [Manage multiple Instagram accounts for clients](https://smtasker.com/how-to-manage-and-automate-multiple-instagram-accounts-for-clients/)
- [Create and review a workflow in SMTasker](https://smtasker.com/knowledge-base/getting-started-with-workflows/)
