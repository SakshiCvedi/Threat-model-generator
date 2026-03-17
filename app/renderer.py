import os
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table as RLTable, TableStyle

# Rich console — used for all terminal output
console = Console()


# ─────────────────────────────────────────
# OUTPUT 1 — Terminal table using Rich
# ─────────────────────────────────────────

def render_terminal(threat_model: dict):
    """Prints a beautiful colored threat model table in the terminal"""

    # Header panel
    console.print()
    console.print(Panel(
        f"[bold white]{threat_model.get('system_name', 'Unknown System')}[/bold white]\n"
        f"[dim]Overall Risk Score: [/dim][bold red]{threat_model.get('overall_risk_score', 'N/A')}/10[/bold red]",
        title="[bold blue]Threat Model Report[/bold blue]",
        border_style="blue"
    ))

    # Trust boundaries
    console.print("\n[bold yellow]Trust Boundaries:[/bold yellow]")
    for boundary in threat_model.get("trust_boundaries", []):
        console.print(f"  [dim]▸[/dim] {boundary}")

    # STRIDE table
    console.print()
    table = Table(
        title="STRIDE Analysis",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold white on dark_blue"
    )

    table.add_column("Category",   style="cyan bold",   width=22)
    table.add_column("Risk Level", style="magenta",     width=12)
    table.add_column("Top Threat", style="white",       width=38)
    table.add_column("Top Mitigation", style="green",   width=38)

    # Risk color mapping
    risk_colors = {
        "Critical": "[bold red]Critical[/bold red]",
        "High":     "[red]High[/red]",
        "Medium":   "[yellow]Medium[/yellow]",
        "Low":      "[green]Low[/green]"
    }

    stride_categories = [
        "spoofing",
        "tampering",
        "repudiation",
        "information_disclosure",
        "denial_of_service",
        "elevation_of_privilege"
    ]

    for category in stride_categories:
        data = threat_model.get("stride", {}).get(category, {})
        risk        = data.get("risk", "Unknown")
        threats     = data.get("threats", ["N/A"])
        mitigations = data.get("mitigations", ["N/A"])

        table.add_row(
            category.replace("_", " ").title(),
            risk_colors.get(risk, risk),
            threats[0] if threats else "N/A",
            mitigations[0] if mitigations else "N/A"
        )

    console.print(table)

    # Top 3 actions
    console.print("\n[bold red]⚡ Top 3 Immediate Actions:[/bold red]")
    for i, action in enumerate(threat_model.get("top_3_actions", []), 1):
        console.print(f"  [bold white]{i}.[/bold white] {action}")

    console.print()


# ─────────────────────────────────────────
# OUTPUT 2 — Markdown file
# ─────────────────────────────────────────

def render_markdown(threat_model: dict) -> str:
    """Generates a markdown string and saves it to outputs/"""

    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines.append(f"# Threat Model: {threat_model.get('system_name', 'Unknown')}")
    lines.append(f"\n**Generated:** {timestamp}")
    lines.append(f"\n**Overall Risk Score:** {threat_model.get('overall_risk_score', 'N/A')}/10\n")

    lines.append("## Trust Boundaries\n")
    for boundary in threat_model.get("trust_boundaries", []):
        lines.append(f"- {boundary}")

    lines.append("\n## STRIDE Analysis\n")

    for category, data in threat_model.get("stride", {}).items():
        title = category.replace("_", " ").title()
        lines.append(f"### {title} — Risk: {data.get('risk', 'N/A')}\n")

        lines.append("**Threats:**")
        for t in data.get("threats", []):
            lines.append(f"- {t}")

        lines.append("\n**Mitigations:**")
        for m in data.get("mitigations", []):
            lines.append(f"- {m}")

        lines.append("")

    lines.append("## ⚡ Top 3 Immediate Actions\n")
    for i, action in enumerate(threat_model.get("top_3_actions", []), 1):
        lines.append(f"{i}. {action}")

    markdown_content = "\n".join(lines)

    # Save to outputs/ folder
    output_path = Path("outputs") / f"threat_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    console.print(f"\n[green]Markdown saved to: {output_path}[/green]")
    return markdown_content


# ─────────────────────────────────────────
# OUTPUT 3 — PDF report
# ─────────────────────────────────────────

def render_pdf(threat_model: dict):
    """Generates a professional PDF report in outputs/"""

    output_path = Path("outputs") / f"threat_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output_path.parent.mkdir(exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = getSampleStyleSheet()
    story  = []

    # Title
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=20,
        textColor=colors.HexColor("#1B2A4A"),
        spaceAfter=6
    )
    story.append(Paragraph(
        f"Threat Model: {threat_model.get('system_name', 'Unknown')}",
        title_style
    ))

    # Risk score
    story.append(Paragraph(
        f"Overall Risk Score: {threat_model.get('overall_risk_score', 'N/A')}/10  |  "
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 0.2*inch))

    # Trust boundaries
    story.append(Paragraph("Trust Boundaries", styles["Heading2"]))
    for boundary in threat_model.get("trust_boundaries", []):
        story.append(Paragraph(f"• {boundary}", styles["Normal"]))
    story.append(Spacer(1, 0.2*inch))

    # STRIDE table
    story.append(Paragraph("STRIDE Analysis", styles["Heading2"]))
    story.append(Spacer(1, 0.1*inch))

    table_data = [["Category", "Risk", "Top Threat", "Top Mitigation"]]

    risk_color_map = {
        "Critical": colors.HexColor("#DC2626"),
        "High":     colors.HexColor("#EA580C"),
        "Medium":   colors.HexColor("#CA8A04"),
        "Low":      colors.HexColor("#16A34A"),
    }

    for category, data in threat_model.get("stride", {}).items():
        threats     = data.get("threats", ["N/A"])
        mitigations = data.get("mitigations", ["N/A"])
        table_data.append([
            category.replace("_", " ").title(),
            data.get("risk", "N/A"),
            threats[0][:60] + "..." if len(threats[0]) > 60 else threats[0],
            mitigations[0][:60] + "..." if len(mitigations[0]) > 60 else mitigations[0],
        ])

    rl_table = RLTable(table_data, colWidths=[1.2*inch, 0.8*inch, 2.5*inch, 2.5*inch])
    rl_table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  colors.HexColor("#1B2A4A")),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0),  10),
        ("FONTSIZE",    (0, 1), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F9FAFB"), colors.white]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
        ("PADDING",     (0, 0), (-1, -1), 6),
    ]))
    story.append(rl_table)
    story.append(Spacer(1, 0.2*inch))

    # Top 3 actions
    story.append(Paragraph("⚡ Top 3 Immediate Actions", styles["Heading2"]))
    for i, action in enumerate(threat_model.get("top_3_actions", []), 1):
        story.append(Paragraph(f"{i}. {action}", styles["Normal"]))

    doc.build(story)
    console.print(f"\n[green]PDF saved to: {output_path}[/green]")