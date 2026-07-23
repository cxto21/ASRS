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
