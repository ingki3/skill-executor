# Quickstart: GitHub Direct Skill Folder Input

This feature allows you to register skills directly by pasting a specific GitHub folder link.

## 1. Get a Skill Folder Link
Navigate to a skill directory on GitHub (e.g., `https://github.com/ComposioHQ/awesome-claude-skills/tree/main/freshdesk-automation`) and copy the URL from your browser's address bar.

## 2. Paste into Registration
1. Open the Skill Executor Dashboard.
2. Ensure the search mode is set to **GitHub**.
3. Paste the deep link into the "GitHub Repo URL" field.

## 3. Direct Registration
1. If the system detects a deep link, it will automatically skip the "Search Repo" step.
2. Click **Scan Selected** (or just **Register** depending on UI state).
3. The skill will be added directly to the "Registration Queue" for security review.

## 4. Automatic Processing
The system will automatically clone the correct branch and target the specific subdirectory, making registration faster and more precise.