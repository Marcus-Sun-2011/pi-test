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
from src.core.exceptions import ValidationError, SecurityBlockError

app = typer.Typer(help="Local Agent Studio CLI - Connect local LLMs with tools.")

@app.command("chat")
def chat():
    """Start an interactive multi-turn chat session with the agent."""
    rprint("[bold green]Local Agent Studio Interactive Chat[/bold green]")
    rprint("Type 'exit', 'quit', or press Ctrl+C to exit.\n")
    
    # Enhanced health check on start
    if not client.check_health():
        rprint("[bold red]Critical Connection Error:[/bold red] Could not connect to LM Studio at http://localhost:1234/v1.")
        rprint("Please ensure LM Studio is running and the local API server is active.")
        return

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                rprint("[bold blue]Goodbye![/bold blue]")
                break
            
            # Visual feedback for the agent's thinking process
            rprint("[italic,dim]Agent is processing...[/italic,dim]")
            response = engine.run(user_input)
            rprint(f"\n[bold cyan]Assistant:[/bold cyan] {response}")
        except (KeyboardInterrupt, EOFError):
            rprint("\n[bold blue]Goodbye![/bold blue]")
            break
        except ValidationError as ve:
            rprint(f"[bold yellow]Input Warning:[/bold yellow] The request was invalid. Please check your input parameters.")
            rprint(f"Detail: {ve}")
        except SecurityBlockError as sbe:
            rprint(f"[bold red]Security Alert:[/bold red] This specific action is restricted by the safety guard.")
            rprint(f"Reason: {sbe}")
        except Exception as e:
            rprint(f"[bold red]System Error:[/bold red] {type(e).__name__}: {e}")
            logger.exception("Unexpected error in main chat loop")

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
