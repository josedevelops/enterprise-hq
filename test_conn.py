import os
from dotenv import load_dotenv
from scrapli import Scrapli
from rich import print 


load_dotenv()

# Senior Tip: Using the 'generic' or 'nokia_srlinux' platform 
# depends on the driver version. We'll use the specific Nokia one.

HOSTS = [
    "172.20.20.10",
    "172.20.20.11",
    "172.20.20.12",
    "172.20.20.13",
]

COMMON = {
        "auth_username": os.getenv("SWITCH_USER"),
        "auth_password": os.getenv("SWITCH_PASS"),
        "auth_strict_key": os.getenv("SWITCH_STRICT_KEY", "false").lower() == "true",
        "platform": os.getenv("PLATFORM"),
        "transport": os.getenv("TRANSPORT"),
}

for host in HOSTS:
    device = {**COMMON, "host": host}
    try:
        with Scrapli(**device) as conn:
            response = conn.send_command("show version")
            print(f"[green] Success![/green] Connected to [bold]{host}[/bold]")
            print(f"[yellow]Switch Output:[/yellow]\n{response.result}")
    except Exception as e:
        print(f"[red]Execution Error on {host}:[/red] {e}")



