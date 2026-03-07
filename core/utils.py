import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

def run_powershell(command: str) -> tuple[int, str, str]:
    """
    Runs a PowerShell command and returns the return code, stdout, and stderr.
    """
    try:
        process = subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout.strip(), stderr.strip()
    except Exception as e:
        logging.error(f"Error running PowerShell command: {e}")
        return 1, "", str(e)
