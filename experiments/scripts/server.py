# server.py
# Class definition for `NoisePageServer` used in JUnit tests.

import time
import subprocess

# -----------------------------------------------------------------------------
# NoisePageServer


class NoisePageServer:
    """
    NoisePageServer represents a NoisePage DBMS instance.
    """

    def __init__(self, binary_path: str, host: str, port: str):
        """
        Initialize a new DBMS server instance.
        :param binary_path The path to the NoisePage binary
        :param host The host on which to run the server
        :param port The port on which to run the server
        """
        self.binary_path = binary_path
        self.db_host = host
        self.db_port = port
        self.db_process = None

    def start(self):
        """
        Start the NoisePage server instance.
        """
        db_process = subprocess.Popen(
            [f"{self.binary_path}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        check_line = f"NoisePage - Self-Driving Database Management System [port={self.db_port}] [PID={db_process.pid}]"

        while True:
            log_line = db_process.stdout.readline().decode("utf-8").rstrip("\n")
            if log_line.endswith(check_line):
                self.db_process = db_process
                break
            time.sleep(1.0)

    def stop(self):
        """
        Stop the NoisePage server instance.
        """
        if self.db_process is None:
            raise RuntimeError("System is in an invalid state.")

        # Check if the DBMS is still running.
        return_code = self.db_process.poll()
        if return_code is not None:
            raise RuntimeError(
                f"DBMS already terminated, code: {self.db_process.returncode}"
            )

        try:
            # Try to kill the process politely and wait for 60 seconds
            self.db_process.terminate()
            self.db_process.wait(60)
        except subprocess.TimeoutExpired:
            # Otherwise, try to kill the process forcefully and wait another 60 seconds
            self.db_process.kill()
            self.db_process.wait(60)
        except KeyboardInterrupt:
            raise KeyboardInterrupt

        return self.db_process.returncode
