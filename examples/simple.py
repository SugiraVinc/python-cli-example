import subprocess
import shlex
import json


# Create a function that runs subprocess and returns the output
def run_command(command):
    cmd = shlex.split(command)
    output = subprocess.check_output(cmd)
    return output


def run_lsblk(device):
    """
    Runs lsblk command and produces JSON output:

    Example output:
    {
        "blockdevices": [
            {
                "name": "vda",
                "size": "59.6G",
                "type": "disk",
                "mountpoint": null,
                "children": [
                    {
                        "name": "vda1",
                        "size": "59.6G",
                        "type": "part",
                        "mountpoint": "/etc/hosts"
                    }
                ]
            }
        ]
    }
    """
    command = "lsblk -J -o NAME,SIZE,TYPE,MOUNTPOINT"  # Removed `f` prefix
    output = run_command(command)
    devices = json.loads(output)["blockdevices"]
    for parent in devices:
        if parent["name"] == device:
            return parent
        for child in parent.get("children", []):
            if child["name"] == device:
                return child


def main(device):
    print(f"'{run_lsblk(device)}'")


if __name__ == "__main__":
    import sys

    main(sys.argv[-1])
