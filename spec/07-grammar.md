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
