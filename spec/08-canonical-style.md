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
