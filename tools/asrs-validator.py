#!/usr/bin/env python3
"""
ASRS Validator - Validates Agent Software Requirements Specification documents.

Usage:
    python asrs-validator.py document.asrs
    python asrs-validator.py document.asrs --json
    python asrs-validator.py document.asrs --strict
    python asrs-validator.py document.yaml
    python asrs-validator.py document.yml
"""

import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple

# Try to import yaml, with fallback
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


# ASRS Entity Types
ENTITY_TYPES = {
    "Project", "Principal", "Feature", "Scenario",
    "Component", "Resource", "Test"
}

# Required properties per entity type (PascalCase for ASRS format)
REQUIRED_PROPERTIES = {
    "Project": ["Name", "Specification", "Document Version"],
    "Principal": ["Type"],
    "Feature": [],
    "Scenario": ["Given", "When", "Then"],
    "Component": ["Type"],
    "Resource": ["Type"],
    "Test": ["Validates", "Given", "When", "Then"],
}

# Valid Principal types
PRINCIPAL_TYPES = {"Human", "External System", "Service", "Agent", "Scheduler", "Device"}

# Valid Component types
COMPONENT_TYPES = {"Service", "Frontend", "Backend", "Library", "Worker", "Agent", "Gateway", "External"}

# Valid Resource types
RESOURCE_TYPES = {"Table", "Bucket", "Cache", "Queue", "Secret"}

# Valid reference properties
REFERENCE_PROPERTIES = {"Uses", "Creates", "Reads", "Writes", "Publishes", "Consumes", "Validates", "Principal"}

# YAML entity type mappings
YAML_ENTITY_MAPPINGS = {
    "project": "Project",
    "principals": "Principal",
    "features": "Feature",
    "scenarios": "Scenario",
    "components": "Component",
    "resources": "Resource",
    "tests": "Test"
}

# YAML required properties per entity type (lowercase keys)
YAML_REQUIRED_PROPERTIES = {
    "Project": ["id", "name", "specification", "document_version"],
    "Principal": ["id", "type"],
    "Feature": ["id"],
    "Scenario": ["id", "principal", "given", "when", "then"],
    "Component": ["id", "type"],
    "Resource": ["id", "type"],
    "Test": ["id", "validates", "given", "when", "then"],
}

# YAML reference properties (lowercase)
YAML_REFERENCE_PROPERTIES = {
    "uses", "creates", "reads", "writes", "publishes", "consumes", "validates", "principal"
}

# Valid types for YAML
YAML_PRINCIPAL_TYPES = {"Human", "External System", "Service", "Agent", "Scheduler", "Device"}
YAML_COMPONENT_TYPES = {"Service", "Frontend", "Backend", "Library", "Worker", "Agent", "Gateway", "External"}
YAML_RESOURCE_TYPES = {"Table", "Bucket", "Cache", "Queue", "Secret"}


@dataclass
class Entity:
    """Represents an ASRS entity."""
    type: str
    id: str
    line: int
    properties: Dict[str, List[str]] = field(default_factory=dict)
    raw_lines: List[str] = field(default_factory=list)


@dataclass
class ValidationError:
    """Represents a validation error."""
    line: int
    message: str
    severity: str  # "error" or "warning"
    entity_id: Optional[str] = None


class ASRSValidator:
    """Validates ASRS documents (old .asrs format)."""
    
    def __init__(self, strict: bool = False):
        self.strict = strict
        self.entities: List[Entity] = []
        self.errors: List[ValidationError] = []
        self.entity_ids: Set[str] = set()
        self.project_count = 0
    
    def validate(self, content: str) -> Tuple[List[ValidationError], List[Entity]]:
        """Validate ASRS content and return errors and entities."""
        lines = content.split('\n')
        self._parse_entities(lines)
        self._validate_entities()
        self._validate_references()
        self._validate_structure()
        return self.errors, self.entities
    
    def _parse_entities(self, lines: List[str]):
        """Parse entities from ASRS content."""
        current_entity = None
        current_property = None
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                continue
            
            # Calculate indentation (4 spaces per level)
            indentation = len(line) - len(line.lstrip())
            level = indentation // 4
            
            # Check for entity declaration
            entity_match = re.match(r'^(' + '|'.join(ENTITY_TYPES) + r')\s+([A-Z][A-Z0-9-]+)$', stripped)
            if entity_match:
                entity_type = entity_match.group(1)
                entity_id = entity_match.group(2)
                
                current_entity = Entity(
                    type=entity_type,
                    id=entity_id,
                    line=i,
                    raw_lines=[line]
                )
                self.entities.append(current_entity)
                current_property = None
                continue
            
            # Check for property (at indentation level 1)
            if current_entity and level == 1 and not line.startswith('        '):
                property_name = stripped
                current_property = property_name
                if property_name not in current_entity.properties:
                    current_entity.properties[property_name] = []
                current_entity.raw_lines.append(line)
                continue
            
            # Check for value (at indentation level 2)
            if current_entity and current_property and level == 2:
                value = stripped
                current_entity.properties[current_property].append(value)
                current_entity.raw_lines.append(line)
                continue
    
    def _validate_entities(self):
        """Validate each entity."""
        seen_ids = set()
        
        for entity in self.entities:
            # Check for duplicate IDs
            if entity.id in seen_ids:
                self.errors.append(ValidationError(
                    line=entity.line,
                    message=f"Duplicate ID: {entity.id}",
                    severity="error",
                    entity_id=entity.id
                ))
            seen_ids.add(entity.id)
            self.entity_ids.add(entity.id)
            
            # Count projects
            if entity.type == "Project":
                self.project_count += 1
            
            # Validate required properties
            required = REQUIRED_PROPERTIES.get(entity.type, [])
            for prop in required:
                if prop not in entity.properties or not entity.properties[prop]:
                    self.errors.append(ValidationError(
                        line=entity.line,
                        message=f"{entity.type} {entity.id} missing required property: {prop}",
                        severity="error",
                        entity_id=entity.id
                    ))
            
            # Validate Principal type
            if entity.type == "Principal" and "Type" in entity.properties:
                principal_type = entity.properties["Type"][0] if entity.properties["Type"] else ""
                if principal_type not in PRINCIPAL_TYPES:
                    self.errors.append(ValidationError(
                        line=entity.line,
                        message=f"Invalid Principal type: {principal_type}. Valid: {', '.join(PRINCIPAL_TYPES)}",
                        severity="warning",
                        entity_id=entity.id
                    ))
            
            # Validate Component type
            if entity.type == "Component" and "Type" in entity.properties:
                component_type = entity.properties["Type"][0] if entity.properties["Type"] else ""
                if component_type not in COMPONENT_TYPES:
                    self.errors.append(ValidationError(
                        line=entity.line,
                        message=f"Invalid Component type: {component_type}. Valid: {', '.join(COMPONENT_TYPES)}",
                        severity="warning",
                        entity_id=entity.id
                    ))
            
            # Validate Resource type
            if entity.type == "Resource" and "Type" in entity.properties:
                resource_type = entity.properties["Type"][0] if entity.properties["Type"] else ""
                if resource_type not in RESOURCE_TYPES:
                    self.errors.append(ValidationError(
                        line=entity.line,
                        message=f"Invalid Resource type: {resource_type}. Valid: {', '.join(RESOURCE_TYPES)}",
                        severity="warning",
                        entity_id=entity.id
                    ))
    
    def _validate_references(self):
        """Validate that all references point to existing entities."""
        for entity in self.entities:
            for prop_name, values in entity.properties.items():
                if prop_name in REFERENCE_PROPERTIES:
                    for value in values:
                        # Skip non-ID values
                        if not re.match(r'^[A-Z][A-Z0-9-]+$', value):
                            continue
                        if value not in self.entity_ids:
                            self.errors.append(ValidationError(
                                line=entity.line,
                                message=f"Reference to non-existent entity: {value}",
                                severity="error",
                                entity_id=entity.id
                            ))
    
    def _validate_structure(self):
        """Validate document structure."""
        if self.project_count == 0:
            self.errors.append(ValidationError(
                line=1,
                message="No Project entity found. Exactly one Project MUST exist.",
                severity="error"
            ))
        elif self.project_count > 1:
            self.errors.append(ValidationError(
                line=1,
                message=f"Multiple Project entities found ({self.project_count}). Exactly one Project MUST exist.",
                severity="error"
            ))


class ASRSYAMLValidator:
    """Validates YAML ASRS documents."""
    
    def __init__(self, strict: bool = False):
        self.strict = strict
        self.entities: List[Entity] = []
        self.errors: List[ValidationError] = []
        self.entity_ids: Set[str] = set()
        self.project_count = 0
    
    def validate(self, content: str) -> Tuple[List[ValidationError], List[Entity]]:
        """Validate YAML ASRS content and return errors and entities."""
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            self.errors.append(ValidationError(line=1, message=f"YAML parsing error: {e}", severity="error"))
            return self.errors, self.entities
        
        if not data or not isinstance(data, dict):
            self.errors.append(ValidationError(line=1, message="Empty or invalid YAML document", severity="error"))
            return self.errors, self.entities
        
        # 1. Validate project (required, exactly one)
        if "project" not in data:
            self.errors.append(ValidationError(line=1, message="Missing 'project' key", severity="error"))
            return self.errors, self.entities
        
        self._add_entity(data["project"], "Project", 1)
        
        # 2. Validate other entity arrays
        for yaml_key, entity_type in YAML_ENTITY_MAPPINGS.items():
            if yaml_key == "project":
                continue
            if yaml_key not in data:
                continue
            items = data[yaml_key]
            if not isinstance(items, list):
                self.errors.append(ValidationError(line=1, message=f"'{yaml_key}' must be a list", severity="error"))
                continue
            for i, item in enumerate(items):
                if isinstance(item, dict):
                    self._add_entity(item, entity_type, i + 2)
        
        # 3. Validate entities
        self._validate_all_entities()
        
        # 4. Validate references
        self._validate_references()
        
        # 5. Validate structure
        self._validate_structure()
        
        return self.errors, self.entities
    
    def _add_entity(self, data: dict, entity_type: str, line: int):
        """Add an entity from YAML data."""
        entity_id = str(data.get("id", ""))
        if not entity_id:
            self.errors.append(ValidationError(line=line, message=f"{entity_type} missing 'id' field", severity="error"))
            entity_id = f"UNKNOWN-{entity_type}-{line}"
        
        # Convert all YAML keys to properties (keep id too for validation)
        properties = {}
        for key, value in data.items():
            if isinstance(value, list):
                properties[key] = [str(v) for v in value]
            else:
                properties[key] = [str(value)] if value is not None else []
        
        entity = Entity(type=entity_type, id=entity_id, line=line, properties=properties)
        self.entities.append(entity)
        self.entity_ids.add(entity_id)
        
        if entity_type == "Project":
            self.project_count += 1
    
    def _validate_all_entities(self):
        """Validate all entities."""
        seen_ids = set()
        
        for entity in self.entities:
            # Duplicate IDs
            if entity.id in seen_ids:
                self.errors.append(ValidationError(line=entity.line, message=f"Duplicate ID: {entity.id}", severity="error", entity_id=entity.id))
            seen_ids.add(entity.id)
            
            # Required properties
            required = YAML_REQUIRED_PROPERTIES.get(entity.type, [])
            for prop in required:
                if prop not in entity.properties or not entity.properties[prop]:
                    self.errors.append(ValidationError(line=entity.line, message=f"{entity.type} {entity.id} missing required property: {prop}", severity="error", entity_id=entity.id))
            
            # Type validation
            if entity.type == "Principal" and "type" in entity.properties:
                pt = entity.properties["type"][0] if entity.properties["type"] else ""
                if pt not in YAML_PRINCIPAL_TYPES:
                    self.errors.append(ValidationError(line=entity.line, message=f"Invalid Principal type: {pt}. Valid: {', '.join(YAML_PRINCIPAL_TYPES)}", severity="warning", entity_id=entity.id))
            
            if entity.type == "Component" and "type" in entity.properties:
                ct = entity.properties["type"][0] if entity.properties["type"] else ""
                if ct not in YAML_COMPONENT_TYPES:
                    self.errors.append(ValidationError(line=entity.line, message=f"Invalid Component type: {ct}. Valid: {', '.join(YAML_COMPONENT_TYPES)}", severity="warning", entity_id=entity.id))
            
            if entity.type == "Resource" and "type" in entity.properties:
                rt = entity.properties["type"][0] if entity.properties["type"] else ""
                if rt not in YAML_RESOURCE_TYPES:
                    self.errors.append(ValidationError(line=entity.line, message=f"Invalid Resource type: {rt}. Valid: {', '.join(YAML_RESOURCE_TYPES)}", severity="warning", entity_id=entity.id))
    
    def _validate_references(self):
        """Validate that all references point to existing entities."""
        for entity in self.entities:
            for prop_name, values in entity.properties.items():
                if prop_name in YAML_REFERENCE_PROPERTIES:
                    for value in values:
                        # Check if value looks like an ID reference (UPPER-CASE format)
                        if re.match(r'^[A-Z][A-Z0-9-]+$', value):
                            if value not in self.entity_ids:
                                self.errors.append(ValidationError(line=entity.line, message=f"Reference to non-existent entity: {value}", severity="error", entity_id=entity.id))
    
    def _validate_structure(self):
        """Validate document structure."""
        if self.project_count == 0:
            self.errors.append(ValidationError(line=1, message="No Project found. Exactly one Project MUST exist.", severity="error"))
        elif self.project_count > 1:
            self.errors.append(ValidationError(line=1, message=f"Multiple Projects found ({self.project_count}). Exactly one Project MUST exist.", severity="error"))


def format_errors(errors: List[ValidationError], use_json: bool = False) -> str:
    """Format validation errors."""
    if use_json:
        return json.dumps([{
            "line": e.line,
            "message": e.message,
            "severity": e.severity,
            "entity_id": e.entity_id
        } for e in errors], indent=2)
    
    if not errors:
        return "✓ Document is valid"
    
    error_count = sum(1 for e in errors if e.severity == "error")
    warning_count = sum(1 for e in errors if e.severity == "warning")
    
    lines = [f"Found {error_count} error(s) and {warning_count} warning(s)\n"]
    for error in sorted(errors, key=lambda x: x.line):
        prefix = "✗" if error.severity == "error" else "⚠"
        lines.append(f"{prefix} Line {error.line}: {error.message}")
    
    return "\n".join(lines)


def print_summary(entities: List[Entity]):
    """Print entity summary."""
    counts = {}
    for entity in entities:
        counts[entity.type] = counts.get(entity.type, 0) + 1
    
    print("\nEntity Summary:")
    for entity_type in ENTITY_TYPES:
        count = counts.get(entity_type, 0)
        if count > 0:
            print(f"  {entity_type}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate ASRS (Agent Software Requirements Specification) documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.asrs
  %(prog)s document.yaml
  %(prog)s document.yaml --json
  %(prog)s document.yaml --strict
  %(prog)s document.yaml --summary
        """
    )
    parser.add_argument("file", help="ASRS document to validate (.asrs, .yaml, .yml)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--summary", action="store_true", help="Show entity summary")
    
    args = parser.parse_args()
    
    # Read file
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Determine format and validate
    file_ext = file_path.suffix.lower()
    
    if file_ext in ('.yaml', '.yml'):
        if not YAML_AVAILABLE:
            print("Error: YAML support requires pyyaml. Install: pip install pyyaml", file=sys.stderr)
            sys.exit(1)
        validator = ASRSYAMLValidator(strict=args.strict)
    elif file_ext == '.asrs':
        validator = ASRSValidator(strict=args.strict)
    else:
        print(f"Error: Unsupported format '{file_ext}'. Use .asrs, .yaml, or .yml", file=sys.stderr)
        sys.exit(1)
    
    errors, entities = validator.validate(content)
    
    # Filter errors based on strict mode
    if args.strict:
        display_errors = errors
    else:
        display_errors = [e for e in errors if e.severity == "error"]
    
    # Output
    if args.json:
        print(format_errors(display_errors, use_json=True))
    else:
        print(format_errors(display_errors))
        if args.summary:
            print_summary(entities)
    
    error_count = sum(1 for e in display_errors if e.severity == "error")
    sys.exit(1 if error_count > 0 else 0)


if __name__ == "__main__":
    main()
