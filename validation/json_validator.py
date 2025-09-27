#!/usr/bin/env python3
"""
JSON Schema Validator for Binom API Encyclopedia
"""

import json
import jsonschema
import os
from pathlib import Path

class BinomAPIValidator:
    
    def __init__(self):
        self.schemas = self.load_schemas()
    
    def load_schemas(self):
        """Load validation schemas"""
        return {
            "endpoint": {
                "type": "object",
                "required": ["method", "path", "description"],
                "properties": {
                    "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"]},
                    "path": {"type": "string"},
                    "description": {"type": "string"},
                    "parameters": {"type": "object"},
                    "responses": {"type": "object"}
                }
            },
            "workflow": {
                "type": "object",
                "required": ["name", "goal", "steps"],
                "properties": {
                    "name": {"type": "string"},
                    "goal": {"type": "string"},
                    "steps": {"type": "array"},
                    "ai_pattern": {"type": "string"}
                }
            }
        }
    
    def validate_json_file(self, filepath, schema_name):
        """Validate a JSON file against a schema"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if schema_name in self.schemas:
                jsonschema.validate(data, self.schemas[schema_name])
                return True, "Valid"
            else:
                return False, f"Unknown schema: {schema_name}"
                
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}"
        except jsonschema.ValidationError as e:
            return False, f"Schema validation failed: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def validate_all_workflows(self):
        """Validate all workflow files"""
        workflows_dir = Path("/home/ubuntu/binom-api-encyclopedia/workflows")
        results = []
        
        if workflows_dir.exists():
            for json_file in workflows_dir.glob("*.json"):
                is_valid, message = self.validate_json_file(json_file, "workflow")
                results.append({
                    "file": str(json_file),
                    "valid": is_valid,
                    "message": message
                })
        
        return results

if __name__ == "__main__":
    validator = BinomAPIValidator()
    results = validator.validate_all_workflows()
    
    print("Validation Results:")
    print("=" * 50)
    for result in results:
        status = "✅ PASS" if result["valid"] else "❌ FAIL"
        print(f"{status} {result['file']}: {result['message']}")
