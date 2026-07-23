# 7. Grammar

ASRS defines the abstract grammar. The concrete syntax depends on the format (see Section 17: Format Specification).

## Abstract Grammar

ASRS defines three core constructs:

- **Entity**: A uniquely identifiable concept
- **Property**: A named attribute of an entity
- **List**: An ordered collection of values

---

## Entity

Every entity has:
- **Type**: The kind of entity (Project, Principal, Feature, Scenario, Component, Resource, Test)
- **ID**: A unique identifier (PREFIX-NAME format)
- **Properties**: Named attributes

---

## Property

Every property has:
- **Name**: PascalCase identifier
- **Value**: String, list, or reference

---

## List

Lists are:
- **Ordered**: Sequence matters
- **Typed**: All items share the same type
- **Homogeneous**: No mixed types

---

## Format Mapping

The abstract grammar maps to concrete formats:

| Abstract | YAML | JSON | TOML |
|----------|------|------|------|
| Entity | Top-level key + array item | Object in array | [[section]] |
| Property | Object key | Object key | Key = value |
| List | Array | Array | Array |

See Section 17 for complete format specifications.
