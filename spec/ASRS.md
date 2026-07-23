# ASRS
## Agent Software Requirements Specification

**Version:** 1.0.0-draft

---

# 1. Purpose

ASRS is a specification language for describing software systems.

It is designed equally for:

- Humans
- AI agents
- Code generators
- Test generators

ASRS prioritizes **clarity**, **precision**, and **simplicity**.

---

# 2. Normative Language

The keywords

- MUST
- MUST NOT
- REQUIRED
- SHALL
- SHALL NOT
- SHOULD
- SHOULD NOT
- RECOMMENDED
- MAY
- OPTIONAL

MUST be interpreted as defined by RFC 2119.

Reference: https://www.ietf.org/rfc/rfc2119.txt

---

# 3. Design Principles

## Agent Native

The document MUST be directly consumable by software agents.

Information SHOULD NOT require inference whenever it can be expressed explicitly.

---

## Minimal Vocabulary

ASRS defines only **7 core entities**.

Nothing else is required.

---

## Behavior First

Behavior MUST describe observable system behavior.

Implementation details belong to Components.

---

## Verification First

Every important entity SHOULD define how its correctness is verified.

Verification is part of the specification.

Tests implement Verification.

---

## Token Efficiency

Every token SHOULD provide semantic value.

Avoid unnecessary prose, repeated information, and decorative syntax.

---

# 4. Versioning

ASRS follows Semantic Versioning 2.0.

Reference: https://semver.org/

Format: `MAJOR.MINOR.PATCH`

- MAJOR: Breaking language changes
- MINOR: Backward-compatible additions
- PATCH: Editorial corrections

Every ASRS document SHOULD declare:

```
Specification: ASRS 1.0.0
Document Version: 1.0.0
```

---

# 5. Standards References

ASRS aligns with the following standards:

| Standard | Purpose | Reference |
|----------|---------|-----------|
| RFC 2119 | Key words for requirements | https://www.ietf.org/rfc/rfc2119.txt |
| SemVer 2.0 | Version numbering | https://semver.org/ |
| ISO/IEC/IEEE 29148 | Requirements engineering | https://www.iso.org/standard/72368.html |
| Gherkin | Behavior-driven syntax | https://cucumber.io/docs/gherkin/ |

---

# 6. Core Entities

ASRS defines exactly 7 entities.

| Entity | Purpose |
|--------|---------|
| Project | Root of the specification |
| Principal | External entity interacting with the system |
| Feature | System capability |
| Scenario | Observable behavior |
| Component | Implementation unit |
| Resource | Persistent data |
| Test | Executable verification |

---

# 7. Grammar

ASRS defines only three syntactic constructs.

- **Entity**: `<EntityType> <EntityID>`
- **Property**: `Property Name` followed by indented value
- **List**: Indented items under a property

---

## Entity

```
<EntityType> <EntityID>

    Property

        Value
```

Example:

```
Component COMP-AUTH

    Type

        Service
```

---

## Property

```
Property

    Value
```

Example:

```
Technology

    Supabase Auth
```

---

## List

```
Property

    Item 1

    Item 2

    Item 3
```

Example:

```
Responsibilities

    Authentication

    OAuth

    Sessions
```

---

# 8. Canonical Style

## Separation

One blank line separates Entities.

## Indentation

Properties begin at one indentation level.

Values begin at two indentation levels.

## References

References always contain IDs, never names.

Correct:
```
Uses

    COMP-AUTH
```

Incorrect:
```
Uses

    Authentication Service
```

## Capitalization

- Entity Types: PascalCase (`Component`, `Scenario`)
- Properties: PascalCase (`Description`, `Responsibilities`)
- IDs: Uppercase with prefix (`COMP-AUTH`, `SCN-LOGIN`)

## Comments

Comments begin with `#`.

Parsers SHOULD ignore comments.

---

# 9. Identity

Every Entity MUST define an ID.

IDs MUST be unique.

IDs SHOULD NOT be reused.

Format: `PREFIX-NAME`

Examples:
- `COMP-AUTH`
- `SCN-LOGIN`
- `RES-USERS`
- `TEST-LOGIN`
- `PRINCIPAL-USER`

---

# 10. Entity Specification

---

## 10.1 Project

Represents the root of the specification.

Exactly one Project MUST exist.

### Required Properties

- Name
- Specification
- Document Version

### Optional Properties

- Description
- Owner
- Compliance Level

### Example

```
Project PROJECT-LASSET

    Name

        Lasset

    Specification

        ASRS 1.0.0

    Document Version

        1.0.0

    Compliance Level

        Level 2
```

---

## 10.2 Principal

Represents an external entity that interacts with the system.

Principals answer "who initiates behavior?" 

Principals SHOULD be defined before Scenarios that reference them.

### Required Properties

- Type

### Optional Properties

- Description
- Can (capabilities this Principal may perform)

### Type Values

- Human
- External System
- Service
- Agent
- Scheduler
- Device

### Example

```
Principal USER

    Type

        Human

    Description

        Registered user of the application

    Can

        Read books

        Search books


Principal EDITOR

    Type

        Human

    Description

        Can manage book catalog

    Can

        Add books

        Edit books

        Delete books


Principal STRIPE

    Type

        External System

    Description

        Payment processing provider

    Can

        Process payments

        Refund payments
```

---

## 10.3 Feature

Represents a system capability.

A Feature groups one or more Scenarios.

### Required Properties

- None (but SHOULD have Description)

### Optional Properties

- Description
- Requirements (references external requirements)

### Example

```
Feature FEAT-LOGIN

    Description

        User authentication

    Requirements

        REQ-AUTH-001
```

---

## 10.4 Scenario

Represents observable behavior.

Scenarios describe:
- Initial state (Given)
- Action (When)
- Expected result (Then)

Scenarios SHOULD NOT describe implementation.

### Required Properties

- Given
- When
- Then

### Optional Properties

- Principal (who initiates the behavior)
- Uses (references Components)

### Example

```
Scenario SCN-LOGIN

    Principal

        USER

    Uses

        COMP-WEB

        COMP-AUTH

    Given

        Existing user

    When

        Submit credentials

    Then

        Session created


Scenario SCN-ADD-BOOK

    Principal

        EDITOR

    Uses

        COMP-WEB

        COMP-BOOKS

    Given

        Editor logged in

    When

        Add new book

    Then

        Book created
```

---

## 10.5 Component

Represents an implementation unit.

### Required Properties

- Type

### Optional Properties

- Technology
- Responsibilities
- Uses (references other Components)
- Creates / Reads / Writes (references Resources)
- Publishes / Consumes (references events)
- Verify (verification rules)

### Type Values

- Service
- Frontend
- Backend
- Library
- Worker
- Agent
- Gateway
- External

### Example

```
Component COMP-AUTH

    Type

        Service

    Technology

        Supabase Auth

    Responsibilities

        Authentication

        OAuth

        Sessions

    Creates

        RES-SESSIONS

    Verify

        MUST authenticate users

        MUST reject invalid credentials

        SHOULD respond < 500ms
```

---

## 10.6 Resource

Represents persistent or shared data.

### Required Properties

- Type

### Optional Properties

- Schema

### Type Values

- Table
- Bucket
- Cache
- Queue
- Secret

### Example

```
Resource RES-USERS

    Type

        Table

    Schema

        id: uuid

        email: string

        created_at: timestamp
```

---

## 10.7 Test

Represents executable verification.

Tests validate one or more Entities.

### Required Properties

- Validates (references Entities to verify)
- Given
- When
- Then

### Example

```
Test TEST-LOGIN

    Validates

        SCN-LOGIN

        COMP-AUTH

    Given

        Existing user

    When

        Valid credentials

    Then

        Session created
```

---

# 11. References

References create relationships between entities.

ASRS uses properties to express references.

Standard reference properties:

| Property | Meaning |
|----------|---------|
| Uses | Depends on |
| Creates | Produces |
| Reads | Consumes from |
| Writes | Modifies |
| Publishes | Emits event |
| Consumes | Listens to event |
| Validates | Verifies correctness |
| Principal | Initiates behavior |

Example:

```
Component COMP-WEB

    Uses

        COMP-AUTH

    Reads

        RES-USERS

    Publishes

        EVT-LOGIN
```

---

# 12. Verification

Verification defines correctness.

Verification SHOULD contain measurable statements.

Example:

```
Verify

    MUST authenticate users

    MUST reject invalid credentials

    SHOULD respond < 500ms

    MUST NOT create duplicated sessions
```

Verification SHOULD avoid implementation details.

---

# 13. Traceability

The recommended traceability chain:

```
Principal → Feature → Scenario → Component → Resource → Test
```

---

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

---

# 15. Compliance Levels

## Level 1: Functional Specification

Required Entities:
- Project
- Principal
- Feature
- Scenario

## Level 2: Architecture Specification

Adds:
- Component
- Resource

## Level 3: Executable Specification

Adds:
- Test
- Verify

Projects SHOULD declare their Compliance Level.

---

# 16. Complete Example

```
Project PROJECT-BOOKS

    Name

        Book Library

    Specification

        ASRS 1.0.0

    Document Version

        1.0.0

    Compliance Level

        Level 3


Principal USER

    Type

        Human

    Can

        Read books

        Search books


Principal EDITOR

    Type

        Human

    Can

        Add books

        Edit books

        Delete books


Feature FEAT-BOOKS

    Description

        Book management


Scenario SCN-READ-BOOK

    Principal

        USER

    Uses

        COMP-WEB

        COMP-BOOKS

    Given

        User logged in

    When

        Select book

    Then

        Book displayed


Scenario SCN-ADD-BOOK

    Principal

        EDITOR

    Uses

        COMP-WEB

        COMP-BOOKS

    Given

        Editor logged in

    When

        Add new book

    Then

        Book created


Component COMP-WEB

    Type

        Frontend

    Technology

        React

    Uses

        COMP-BOOKS

    Verify

        MUST support Chrome-based browsers


Component COMP-BOOKS

    Type

        Service

    Technology

        Node.js

    Creates

        RES-BOOKS

    Verify

        MUST store books

        MUST validate book data


Resource RES-BOOKS

    Type

        Table

    Schema

        id: uuid

        title: string

        author: string

        created_at: timestamp


Test TEST-READ-BOOK

    Validates

        SCN-READ-BOOK

        COMP-BOOKS

    Given

        User logged in

        Book exists

    When

        Select book

    Then

        Book displayed


Test TEST-ADD-BOOK

    Validates

        SCN-ADD-BOOK

        COMP-BOOKS

    Given

        Editor logged in

    When

        Add new book

    Then

        Book created
```

---

# End of Specification

**Agent Software Requirements Specification**

**ASRS v1.0.0-draft**
