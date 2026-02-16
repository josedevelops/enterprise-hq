import os
import yaml
from dotenv import load_dotenv
from lib.switch_manager import SwitchManager
from rich import print

# Environment Variables
load_dotenv()

def main():
    # Inventory Discovery
    try:
        with open ("topology.clab.yml", "r") as f:
            inventory = yaml.safe_load(f)['topology']['nodes']
    except FileNotFoundError:
        print("[red]Error: topology.clab.yml not found.[/red]")
        return

    print(f"[bold cyan] Starting Connectivity Audit for {len(inventory)} nodes....[/bold cyan]")

    # Execution Cycle
    for name, details in inventory.items():
        # Intialize the Service for this specific node
        manager = SwitchManager(
            host=details['mgmt-ipv4'],
            username=os.getenv("SWITCH_USER"),
            password=os.getenv("SWITCH_PASS")
        )

        # Connection Test
        if manager.test_connection():
            print(f"[green] {name} ({details['mgmt-ipv4']}) is reachable.[/green]")


            version_info = manager.get_version()
            if "SSH Error" in version_info:
                print(f"[red] SSH Auth Failed: {version_info}[/red]")
                continue

            print(f"[bold green] SSH Authenticated.[/bold green]")

            # Context Base 
            context = {
                "hostname": name,
                "contact": "Jose - Network Engineer",
                "location": "MDF - Rack A1"
            }

            # Deployment Action
            result = manager.deploy_config("templates/base_setup.j2", context)

            if hasattr(result, 'failed') and not result.failed:
                print(f"[bold green] Configuration committed successfully.[/bold green]")
            else:
                print(f"[red] Deployment failed: {result}[/red]")

        else:
            print(f"[red] {name} ({details['mgmt-ipv4']}) is UNREACHABLE.[/red]")
if __name__== "__main__":
    main()
