#!/usr/bin/env python3
"""
ASRS Converter - Convert between ASRS and YAML formats.

Usage:
    python3 asrs-convert.py document.asrs --to yaml
    python3 asrs-convert.py document.yaml --to asrs
"""

import re
import sys
import yaml
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class Entity:
    """Represents an ASRS entity."""
    type: str
    id: str
    line: int
    properties: Dict[str, List[str]] = field(default_factory=dict)


class ASRSParser:
    """Parse ASRS documents."""
    
    ENTITY_TYPES = {
        "Project", "Principal", "Feature", "Scenario",
        "Component", "Resource", "Test"
    }
    
    def parse(self, content: str) -> List[Entity]:
        """Parse ASRS content into entities."""
        lines = content.split('\n')
        entities = []
        current_entity = None
        current_property = None
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                continue
            
            # Calculate indentation
            indentation = len(line) - len(line.lstrip())
            level = indentation // 4
            
            # Check for entity declaration
            entity_match = re.match(
                r'^(' + '|'.join(self.ENTITY_TYPES) + r')\s+([A-Z][A-Z0-9-]+)$',
                stripped
            )
            if entity_match:
                entity_type = entity_match.group(1)
                entity_id = entity_match.group(2)
                
                current_entity = Entity(
                    type=entity_type,
                    id=entity_id,
                    line=i
                )
                entities.append(current_entity)
                current_property = None
                continue
            
            # Check for property (at indentation level 1)
            if current_entity and level == 1:
                current_property = stripped
                if current_property not in current_entity.properties:
                    current_entity.properties[current_property] = []
                continue
            
            # Check for value (at indentation level 2)
            if current_entity and current_property and level == 2:
                current_entity.properties[current_property].append(stripped)
                continue
        
        return entities


class ASRSConverter:
    """Convert between ASRS and YAML formats."""
    
    def __init__(self):
        self.parser = ASRSParser()
    
    def asrs_to_yaml(self, asrs_content: str) -> str:
        """Convert ASRS to YAML format."""
        entities = self.parser.parse(asrs_content)
        
        # Group entities by type
        grouped = {}
        for entity in entities:
            if entity.type not in grouped:
                grouped[entity.type] = []
            grouped[entity.type].append(entity)
        
        # Build YAML structure
        yaml_data = {}
        
        # Project (singular)
        if "Project" in grouped:
            project = grouped["Project"][0]
            yaml_data["project"] = {
                "id": project.id,
                "name": project.properties.get("Name", [""])[0],
                "specification": project.properties.get("Specification", [""])[0],
                "document_version": project.properties.get("Document Version", [""])[0],
            }
            if "Description" in project.properties:
                yaml_data["project"]["description"] = project.properties["Description"][0]
            if "Compliance Level" in project.properties:
                yaml_data["project"]["compliance_level"] = project.properties["Compliance Level"][0]
        
        # Principals
        if "Principal" in grouped:
            yaml_data["principals"] = []
            for entity in grouped["Principal"]:
                principal = {
                    "id": entity.id,
                    "type": entity.properties.get("Type", [""])[0],
                }
                if "Description" in entity.properties:
                    principal["description"] = entity.properties["Description"][0]
                if "Can" in entity.properties:
                    principal["can"] = entity.properties["Can"]
                yaml_data["principals"].append(principal)
        
        # Features
        if "Feature" in grouped:
            yaml_data["features"] = []
            for entity in grouped["Feature"]:
                feature = {"id": entity.id}
                if "Description" in entity.properties:
                    feature["description"] = entity.properties["Description"][0]
                if "Requirements" in entity.properties:
                    feature["requirements"] = entity.properties["Requirements"]
                yaml_data["features"].append(feature)
        
        # Scenarios
        if "Scenario" in grouped:
            yaml_data["scenarios"] = []
            for entity in grouped["Scenario"]:
                scenario = {"id": entity.id}
                if "Principal" in entity.properties:
                    scenario["principal"] = entity.properties["Principal"][0]
                if "Uses" in entity.properties:
                    scenario["uses"] = entity.properties["Uses"]
                if "Given" in entity.properties:
                    scenario["given"] = entity.properties["Given"]
                if "When" in entity.properties:
                    scenario["when"] = entity.properties["When"]
                if "Then" in entity.properties:
                    scenario["then"] = entity.properties["Then"]
                yaml_data["scenarios"].append(scenario)
        
        # Components
        if "Component" in grouped:
            yaml_data["components"] = []
            for entity in grouped["Component"]:
                component = {
                    "id": entity.id,
                    "type": entity.properties.get("Type", [""])[0],
                }
                if "Technology" in entity.properties:
                    component["technology"] = entity.properties["Technology"][0]
                if "Responsibilities" in entity.properties:
                    component["responsibilities"] = entity.properties["Responsibilities"]
                if "Uses" in entity.properties:
                    component["uses"] = entity.properties["Uses"]
                if "Creates" in entity.properties:
                    component["creates"] = entity.properties["Creates"]
                if "Reads" in entity.properties:
                    component["reads"] = entity.properties["Reads"]
                if "Writes" in entity.properties:
                    component["writes"] = entity.properties["Writes"]
                if "Publishes" in entity.properties:
                    component["publishes"] = entity.properties["Publishes"]
                if "Consumes" in entity.properties:
                    component["consumes"] = entity.properties["Consumes"]
                if "Verify" in entity.properties:
                    component["verify"] = entity.properties["Verify"]
                yaml_data["components"].append(component)
        
        # Resources
        if "Resource" in grouped:
            yaml_data["resources"] = []
            for entity in grouped["Resource"]:
                resource = {
                    "id": entity.id,
                    "type": entity.properties.get("Type", [""])[0],
                }
                if "Schema" in entity.properties:
                    resource["schema"] = entity.properties["Schema"]
                yaml_data["resources"].append(resource)
        
        # Tests
        if "Test" in grouped:
            yaml_data["tests"] = []
            for entity in grouped["Test"]:
                test = {"id": entity.id}
                if "Validates" in entity.properties:
                    test["validates"] = entity.properties["Validates"]
                if "Given" in entity.properties:
                    test["given"] = entity.properties["Given"]
                if "When" in entity.properties:
                    test["when"] = entity.properties["When"]
                if "Then" in entity.properties:
                    test["then"] = entity.properties["Then"]
                yaml_data["tests"].append(test)
        
        return yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)
    
    def yaml_to_asrs(self, yaml_content: str) -> str:
        """Convert YAML to ASRS format."""
        yaml_data = yaml.safe_load(yaml_content)
        lines = []
        
        # Project
        if "project" in yaml_data:
            project = yaml_data["project"]
            lines.append(f"Project {project['id']}")
            lines.append("")
            lines.append("    Name")
            lines.append("")
            lines.append(f"        {project['name']}")
            lines.append("")
            lines.append("    Specification")
            lines.append("")
            lines.append(f"        {project['specification']}")
            lines.append("")
            lines.append("    Document Version")
            lines.append("")
            lines.append(f"        {project['document_version']}")
            if "description" in project:
                lines.append("")
                lines.append("    Description")
                lines.append("")
                lines.append(f"        {project['description']}")
            if "compliance_level" in project:
                lines.append("")
                lines.append("    Compliance Level")
                lines.append("")
                lines.append(f"        {project['compliance_level']}")
            lines.append("")
            lines.append("")
        
        # Principals
        if "principals" in yaml_data:
            for principal in yaml_data["principals"]:
                lines.append(f"Principal {principal['id']}")
                lines.append("")
                lines.append("    Type")
                lines.append("")
                lines.append(f"        {principal['type']}")
                if "description" in principal:
                    lines.append("")
                    lines.append("    Description")
                    lines.append("")
                    lines.append(f"        {principal['description']}")
                if "can" in principal:
                    lines.append("")
                    lines.append("    Can")
                    for item in principal["can"]:
                        lines.append("")
                        lines.append(f"        {item}")
                lines.append("")
                lines.append("")
        
        # Features
        if "features" in yaml_data:
            for feature in yaml_data["features"]:
                lines.append(f"Feature {feature['id']}")
                if "description" in feature:
                    lines.append("")
                    lines.append("    Description")
                    lines.append("")
                    lines.append(f"        {feature['description']}")
                if "requirements" in feature:
                    lines.append("")
                    lines.append("    Requirements")
                    for req in feature["requirements"]:
                        lines.append("")
                        lines.append(f"        {req}")
                lines.append("")
                lines.append("")
        
        # Scenarios
        if "scenarios" in yaml_data:
            for scenario in yaml_data["scenarios"]:
                lines.append(f"Scenario {scenario['id']}")
                if "principal" in scenario:
                    lines.append("")
                    lines.append("    Principal")
                    lines.append("")
                    lines.append(f"        {scenario['principal']}")
                if "uses" in scenario:
                    lines.append("")
                    lines.append("    Uses")
                    for use in scenario["uses"]:
                        lines.append("")
                        lines.append(f"        {use}")
                if "given" in scenario:
                    lines.append("")
                    lines.append("    Given")
                    lines.append("")
                    lines.append(f"        {scenario['given']}")
                if "when" in scenario:
                    lines.append("")
                    lines.append("    When")
                    lines.append("")
                    lines.append(f"        {scenario['when']}")
                if "then" in scenario:
                    lines.append("")
                    lines.append("    Then")
                    lines.append("")
                    lines.append(f"        {scenario['then']}")
                lines.append("")
                lines.append("")
        
        # Components
        if "components" in yaml_data:
            for component in yaml_data["components"]:
                lines.append(f"Component {component['id']}")
                lines.append("")
                lines.append("    Type")
                lines.append("")
                lines.append(f"        {component['type']}")
                if "technology" in component:
                    lines.append("")
                    lines.append("    Technology")
                    lines.append("")
                    lines.append(f"        {component['technology']}")
                if "responsibilities" in component:
                    lines.append("")
                    lines.append("    Responsibilities")
                    for resp in component["responsibilities"]:
                        lines.append("")
                        lines.append(f"        {resp}")
                if "uses" in component:
                    lines.append("")
                    lines.append("    Uses")
                    for use in component["uses"]:
                        lines.append("")
                        lines.append(f"        {use}")
                if "creates" in component:
                    lines.append("")
                    lines.append("    Creates")
                    for create in component["creates"]:
                        lines.append("")
                        lines.append(f"        {create}")
                if "reads" in component:
                    lines.append("")
                    lines.append("    Reads")
                    for read in component["reads"]:
                        lines.append("")
                        lines.append(f"        {read}")
                if "writes" in component:
                    lines.append("")
                    lines.append("    Writes")
                    for write in component["writes"]:
                        lines.append("")
                        lines.append(f"        {write}")
                if "publishes" in component:
                    lines.append("")
                    lines.append("    Publishes")
                    for pub in component["publishes"]:
                        lines.append("")
                        lines.append(f"        {pub}")
                if "consumes" in component:
                    lines.append("")
                    lines.append("    Consumes")
                    for cons in component["consumes"]:
                        lines.append("")
                        lines.append(f"        {cons}")
                if "verify" in component:
                    lines.append("")
                    lines.append("    Verify")
                    for v in component["verify"]:
                        lines.append("")
                        lines.append(f"        {v}")
                lines.append("")
                lines.append("")
        
        # Resources
        if "resources" in yaml_data:
            for resource in yaml_data["resources"]:
                lines.append(f"Resource {resource['id']}")
                lines.append("")
                lines.append("    Type")
                lines.append("")
                lines.append(f"        {resource['type']}")
                if "schema" in resource:
                    lines.append("")
                    lines.append("    Schema")
                    for field in resource["schema"]:
                        lines.append("")
                        lines.append(f"        {field}")
                lines.append("")
                lines.append("")
        
        # Tests
        if "tests" in yaml_data:
            for test in yaml_data["tests"]:
                lines.append(f"Test {test['id']}")
                if "validates" in test:
                    lines.append("")
                    lines.append("    Validates")
                    for val in test["validates"]:
                        lines.append("")
                        lines.append(f"        {val}")
                if "given" in test:
                    lines.append("")
                    lines.append("    Given")
                    lines.append("")
                    lines.append(f"        {test['given']}")
                if "when" in test:
                    lines.append("")
                    lines.append("    When")
                    lines.append("")
                    lines.append(f"        {test['when']}")
                if "then" in test:
                    lines.append("")
                    lines.append("    Then")
                    lines.append("")
                    lines.append(f"        {test['then']}")
                lines.append("")
                lines.append("")
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Convert between ASRS and YAML formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.asrs --to yaml
  %(prog)s document.yaml --to asrs
        """
    )
    parser.add_argument("file", help="Input file")
    parser.add_argument("--to", choices=["yaml", "asrs"], required=True,
                        help="Output format")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    # Read input file
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Convert
    converter = ASRSConverter()
    
    if args.to == "yaml":
        if not file_path.suffix.endswith('.asrs'):
            print("Warning: Input file doesn't have .asrs extension", file=sys.stderr)
        result = converter.asrs_to_yaml(content)
    else:  # asrs
        if not file_path.suffix.endswith('.yaml') and not file_path.suffix.endswith('.yml'):
            print("Warning: Input file doesn't have .yaml/.yml extension", file=sys.stderr)
        result = converter.yaml_to_asrs(content)
    
    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(result, encoding="utf-8")
        print(f"Converted to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
