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
