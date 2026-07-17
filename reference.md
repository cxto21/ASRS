# ASRS Specification
## Agent Software Requirements Specification

**Version:** 2.0.0-draft

---

# 1. Purpose

ASRS (Agent Software Requirements Specification) is a graph-oriented specification language for describing software systems.

Its primary goal is to become the **single source of truth** for software projects by describing:

- business requirements
- software behavior
- architecture
- components
- interfaces
- resources
- events
- verification
- tests
- decisions

inside a single document.

ASRS is designed equally for:

- humans
- AI agents
- documentation generators
- code generators
- architecture analyzers
- test generators
- project management tools

ASRS intentionally prioritizes **clarity**, **determinism**, and **token efficiency**.

---

# 2. Design Principles

Every ASRS document MUST follow these principles.

## Human Readable

A software engineer SHOULD be able to understand an ASRS document without specialized tooling.

---

## Agent Native

The document MUST be directly consumable by software agents.

Information SHOULD NOT require inference whenever it can be expressed explicitly.

---

## Graph First

Every entity is a graph node.

Every reference is a graph edge.

The architecture emerges naturally from the graph.

---

## Single Source of Truth

Every concept SHOULD exist exactly once.

Objects SHOULD reference other objects instead of duplicating information.

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

Avoid:

- unnecessary prose
- repeated information
- decorative syntax
- duplicated metadata

---

# 3. Normative Language

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

Reference

https://www.ietf.org/rfc/rfc2119.txt

---

# 4. Versioning

The ASRS specification follows Semantic Versioning 2.0.

Reference

https://semver.org/

Format

```
MAJOR.MINOR.PATCH
```

Rules

MAJOR

Breaking language changes.

MINOR

Backward-compatible additions.

PATCH

Editorial corrections.

Every ASRS document SHOULD declare:

```
Specification

Document Version
```

Example

```
Specification

    ASRS 2.0.0

Document Version

    1.4.0
```

---

# 5. Core Model

Everything inside ASRS belongs to one of four concepts.

```
Entity

Behavior

Reference

Verification
```

Nothing else exists.

---

## Entity

Represents something.

Examples

```
Project

Feature

Component

Resource

Interface

Event

Test
```

Entities become graph nodes.

---

## Behavior

Represents observable software behavior.

Behavior is expressed using Scenarios.

Behavior intentionally ignores implementation details.

---

## Reference

References connect entities.

References create the software graph.

Every reference MUST point to an Entity ID.

---

## Verification

Verification defines correctness.

Verification belongs directly to the Entity being verified.

---

# 6. Grammar

ASRS defines only three syntactic constructs.

```
Entity

Property

List
```

Everything else derives from these.

---

## Entity

```
<EntityType> <EntityID>

    Property

        Value

    Property

        Value
```

Example

```
Component COMP-AUTH

    Name

        Authentication Service

    Type

        Service
```

---

## Property

Properties describe an Entity.

Syntax

```
Property

    Value
```

Example

```
Technology

    Supabase Auth
```

---

## List

Lists are indentation-based.

Example

```
Responsibilities

    Authentication

    OAuth

    Sessions
```

Lists preserve order.

Unless explicitly defined, order has no semantic meaning.

---

# 7. Canonical Style

All ASRS documents SHOULD follow the same formatting rules.

## One Entity

One blank line separates Entities.

---

## One Property



Properties begin at one indentation level.

---

## Values

Values begin at two indentation levels.

---

## References

References always contain IDs.

Never names.

Correct

```
Uses

    COMP-AUTH
```

Incorrect

```
Uses

    Authentication Service
```

---

## Capitalization

Entity Types

PascalCase

```
Component

Scenario

Feature
```

Properties

PascalCase

```
Description

Responsibilities

Verification
```

IDs

Uppercase

```
COMP-AUTH

SCN-LOGIN

RES-USERS
```

---

## Comments

Comments begin with

```
#
```

Parsers SHOULD ignore comments.

---

# 8. Universal Properties

Every Entity MAY contain

```
Name

Description

Version

Status

Owner

Tags

Verify
```

Meaning

Name

Human-readable title.

Description

Short explanation.

Version

Entity version.

Status

Draft

Active

Deprecated

Owner

Responsible person or team.

Tags

Free-form labels.

Verify

Verification rules.

---

# 9. Identity

Every Entity MUST define an ID.

IDs MUST be unique.

IDs MUST remain stable.

IDs SHOULD NOT be reused.

Recommended format

```
PREFIX-NAME
```

Examples

```
COMP-AUTH

COMP-WEB

SCN-LOGIN

FEAT-AUDIT

RES-USERS

EVT-SESSION-CREATED

TEST-LOGIN
```

---

# 10. References

References define relationships.

ASRS no longer defines a dedicated Relationship object.

Relationships emerge from properties.

Example

```
Component COMP-WEB

    Uses

        COMP-AUTH

        COMP-DB
```

The parser automatically creates

```
COMP-WEB

uses

COMP-AUTH
```

and

```
COMP-WEB

uses

COMP-DB
```

No additional syntax is required.

---

# 11. Standard Reference Properties

The following properties create graph edges.

```
Uses

Depends

Reads

Writes

Creates

Updates

Deletes

Publishes

Consumes

Calls

Implements

Owns

Contains

Validates
```

Projects MAY introduce additional reference properties.

Unknown reference properties SHOULD generate warnings.

---

# 12. Universal Verification

Every Entity MAY define

```
Verify
```

Verification is no longer a standalone object.

Example

```
Component COMP-AUTH

    Verify

        MUST authenticate users

        MUST reject invalid passwords

        SHOULD respond < 500ms
```

This rule applies equally to

- Components
- Features
- Scenarios
- Interfaces
- Resources
- Events
- Tests

Verification is inherited by the Entity.

---

# 13. Parsing Rules

A conforming parser MUST

- recognize Entities
- recognize Properties
- recognize Lists
- recognize References
- validate IDs
- validate references
- preserve ordering
- preserve comments (optional)

A parser MUST reject

- duplicate IDs
- malformed indentation
- invalid Entity declarations
- invalid references

---

# 14. Philosophy

ASRS intentionally minimizes language complexity.

A parser only needs to understand:

```
Entity

↓

Properties

↓

Values

↓

References
```

Everything else is semantics.

This allows an implementation to remain simple while preserving rich software knowledge.

---

# 15. Design Objective

An ASRS document SHOULD answer four questions.

```
What exists?

(Entity)

What happens?

(Scenario)

How are things connected?

(References)

How do we know it is correct?

(Verify)
```

Everything else is derived.

---

# 16. Preview

A complete software specification can now be expressed as:

```
Project PROJECT-LASSET

Component COMP-WEB

Component COMP-AUTH

Component COMP-DB

Feature FEAT-LOGIN

Scenario SCN-LOGIN

Test TEST-LOGIN
```

Each Entity contributes new knowledge.

The architecture emerges automatically from references.

No UML.

No C4.

No separate dependency graphs.

Everything exists in one graph.

---

**End of Part 1**

**Next:** Part 2 defines every Entity (`Project`, `Requirement`, `Feature`, `Scenario`, `Component`, `Interface`, `Resource`, `Event`, `Decision`, `Test`), their required and optional properties, validation rules, compliance levels, and a complete example project.

# 17. Entity Specification

This section defines every Entity supported by ASRS.

An Entity represents a uniquely identifiable concept within the software system.

Unless explicitly stated otherwise:

- Every Entity MUST have an ID.
- Every Entity MAY use Universal Properties.
- Every Entity MAY define Verify.
- Every Entity MAY reference other Entities.

---

# 18. Project

Represents the root of the specification.

Exactly one Project MUST exist.

## Required Properties

```
Name

Specification

Document Version
```

## Optional Properties

```
Description

Owner

Tags
```

## Example

```
Project PROJECT-LASSET

    Name

        Lasset

    Specification

        ASRS 2.0.0

    Document Version

        1.0.0
```

---

# 19. Requirement

Represents a business, technical or regulatory requirement.

Requirements SHOULD be implementation independent.

## Additional Properties

```
Priority

Source
```

Priority values

```
Critical

High

Medium

Low
```

Requirements SHOULD be referenced by Features.

---

# 20. Feature

Represents a user capability.

A Feature groups one or more Scenarios.

## Additional Properties

```
Goal

Requirements
```

Requirements references Requirement IDs.

Example

```
Feature FEAT-LOGIN

    Goal

        Authenticate users

    Requirements

        REQ-AUTH
```

---

# 21. Scenario

Represents observable software behavior.

Scenarios describe:

- initial state
- action
- expected result

Scenarios SHOULD NOT describe implementation.

## Additional Properties

```
Uses

Given

When

Then
```

Uses references Components.

Example

```
Scenario SCN-LOGIN

    Uses

        COMP-WEB

        COMP-AUTH

    Given

        Existing user

    When

        Login

    Then

        Session created
```

---

# 22. Component

Represents an implementation unit.

Examples

- Frontend
- Backend
- Service
- Database
- Queue
- Worker
- Agent

## Required Properties

```
Type
```

## Optional Properties

```
Technology

Responsibilities

Interfaces
```

Responsibilities SHOULD be implementation responsibilities.

Behavior belongs to Scenarios.

Example

```
Component COMP-AUTH

    Type

        Service

    Technology

        Supabase Auth

    Responsibilities

        Authentication

        OAuth

        Session management
```

---

# 23. Interface

Represents a public interaction point.

Examples

- REST endpoint
- GraphQL query
- Event consumer
- CLI command

## Required Properties

```
Protocol
```

## Optional Properties

```
Endpoint

Input

Output
```

Example

```
Interface API-LOGIN

    Protocol

        HTTP

    Endpoint

        POST /login
```

---

# 24. Resource

Represents persistent or shared data.

Examples

- Database table
- Storage bucket
- Cache
- Queue
- Secret
- Dataset

## Required Properties

```
Type
```

## Optional Properties

```
Schema

Owner
```

Example

```
Resource RES-USERS

    Type

        Table
```

---

# 25. Event

Represents a domain event.

Events SHOULD describe business facts.

Events SHOULD NOT describe implementation mechanisms.

Example

```
Event EVT-USER-CREATED

    Description

        User account created
```

---

# 26. Decision

Represents an architectural decision.

Equivalent to an ADR.

## Additional Properties

```
Reason

Alternatives

Consequences
```

Example

```
Decision ADR-AUTH

    Reason

        Integrated OAuth

    Alternatives

        Auth0

        Clerk
```

---

# 27. Test

Represents executable verification.

Tests validate one or more Entities.

## Required Properties

```
Validates

Given

When

Then
```

Example

```
Test TEST-LOGIN

    Validates

        SCN-LOGIN

        COMP-AUTH

    Given

        Existing user

    When

        Login

    Then

        Session created
```

---

# 28. References

Relationships are expressed through Properties.

Example

```
Uses

Depends

Calls

Reads

Writes

Creates

Updates

Deletes

Publishes

Consumes

Owns

Contains

Validates
```

Example

```
Component COMP-WEB

    Uses

        COMP-AUTH

        COMP-DB

    Reads

        RES-USERS

    Publishes




        EVT-LOGIN
```

This produces the graph automatically.

No explicit Relationship object exists.

---

# 29. Verification

Verification is a Universal Property.

Verification defines correctness.

Verification SHOULD contain measurable statements.

Example

```
Verify

    MUST authenticate users

    MUST reject invalid credentials

    SHOULD respond <500ms

    MUST NOT create duplicated sessions
```

Verification SHOULD avoid implementation details.

---

# 30. Traceability

The recommended traceability chain is

```
Requirement

↓

Feature

↓

Scenario

↓

Component

↓

Interface

↓

Resource

↓

Event

↓

Test
```

Verification belongs directly to each Entity.

Objects SHOULD reference one another whenever possible.

---

# 31. Validation Rules

A valid ASRS document MUST satisfy:

✓ Exactly one Project.

✓ Unique IDs.

✓ Valid references.

✓ Valid Entity declarations.

✓ Valid indentation.

✓ Required Properties.

✓ RFC2119 semantics.

✓ Semantic Versioning.

---

Validators SHOULD warn when detecting

- orphan Components
- orphan Resources
- orphan Interfaces
- orphan Events
- Features without Scenarios
- Scenarios without Components
- Components without Verify
- Verify without Tests
- unused Decisions
- unreachable graph nodes

---

# 32. Compliance Levels

## Level 1

Functional Specification

Required Entities

```
Project

Requirement

Feature

Scenario
```

---

## Level 2

Architecture Specification

Adds

```
Component

Interface

Resource

Event
```

---

## Level 3

Executable Specification

Adds

```
Decision

Test

Verify
```

Projects SHOULD declare their Compliance Level.

---

# 33. Canonical Ordering

The recommended Entity order is

```
Project

Requirement

Decision

Feature

Scenario

Component

Interface

Resource

Event

Test
```

Parsers MUST NOT require this order.

---

# 34. Canonical Style

Recommended maximum Entity size

≈ 30 lines.

Recommended Description length

≤ 5 lines.

Properties SHOULD remain concise.

References SHOULD replace duplicated descriptions.

Prefer

```
Uses

    COMP-AUTH
```

instead of

```
Uses

    Authentication Service
```

---

# 35. Complete Example

```
Project PROJECT-LASSET

    Name

        Lasset

    Specification

        ASRS 2.0.0

    Document Version

        1.0.0


Requirement REQ-AUTH

    Description

        Users must authenticate before accessing private resources.


Decision ADR-AUTH

    Reason

        Integrated OAuth support.


Feature FEAT-LOGIN

    Goal

        Authenticate users.

    Requirements

        REQ-AUTH


Scenario SCN-LOGIN

    Uses

        COMP-WEB

        COMP-AUTH

    Given

        Existing user

    When

        User submits credentials

    Then

        Session created


Component COMP-WEB

    Type

        Frontend

    Uses

        COMP-AUTH


Component COMP-AUTH

    Type

        Service

    Technology

        Supabase Auth

    Creates

        RES-SESSIONS

    Publishes

        EVT-SESSION-CREATED

    Verify

        MUST authenticate users

        MUST reject invalid credentials

        SHOULD respond <500ms


Interface API-LOGIN

    Protocol

        HTTP

    Endpoint

        POST /login


Resource RES-SESSIONS

    Type

        Table


Event EVT-SESSION-CREATED

    Description

        Session successfully created.


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

# 36. Design Intent

ASRS intentionally models software as a connected graph.

Each Entity contributes knowledge.

Each Reference connects knowledge.

Each Verify statement defines correctness.

Each Test provides evidence.

From a single ASRS document, tools SHOULD be capable of generating:

- Requirements documentation
- Architecture diagrams
- Dependency graphs
- Component maps
- Sequence diagrams
- Test plans
- Coverage reports
- Impact analysis
- AI implementation plans

ASRS is designed so that software is specified once and consumed many times.

---

# 37. Future Evolution




Future versions MAY introduce additional Entities.

Examples

```
Workflow

Policy

DataModel

Deployment

Agent

Module

Package
```

Future versions MUST preserve backward compatibility unless the MAJOR version changes.

New Entity types SHOULD integrate into the existing Entity → Property → Reference → Verify model.

---

# End of Specification

**Agent Software Requirements Specification**

**ASRS v2.0.0-draft**
Una propuesta final para ASRS 2.1
Después de ver la especificación completa, hay una simplificación que creo que la haría aún más potente: eliminar las entidades Feature y Requirement como tipos especiales y convertirlas en especializaciones de una única entidad Capability.
Con ello tendrías un metamodelo extremadamente pequeño:
Project
Capability
Scenario
Component
Interface
Resource
Event
Decision
Test
Es decir, solo 9 entidades. Todo lo demás serían propiedades y referencias. Eso reduciría aún más la complejidad del lenguaje, facilitaría la implementación de parsers y haría que ASRS tuviera una identidad muy marcada frente a SRS, UML y Gherkin: un lenguaje declarativo, orientado a grafos, con muy pocos conceptos fundamentales y una gran capacidad de expresar sistemas completos. Creo que esa dirección sería una evolución natural para una futura ASRS 2.1.
Podrías darme ejemplos de micro app para el lengaje ASRS 2.0
Sí. De hecho, creo que una de las formas de validar si ASRS está bien diseñado es ver si puede describir micro aplicaciones completas con muy poco texto.
Aquí tienes varios ejemplos ordenados por complejidad.
1. Login (Hola Mundo de ASRS)
Project PROJECT-LOGIN

    Name

        Simple Login


Requirement REQ-AUTH

    Description

        Users must authenticate.


Feature FEAT-LOGIN

    Requirements

        REQ-AUTH


Scenario SCN-LOGIN

    Uses

        COMP-WEB

        COMP-AUTH

    Given

        Existing user

    When

        Login

    Then

        Session created


Component COMP-WEB

    Type

        Frontend

    Uses

        COMP-AUTH


Component COMP-AUTH

    Type

        Service

    Creates

        RES-SESSIONS

    Verify

        MUST authenticate users


Resource RES-SESSIONS

    Type

        Table


Test TEST-LOGIN

    Validates

        SCN-LOGIN

        COMP-AUTH

    Given

        Existing user

    When

        Login

    Then

        Session created
2. Todo App
Project PROJECT-TODO

Feature FEAT-TASKS

Scenario SCN-CREATE-TASK

    Uses

        COMP-WEB

        COMP-TASKS

    Given

        Authenticated user

    When

        Create task

    Then

        Task stored

Component COMP-TASKS

    Type

        Service

    Creates

        RES-TASKS

    Verify

        MUST create tasks

        MUST assign owner


Resource RES-TASKS

    Type

        Table
3. URL Shortener
Project PROJECT-SHORTENER

Feature FEAT-SHORTEN

Scenario SCN-SHORTEN

    Uses

        COMP-API

        COMP-STORAGE

    Given

        URL

    When

        Generate short URL

    Then

        Short URL returned


Component COMP-API

    Type

        Service

    Creates

        RES-LINKS


Resource RES-LINKS

    Type

        Table


Scenario SCN-REDIRECT

    Uses

        COMP-API

    Given

        Short URL

    When

        Visit URL

    Then

        Redirect
4. Chat
Project PROJECT-CHAT

Feature FEAT-MESSAGES

Scenario SCN-SEND

    Uses

        COMP-CHAT

        COMP-WS

    Given

        Connected users

    When

        Send message

    Then

        Message received


Component COMP-CHAT

    Type

        Service

    Publishes

        EVT-MESSAGE


Component COMP-WS

    Type

        Gateway

    Consumes

        EVT-MESSAGE


Event EVT-MESSAGE
5. File Upload
Project PROJECT-UPLOAD

Scenario SCN-UPLOAD

    Uses

        COMP-WEB

        COMP-STORAGE

    Given

        Selected file

    When

        Upload

    Then

        File available


Component COMP-STORAGE

    Type

        Storage

    Creates

        RES-FILES

    Verify

        MUST preserve file integrity


Resource RES-FILES

    Type

        Bucket
6. Weather App

Project PROJECT-WEATHER

Scenario SCN-GET-WEATHER

    Uses

        COMP-API

        COMP-WEATHER

    Given

        City

    When

        Search weather

    Then

        Forecast returned


Component COMP-WEATHER

    Type

        External

    Verify

        MUST return forecast
7. Expense Tracker
Project PROJECT-EXPENSES

Scenario SCN-ADD-EXPENSE

    Uses

        COMP-WEB

        COMP-EXPENSES

    Given

        Logged user

    When

        Register expense

    Then

        Expense stored


Component COMP-EXPENSES

    Type

        Service

    Creates

        RES-EXPENSES


Resource RES-EXPENSES

    Type

        Table
8. AI Chat
Project PROJECT-AICHAT

Scenario SCN-CHAT

    Uses

        COMP-WEB

        COMP-LLM

    Given

        User prompt

    When

        Submit

    Then

        AI response


Component COMP-LLM

    Type

        Agent

    Calls

        API-OPENAI

    Verify

        MUST answer prompts


Interface API-OPENAI

    Protocol

        HTTP
9. QR Generator
Project PROJECT-QR

Scenario SCN-GENERATE

    Uses

        COMP-QR

    Given

        Text

    When

        Generate QR

    Then

        PNG returned


Component COMP-QR

    Type

        Service

    Verify

        MUST generate PNG
10. Password Generator
Project PROJECT-PASSWORD

Scenario SCN-GENERATE

    Uses

        COMP-GENERATOR

    Given

        Length

    When

        Generate password

    Then

        Password returned


Component COMP-GENERATOR

    Type

        Library

    Verify

        MUST generate random passwords
11. Markdown Preview
Project PROJECT-MARKDOWN

Scenario SCN-PREVIEW

    Uses

        COMP-PARSER

    Given

        Markdown

    When

        Render

    Then

        HTML


Component COMP-PARSER

    Type

        Library

    Verify

        MUST support CommonMark
12. Image Resizer
Project PROJECT-IMAGE

Scenario SCN-RESIZE

    Uses

        COMP-IMAGE

    Given

        Uploaded image

    When

        Resize

    Then

        New image


Component COMP-IMAGE

    Type

        Worker

    Verify

        MUST preserve aspect ratio
Lo interesante
Al escribir varios ejemplos, aparece un patrón muy claro:
Project

↓

Features

↓

Scenarios

↓

Components

↓

Resources / Interfaces / Events

↓

Tests
Es decir, el 80 % de las aplicaciones CRUD comparten la misma estructura. Eso me lleva a una idea que creo que puede ser el siguiente gran paso para ASRS.
En lugar de escribir todas las entidades manualmente, ASRS podría incorporar plantillas reutilizables (Template o Blueprint). Por ejemplo:
Template CRUD

    Entity

        Task

    Storage

        PostgreSQL

    Auth

        Required
Un agente expandiría automáticamente esa plantilla en todos los Feature, Scenario, Component, Resource y Test necesarios. Esto convertiría ASRS no solo en un lenguaje de especificación, sino también en un lenguaje de composición, donde pequeños bloques reutilizables permiten describir sistemas completos con muy pocos tokens. Creo que esa sería una evolución muy potente para una futura ASRS 3.0.
me llama la atención que en ningun momento describiste usuarios
Muy buena observación. De hecho, mientras escribía la especificación también me hizo ruido, y creo que encontraste una carencia importante del modelo.
La pregunta es: ¿qué es un usuario dentro de ASRS?
Creo que la respuesta es: no es un Component.
Lo que modela ASRS hoy
Hoy tenemos:
Project

Feature

Scenario

Component

Interface

Resource

Event

Test
Todos son cosas del sistema.
Pero falta modelar el entorno.
Un usuario no es parte del software
Por ejemplo
Usuario

↓

Hace Login

↓

Sistema

↓

Devuelve sesión
El Usuario nunca fue modelado.
En Gherkin esto queda implícito.
Given user exists

When user logs in

Then...
Pero ASRS pretende ser arquitectura también.
Entonces ya no alcanza.
Yo agregaría una nueva entidad
Actor
Actor USER

    Name

        Registered User

    Description

        Uses the application.
Ahora sí.
Después un escenario puede decir

Scenario LOGIN

    Actor

        USER

    Uses

        COMP-WEB

        COMP-AUTH

    Given

        Registered user

    When

        Login

    Then

        Session created
Eso ya empieza a parecer UML Use Cases.
Pero muchísimo más simple.
Incluso varios actores
Actor VISITOR

Actor USER

Actor ADMIN

Actor SYSTEM

Actor PAYMENT_PROVIDER
Luego
Scenario CREATE_USER

    Actor

        VISITOR
Scenario DELETE_USER

    Actor

        ADMIN
Scenario EXPIRE_SESSION

    Actor

        SYSTEM
Y aquí aparece algo interesante
No todos los actores son personas.
Ejemplo
Stripe.
Actor STRIPE

    Type

        External System
GitHub
Actor GITHUB

    Type

        OAuth Provider
OpenAI
Actor OPENAI

    Type

        AI Provider
Cron
Actor CRON

    Type

        Scheduler
Entonces Actor no significa humano.
Significa
Entidad externa que inicia comportamiento.
Eso me gusta mucho más.
Entonces Actor debería tener tipos
Human

Organization

External System

Service

Agent

Scheduler

Device
Ejemplo
Actor USER

    Type

        Human
Actor GITHUB

    Type

        External System
Actor CHATGPT

    Type

        Agent
Actor CAMERA

    Type

        Device
Y hay otra consecuencia
Los escenarios deberían empezar siempre por el actor.
Hoy
Scenario LOGIN

    Uses

        COMP-WEB
Yo lo cambiaría por
Scenario LOGIN

    Actor

        USER

    Uses

        COMP-WEB

        COMP-AUTH
Porque responde inmediatamente
¿Quién inicia este comportamiento?
Pero creo que podemos ir un paso más allá
Creo que Actor sigue siendo demasiado específico.
En ingeniería de software existe un concepto más general:
Principal.
Un Principal es cualquier identidad que puede interactuar con el sistema.
Puede ser:
un usuario,
un administrador,
una API,
un servicio,
un dispositivo,
un agente de IA,
un scheduler,
un robot,
otro sistema.
Entonces propondría cambiar la entidad a:
Principal USER

    Type

        Human

Principal ADMIN

    Type

        Human

Principal GITHUB

    Type

        External System

Principal OPENAI

    Type

        Agent

Principal CRON

    Type

        Scheduler
Y los escenarios quedarían así:
Scenario LOGIN

    Principal

        USER

    Uses

        COMP-WEB

        COMP-AUTH

    Given

        Registered user

    When

        Login

    Then

        Session created
Creo que Principal encaja incluso mejor que Actor con la filosofía de ASRS. No describe "quién actúa" en un sentido teatral, sino quién posee la identidad que inicia o provoca una interacción con el sistema. Además, se alinea muy bien con conceptos ampliamente usados en autenticación y autorización (como IAM, OAuth y sistemas de permisos), y hace que ASRS pueda modelar desde un usuario humano hasta un agente de IA o un webhook sin introducir conceptos especiales para cada caso. Ese cambio, junto con la eliminación del objeto Relationship, me parece uno de los dos avances más importantes para una futura ASRS 2.1.