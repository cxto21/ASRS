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
