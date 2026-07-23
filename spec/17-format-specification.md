# 17. Format Specification

ASRS is format-agnostic. The language can be expressed in any structured format.

## Supported Formats

| Format | Extension | Status |
|--------|-----------|--------|
| YAML | `.yaml` | Primary |
| JSON | `.json` | Planned |
| TOML | `.toml` | Planned |

## YAML Format

### Structure

```yaml
project:
  id: PROJECT-XXX
  name: ...
  specification: ASRS 1.0.0
  document_version: 1.0.0

principals:
- id: PRINCIPAL-XXX
  type: Human|External System|Service|Agent|Scheduler|Device
  description: ...
  can:
  - Capability 1

features:
- id: FEAT-XXX
  description: ...
  requirements:
  - REQ-XXX

scenarios:
- id: SCN-XXX
  principal: PRINCIPAL-XXX
  uses:
  - COMP-XXX
  given:
  - Initial state
  when:
  - Action
  then:
  - Expected result

components:
- id: COMP-XXX
  type: Service|Frontend|Backend|Library|Worker|Agent|Gateway|External
  technology: ...
  responsibilities:
  - Responsibility 1
  uses:
  - COMP-XXX
  creates:
  - RES-XXX
  reads:
  - RES-XXX
  writes:
  - RES-XXX
  publishes:
  - EVT-XXX
  consumes:
  - EVT-XXX
  verify:
  - MUST/SHOULD/MAY ...

resources:
- id: RES-XXX
  type: Table|Bucket|Cache|Queue|Secret
  schema:
  - 'field: type'

tests:
- id: TEST-XXX
  validates:
  - SCN-XXX
  - COMP-XXX
  given:
  - Initial state
  when:
  - Action
  then:
  - Expected result
```

### Mapping Rules

| ASRS Concept | YAML Key | Type |
|--------------|----------|------|
| Entity ID | `id` | string |
| Entity Type | Top-level key | array of objects |
| Property | Object key | string, array, or object |
| List | Array | array of strings |
| Reference | String value | ID reference |

### Block Identification

Each entity maps to a YAML block:

```yaml
# BLOCK-PROJECT-XXX
project:
  id: PROJECT-XXX
  ...

# BLOCK-PRINCIPAL-XXX
principals:
- id: PRINCIPAL-XXX
  ...

# BLOCK-FEATURE-XXX
features:
- id: FEAT-XXX
  ...

# BLOCK-SCENARIO-XXX
scenarios:
- id: SCN-XXX
  ...

# BLOCK-COMPONENT-XXX
components:
- id: COMP-XXX
  ...

# BLOCK-RESOURCE-XXX
resources:
- id: RES-XXX
  ...

# BLOCK-TEST-XXX
tests:
- id: TEST-XXX
  ...
```

## JSON Format (Planned)

### Structure

```json
{
  "project": {
    "id": "PROJECT-XXX",
    "name": "...",
    "specification": "ASRS 1.0.0",
    "document_version": "1.0.0"
  },
  "principals": [
    {
      "id": "PRINCIPAL-XXX",
      "type": "Human",
      "can": ["Capability 1"]
    }
  ],
  "features": [...],
  "scenarios": [...],
  "components": [...],
  "resources": [...],
  "tests": [...]
}
```

## TOML Format (Planned)

### Structure

```toml
[project]
id = "PROJECT-XXX"
name = "..."
specification = "ASRS 1.0.0"
document_version = "1.0.0"

[[principals]]
id = "PRINCIPAL-XXX"
type = "Human"
can = ["Capability 1"]

[[features]]
id = "FEAT-XXX"
description = "..."

[[scenarios]]
id = "SCN-XXX"
principal = "PRINCIPAL-XXX"
given = ["Initial state"]
when = ["Action"]
then = ["Expected result"]

[[components]]
id = "COMP-XXX"
type = "Service"
verify = ["MUST ..."]

[[resources]]
id = "RES-XXX"
type = "Table"
schema = ["field: type"]

[[tests]]
id = "TEST-XXX"
validates = ["SCN-XXX"]
given = ["Initial state"]
when = ["Action"]
then = ["Expected result"]
```

## Conversion Between Formats

ASRS documents can be converted between formats:

```bash
# YAML to JSON
python3 tools/asrs-convert.py document.yaml --to json

# YAML to TOML
python3 tools/asrs-convert.py document.yaml --to toml

# JSON to YAML
python3 tools/asrs-convert.py document.json --to yaml
```

## Format Selection

Choose format based on use case:

| Use Case | Recommended Format |
|----------|-------------------|
| Human editing | YAML |
| API exchange | JSON |
| Configuration | TOML |
| Agent processing | YAML or JSON |
