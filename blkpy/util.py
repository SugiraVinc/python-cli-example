import subprocess
import shlex
import json


# Create a function that runs subprocess and returns the output
def run_command(command):
    """Runs a shell command and returns the output."""
    cmd = shlex.split(command)
    try:
        output = subprocess.check_output(cmd, text=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with return code {e.returncode}")
        return None


def run_lsblk(device):
    """
    Runs the lsblk command and returns JSON output for the specified device.

    Example output:
    {
        "blockdevices": [
            {"name": "vda", "size": "59.6G", "type": "disk", "mountpoint": null,
                "children": [
                    {"name": "vda1", "size": "59.6G", "type": "part",
                      "mountpoint": "/etc/hosts"}
                ]
            }
        ]
    }
    """
    command = "lsblk -J -o NAME,SIZE,TYPE,MOUNTPOINT"
    output = run_command(command)
    if output:
        devices = json.loads(output).get("blockdevices", [])
        for parent in devices:
            if parent["name"] == device:
                return parent
            for child in parent.get("children", []):
                if child["name"] == device:
                    return child  # <-- Added this return statement
    return None  # Return None if device is not found
