---
name: asrs
description: Generate, validate, and work with ASRS (Agent Software Requirements Specification) documents. Use when creating software specifications, validating ASRS format, generating tests from specs, or when the user mentions ASRS, software requirements, or agent-native specifications.
license: MIT
compatibility: Requires Python 3.8+ for validator script
metadata:
  author: asrs-project
  version: "1.0.0"
  specification: "ASRS 1.0.0-draft"
allowed-tools: Bash(python:*) Read Write Glob Grep
---

# ASRS Skill

Agent Software Requirements Specification - A specification language for describing software systems, designed for humans and AI agents.

## Quick Start

### Validate an ASRS document

```bash
python scripts/asrs-validator.py path/to/document.asrs
```

### Generate ASRS from requirements

Use this skill when the user provides software requirements in natural language. Follow the workflow below to generate a valid ASRS document.

## ASRS Core Entities (7)

| Entity | Purpose | Required Properties |
|--------|---------|---------------------|
| Project | Root of specification | Name, Specification, Document Version |
| Principal | External entity interacting with system | Type |
| Feature | System capability | (none, but SHOULD have Description) |
| Scenario | Observable behavior | Given, When, Then |
| Component | Implementation unit | Type |
| Resource | Persistent data | Type |
| Test | Executable verification | Validates, Given, When, Then |

## Generation Workflow

When generating ASRS from natural language requirements:

1. **Extract Principals** - Identify all user types, external systems, and actors
2. **Define Features** - Map requirements to system capabilities
3. **Write Scenarios** - Describe behavior using Given/When/Then for each Feature
4. **Design Components** - Identify implementation units and their responsibilities
5. **Define Resources** - Map data requirements to persistent storage
6. **Create Tests** - Write verification scenarios that validate behavior

## RFC 2119 Keywords

All ASRS documents use RFC 2119 keywords precisely:

- **MUST** / **MUST NOT** - Absolute requirements
- **SHOULD** / **SHOULD NOT** - Recommended, with valid exceptions
- **MAY** / **OPTIONAL** - Truly optional behavior

## Canonical Style

- Entity Types: PascalCase (`Component`, `Scenario`)
- Properties: PascalCase (`Description`, `Responsibilities`)
- IDs: Uppercase with prefix (`COMP-AUTH`, `SCN-LOGIN`)
- One blank line between Entities
- Properties at 1 indentation, Values at 2 indentations

## Validation Rules

A valid ASRS document MUST satisfy:

- Exactly one Project
- Unique IDs across all entities
- Valid references (referenced IDs must exist)
- Required Properties present for each entity type
- Valid indentation (4 spaces per level)

Validators SHOULD warn:

- Features without Scenarios
- Scenarios without Principals
- Components without Verify
- Verify without Tests

## Compliance Levels

| Level | Name | Required Entities |
|-------|------|-------------------|
| 1 | Functional | Project, Principal, Feature, Scenario |
| 2 | Architecture | + Component, Resource |
| 3 | Executable | + Test, Verify |

## Example Structure

```asrs
Project PROJECT-EXAMPLE

    Name

        Example App

    Specification

        ASRS 1.0.0

    Document Version

        1.0.0


Principal USER

    Type

        Human

    Can

        Use features


Feature FEAT-EXAMPLE

    Description

        Example capability


Scenario SCN-EXAMPLE

    Principal

        USER

    Given

        Initial state

    When

        Action performed

    Then

        Expected result


Component COMP-EXAMPLE

    Type

        Service

    Verify

        MUST meet requirements


Resource RES-EXAMPLE

    Type

        Table


Test TEST-EXAMPLE

    Validates

        SCN-EXAMPLE

    Given

        Initial state

    When

        Action performed

    Then

        Expected result
```

## Scripts

### asrs-validator.py

Validates ASRS documents for correct format and references.

```bash
python3 scripts/asrs-validator.py document.asrs
python3 scripts/asrs-validator.py document.asrs --json
python3 scripts/asrs-validator.py document.asrs --strict
```

Options:
- `--json` - Output results as JSON
- `--strict` - Treat warnings as errors
- `--fix` - Attempt to fix common issues

## References

- [ASRS Specification](references/ASRS.md) - Complete language specification
- [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) - Key words for requirements
- [Semantic Versioning](https://semver.org/) - Version numbering

## Edge Cases

### Circular References
ASRS does not allow circular references between entities. The validator will detect and report these.

### Missing Principals
Scenarios SHOULD have a Principal. If missing, the validator warns but does not fail.

### Duplicate IDs
All IDs MUST be unique across the entire document. The validator will fail on duplicates.

### Indentation Errors
ASRS uses strict indentation. Properties at 1 level, Values at 2 levels. The validator checks this.
