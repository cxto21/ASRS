# Agent Guidelines for ASRS

## Overview

This document provides guidelines for AI agents working with ASRS (Agent Software Requirements Specification) documents.

## Reading ASRS

### Start with llms.txt

Always begin by reading `llms.txt` to understand the project structure and available resources.

### Progressive Disclosure

1. Read `llms.txt` for navigation
2. Read specific sections as needed
3. Don't read everything at once

### Entity Recognition

ASRS uses 7 core entities:

| Entity | Prefix | Example |
|--------|--------|---------|
| Project | PROJECT- | PROJECT-LOGIN |
| Principal | PRINCIPAL- | PRINCIPAL-USER |
| Feature | FEAT- | FEAT-AUTH |
| Scenario | SCN- | SCN-LOGIN |
| Component | COMP- | COMP-AUTH |
| Resource | RES- | RES-USERS |
| Test | TEST- | TEST-LOGIN |

## Generating ASRS

### From Natural Language

When generating ASRS from requirements:

1. **Extract Principals** - Identify all user types and external systems
2. **Define Features** - Map requirements to capabilities
3. **Write Scenarios** - Describe behavior with Given/When/Then
4. **Design Components** - Identify implementation units
5. **Define Resources** - Map data to persistent storage
6. **Create Tests** - Write verification scenarios

### From Code

When generating ASRS from existing code:

1. **Analyze entry points** - Find APIs, CLI commands, user interactions
2. **Identify components** - Map modules to Components
3. **Trace data flow** - Identify Resources and their relationships
4. **Document behavior** - Create Scenarios from usage patterns

## Validating ASRS

### Use the Validator

```bash
python3 tools/asrs-validator.py document.asrs
python3 tools/asrs-validator.py document.asrs --json
python3 tools/asrs-validator.py document.asrs --strict
```

### Common Issues

1. **Missing Project** - Exactly one Project MUST exist
2. **Duplicate IDs** - All IDs MUST be unique
3. **Invalid references** - Referenced IDs MUST exist
4. **Missing required properties** - Check entity requirements

## Best Practices

### For Humans

- Keep documents concise
- Use meaningful IDs
- Define Principals before Scenarios
- Include verification in Components

### For Agents

- Parse incrementally
- Validate before processing
- Use references for relationships
- Preserve formatting

## Working with Tools

### Validator

The validator checks:
- Document structure
- Entity validity
- Reference integrity
- Required properties

### Converter

Convert between formats:
```bash
python3 tools/asrs-convert.py document.asrs --to yaml
python3 tools/asrs-convert.py document.yaml --to asrs
```

## Integration Points

### With Code Generation

ASRS can drive code generation:
1. Parse Components → Generate module structure
2. Parse Resources → Generate database schema
3. Parse Scenarios → Generate API endpoints
4. Parse Tests → Generate test files

### With Test Generation

ASRS can drive test generation:
1. Parse Test entities → Generate test cases
2. Parse Given/When/Then → Generate test steps
3. Parse Validates → Generate assertions

## Troubleshooting

### Ambiguous Requirements

If requirements are vague:
1. Ask for clarification
2. Make reasonable assumptions
3. Document assumptions in ASRS
4. Mark as TBD if uncertain

### Complex Systems

For large systems:
1. Break into modules
2. Use separate ASRS files per module
3. Reference between files
4. Maintain a master index
