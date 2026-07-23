# ASRS Project

> Agent Software Requirements Specification - A specification language for describing software systems.

## Scope

- This repository contains the ASRS specification, tools, and examples.
- The specification defines a minimal language with 7 core entities.
- Tools validate and convert ASRS documents.

## Commands

### Validate ASRS documents

```bash
python3 tools/asrs-validator.py document.yaml
python3 tools/asrs-validator.py document.yaml --json
python3 tools/asrs-validator.py document.yaml --strict
python3 tools/asrs-validator.py document.yaml --summary
```

### Convert between formats

```bash
python3 tools/asrs-convert.py document.yaml --to asrs
python3 tools/asrs-convert.py document.asrs --to yaml
```

## Conventions

- Entity Types: PascalCase (`Component`, `Scenario`)
- Properties: PascalCase (`Description`, `Responsibilities`)
- IDs: Uppercase with prefix (`COMP-AUTH`, `SCN-LOGIN`)
- One blank line between Entities
- Properties at 1 indentation (4 spaces), Values at 2 indentations (8 spaces)

## File Structure

- `spec/` - Specification files (read-only reference)
- `tools/` - Validation and conversion scripts
- `examples/` - Example ASRS documents in YAML format
- `docs/` - Additional documentation

## Don't Touch

- `spec/` files are the canonical specification; edit only through formal process
- `spec/meta.yaml` is the ASRS meta-spec (describes itself in YAML format)
- `llms.txt` is the agent navigation index; update when adding new files
- `AGENTS.md` is this file; keep it under 150 lines

## Versioning

- `examples/.asrs.log` tracks all modifications
- Format: VERSION_ID | TIMESTAMP | ACTION | TARGET | BLOCK_ID | AUTHOR | DESCRIPTION
- Newest entries at top (head of file)

## Further Reading

- `spec/ASRS.md` - Complete specification
- `spec/meta.yaml` - ASRS meta-specification
- `docs/srs-comparison.md` - Comparison with traditional SRS
- `docs/agent-guidelines.md` - Guidelines for AI agents
