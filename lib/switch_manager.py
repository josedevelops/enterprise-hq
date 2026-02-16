from jinja2 import Template
from scrapli import Scrapli
from .utils import is_reachable


class SwitchManager:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

        self.conn_params = {
            "host": self.host,
            "auth_username": self.username,
            "auth_password": self.password,
            "platform": "nokia_srlinux",
            "auth_strict_key": False,
            "transport": "system"
        }

    def test_connection(self):
        """
        Validates that the device is on the network.
        """
        if is_reachable(self.host):
            return True
        return False

    def get_version(self):
        """
        SSH Test: Connects to the device and retrieves OS version.
        This confirms SSH reachability AND Credentials are correct. 
        """
        try:
            with Scrapli(**self.conn_params) as conn:
                response = conn.send_command("show version")
                return response.result
        except Exception as e:
            return f"SSH Error: {e}"

    def deploy_config(self, template_path, context):
        """
        Renders a Jinja2 template with dynamic context and pushes it
        to the device using a Scrapli configuration session.
        """
        # Load and render Blueprint
        with open(template_path, "r") as f:
            t = Template(f.read())

        # This turns the template into a list of raw CLI commands
        commands = t.render(context).splitlines()

        # Push to Hardware
        try:
            with Scrapli(**self.conn_params) as conn:
                print("\n[DEBUG] Sending individuals comamnds:\n")
                for cmd in commands:
                    print(f">>> {cmd}")
                    r = conn.send_command(cmd)
                    print(r.result)

                return r
        except Exception as e:
            return f"Deployment Error: {e}"
