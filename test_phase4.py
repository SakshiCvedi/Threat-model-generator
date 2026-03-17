from app.parser import parse_input
from app.analyzer import generate_threat_model
from app.renderer import render_terminal, render_markdown, render_pdf

print("Parsing...")
parsed = parse_input('README.md')

print("Generating threat model...")
threat_model = generate_threat_model(parsed)

print("\n--- TERMINAL OUTPUT ---")
render_terminal(threat_model)

print("--- MARKDOWN OUTPUT ---")
render_markdown(threat_model)

print("--- PDF OUTPUT ---")
render_pdf(threat_model)

print("\nAll 3 outputs done!")