# Data Model: View Skill Popup

## Entities

### SkillDocumentation (UI State)
This feature does not change the backend data structure but introduces new UI states to manage the popup.

- `isPopupOpen`: Boolean (Controls visibility of the MUI Dialog)
- `content`: String (Markdown content fetched from existing `/skills/{id}/documentation` endpoint)
- `status`: Enum (IDLE, LOADING, ERROR, SUCCESS)

## Relationships
- **SkillCard** triggers the **SkillDocumentationDialog**.
- **SkillDocumentationDialog** consumes data from the existing **RegistryService** documentation endpoint.
