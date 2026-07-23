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
