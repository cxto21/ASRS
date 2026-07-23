# 14. Validation Rules

A valid ASRS document MUST satisfy:

- Exactly one Project
- Unique IDs
- Valid references (IDs must exist)
- Valid Entity declarations
- Valid indentation
- Required Properties present

Validators SHOULD warn when detecting:

- Orphan Components
- Features without Scenarios
- Scenarios without Components
- Scenarios without Principals
- Components without Verify
- Verify without Tests
