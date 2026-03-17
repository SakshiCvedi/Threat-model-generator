import typer
from rich.console import Console
from app.parser import parse_input
from app.analyzer import generate_threat_model
from app.renderer import render_terminal, render_markdown, render_pdf

# Create the typer app and rich console
cli = typer.Typer()
console = Console()


@cli.command()
def analyze(
    source: str = typer.Argument(
        ...,
        help="Path to README/architecture file OR raw text description"
    ),
    output: str = typer.Option(
        "terminal",
        "--output", "-o",
        help="Output format: terminal | markdown | pdf | all"
    ),
    save: bool = typer.Option(
        False,
        "--save", "-s",
        help="Save output to outputs/ folder (for terminal output)"
    )
):
    """
    Automated Threat Model Generator

    Analyzes your architecture and generates a STRIDE-based threat model.

    Examples:

        py app/main.py README.md

        py app/main.py README.md --output pdf

        py app/main.py README.md --output all

        py app/main.py "Flask app with JWT and PostgreSQL" --output terminal
    """

    # ── Step 1: Parse input ──────────────────────────
    console.print("\n[bold blue]Step 1/3:[/bold blue] Parsing input...")

    try:
        parsed = parse_input(source)
        console.print(f"[green]✓[/green] Input type: [cyan]{parsed['type']}[/cyan]")
        console.print(f"[green]✓[/green] Source: [cyan]{parsed['source']}[/cyan]")
    except Exception as e:
        console.print(f"[red]✗ Failed to parse input: {e}[/red]")
        raise typer.Exit(code=1)

    # ── Step 2: Generate threat model ────────────────
    console.print("\n[bold blue]Step 2/3:[/bold blue] Generating threat model...")

    try:
        threat_model = generate_threat_model(parsed)
        console.print(f"[green]✓[/green] Threat model generated successfully")
        console.print(
            f"[green]✓[/green] Risk score: "
            f"[bold red]{threat_model.get('overall_risk_score', 'N/A')}/10[/bold red]"
        )
    except Exception as e:
        console.print(f"[red]✗ Failed to generate threat model: {e}[/red]")
        raise typer.Exit(code=1)

    # ── Step 3: Render output ────────────────────────
    console.print(f"\n[bold blue]Step 3/3:[/bold blue] Rendering output as [cyan]{output}[/cyan]...\n")

    try:
        if output == "terminal":
            render_terminal(threat_model)

        elif output == "markdown":
            render_markdown(threat_model)

        elif output == "pdf":
            render_pdf(threat_model)

        elif output == "all":
            # Generate all 3 formats at once
            console.print("[dim]Rendering terminal...[/dim]")
            render_terminal(threat_model)

            console.print("[dim]Saving markdown...[/dim]")
            render_markdown(threat_model)

            console.print("[dim]Saving PDF...[/dim]")
            render_pdf(threat_model)

        else:
            console.print(
                f"[red]✗ Unknown output format: '{output}'[/red]\n"
                f"[yellow]Valid options: terminal | markdown | pdf | all[/yellow]"
            )
            raise typer.Exit(code=1)

        console.print("\n[bold green]✓ Done![/bold green]\n")

    except Exception as e:
        console.print(f"[red]✗ Failed to render output: {e}[/red]")
        raise typer.Exit(code=1)


# This allows running as: py app/main.py
if __name__ == "__main__":
    cli()