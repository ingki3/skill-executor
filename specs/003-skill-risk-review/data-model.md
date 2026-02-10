# Data Model: Skill Risk Review

## Entities

### RegistrationBatch
- `id`: UUID (Stable Batch Identifier)
- `repo_url`: String
- `status`: Enum (`SCANNING`, `REVIEW_REQUIRED`, `COMPLETED`)
- `items`: List of `RegistrationQueueItem`
- `created_at`: ISO DateTime

### RegistrationQueueItem
- `path`: String (Relative path in repo)
- `name`: String
- `safety_status`: Enum (`SCANNING`, `SAFE`, `RISKY`, `FAILED`)
- `judgment`: Enum (`PENDING`, `APPROVED`, `REJECTED`)
- `risk_findings`: List of `RiskFinding`
- `code_content`: String (Source code for review)

### RiskFinding
- `category`: Enum (`PII`, `MALICIOUS_CODE`, `DANGEROUS_OP`, `OTHER`)
- `detail`: String
- `severity`: Enum (`HIGH`, `MEDIUM`, `LOW`)

## Relationships
- `RegistrationBatch` 1:N `RegistrationQueueItem`
- `RegistrationQueueItem` 1:N `RiskFinding`

## Validation Rules
- All `RegistrationQueueItem` must have `judgment != PENDING` before a batch can be marked `COMPLETED`.
- A skill is only added to the `SkillRegistry` if its individual `judgment` is `APPROVED`.