# Quickstart: Skill Risk Review

This feature allows you to safely register multiple skills by reviewing potential security risks before they are added to the active registry.

## 1. Initiate Bulk Scan
1. Navigate to the "Register Skills" section in the dashboard.
2. Enter a repository URL and click "Search Repo".
3. Select the skills you want to register and click "Scan Selected".

## 2. Monitor the Queue
1. A new "Registration Queue" will appear at the top of your dashboard.
2. Each skill will show a status: `SCANNING`, `SAFE`, or `RISKY`.

## 3. Review Findings
1. For any skill (especially those marked `RISKY`), click "Review Details".
2. A side-panel will open showing the source code and specific risk findings (e.g., PII detection, dangerous system operations).

## 4. Make a Judgment
1. **Individual**: Click "Approve" or "Reject" on each skill in the queue.
2. **Bulk**: Click "Approve All Safe" to quickly register all skills that passed the automated scan without flags.

## 5. Verify Registration
Once approved, the skills will move from the "Registration Queue" to the "Skill Management" list and are ready for execution.