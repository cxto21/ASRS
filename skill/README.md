# ASRS Skill

Agent Software Requirements Specification - A specification language for describing software systems.

## Overview

ASRS is a specification language designed for humans and AI agents. It provides a minimal, precise way to document software systems with 7 core entities:

- **Project** - Root of specification
- **Principal** - External entities (users, systems)
- **Feature** - System capabilities
- **Scenario** - Observable behavior (Given/When/Then)
- **Component** - Implementation units
- **Resource** - Persistent data
- **Test** - Executable verification

## Quick Start

### Validate a document

```bash
python3 scripts/asrs-validator.py document.asrs
```

### See example documents

Check the `assets/examples/` directory:
- `login.asrs` - Simple authentication system
- `books.asrs` - Book library with multiple user roles
- `url-shortener.asrs` - URL shortening service

## Features

- **RFC 2119 compliance** - Uses precise requirement keywords
- **Agent-native** - Designed for AI agent consumption
- **Minimal vocabulary** - Only 7 entity types
- **Validation** - Comprehensive format and reference checking
- **Examples** - Ready-to-use example documents

## Documentation

- [ASRS Specification](references/ASRS.md) - Complete language spec
- [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) - Key words for requirements
- [Semantic Versioning](https://semver.org/) - Version numbering

## Validation Rules

### Errors (must fix)
- Exactly one Project entity
- Unique IDs across all entities
- Required properties present
- Valid references to existing entities

### Warnings (recommended to fix)
- Scenarios without Principals
- Components without Verify
- Orphan Components not used by any Scenario

## Compliance Levels

| Level | Name | Entities Required |
|-------|------|-------------------|
| 1 | Functional | Project, Principal, Feature, Scenario |
| 2 | Architecture | + Component, Resource |
| 3 | Executable | + Test, Verify |
