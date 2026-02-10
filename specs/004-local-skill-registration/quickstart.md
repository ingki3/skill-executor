# Quickstart: Local Skill Registration

This feature allows you to register skills stored directly on the server filesystem, restricted to the application root boundary.

## 1. Search a Local Path
1. In the Dashboard under "Register Skills", enter a path relative to the application root (e.g., `./.skills` or an absolute container path).
2. Click "Search Local".
3. The UI will list all immediate subdirectories and indicate if they have valid skill metadata.

## 2. Initiate Scan
1. Select the folders you want to register.
2. Click "Scan Selected".
3. The skills will appear in the "Registration Queue" for security review.

## 3. Handle Duplicates
If you are registering a skill that already exists, the system will prompt you for confirmation. Click "Confirm Update" to proceed or "Cancel" to skip.

## 4. Review and Approve
1. Review the security findings and code preview for the local skills.
2. Click "Approve" to move them into the active registry.