import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import typer
from rich import print as rprint
from src.agent.engine import engine
from src.agent.model_client import client
from src.tools.registry import registry
from src.utils.logger import logger

app = typer.Typer(help="Local Agent Studio CLI - Connect local LLMs with tools.")

@app.command("chat")
def chat():
    """Start an interactive multi-turn chat session with the agent."""
    rprint("[bold green]Local Agent Studio Interactive Chat[/bold green]")
    rprint("Type 'exit', 'quit', or press Ctrl+C to exit.\n")
    
    # Optional health check on start
    if not client.check_health():
        rprint("[bold yellow]Warning: Could not connect to LM Studio at http://localhost:1234/v1. Ensure LM Studio is running.[/bold yellow]")

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                rprint("[bold blue]Goodbye![/bold blue]")
                break
            
            rprint("[dim]Thinking...[/dim]")
            response = engine.run(user_input)
            rprint(f"\n[bold cyan]Assistant:[/bold cyan] {response}")
        except (KeyboardInterrupt, EOFError):
            rprint("\n[bold blue]Goodbye![/bold blue]")
            break
        except Exception as e:
            rprint(f"[bold red]Error:[/bold red] {e}")
            logger.exception("Error in chat loop")

@app.command("health")
def health():
    """Check connection health with LM Studio."""
    rprint("[bold]Checking LM Studio connection...[/bold]")
    if client.check_health():
        rprint("[bold green]Connection successful![/bold green]")
    else:
        rprint("[bold red]Connection failed. Please check your settings and ensure LM Studio is running.[/bold red]")

@app.command("tools")
def list_tools():
    """List all registered tools in the registry."""
    tools = registry.get_all_tools()
    rprint(f"[bold]Registered Tools ({len(tools)}):[/bold]")
    for tool in tools:
        rprint(f"  - [cyan]{tool.name}[/cyan]: {tool.description}")

if __name__ == "__main__":
    app()
