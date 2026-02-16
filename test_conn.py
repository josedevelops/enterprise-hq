from scrapli import Scrapli
from rich import print

# Senior Tip: Using the 'generic' or 'nokia_srlinux' platform 
# depends on the driver version. We'll use the specific Nokia one.
device = {
    "host": "172.20.20.10",
    "auth_username": "admin",
    "auth_password": "NokiaSrl1!", # If this fails, try "Nokia-Srl!"
    "auth_strict_key": False,
    "platform": "nokia_srlinux"
}

try:
    # We use the Scrapli factory to automatically pick the right driver
    with Scrapli(**device) as conn:
        response = conn.send_command("show version")
        print(f"[green]Success![/green] Connected to: [bold]{device['host']}[/bold]")
        print(f"[yellow]Switch Output:[/yellow]\n{response.result}")
except Exception as e:
    print(f"[red]Execution Error:[/red] {e}")
