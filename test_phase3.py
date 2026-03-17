from app.parser import parse_input
from app.analyzer import generate_threat_model
import json

print("Step 1: Parsing README.md...")
parsed = parse_input("README.md")
print(f"Parsed input type: {parsed['type']}")
print(f"Content preview: {parsed['content']}")

print("\nStep 2: Generating threat model...")
result = generate_threat_model(parsed)
print("\nStep 3: Result:")
print(json.dumps(result, indent=2))

