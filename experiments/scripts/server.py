# server.py
# Class definition for `NoisePageServer` used in JUnit tests.

import os
import time
import subprocess
from enum import Enum

# -----------------------------------------------------------------------------
# NoisePageServer

class ExecutionMode(Enum):
    """ExecutionMode enumerates supported NoisePage execution modes."""
    INTERPRETED = 0
    COMPILED = 1

class NoisePageServer:
    """NoisePageServer represents a NoisePage DBMS instance."""

    def __init__(self, path: str, host: str, port: str, execution_mode: ExecutionMode):
        """
        Initialize a new DBMS server instance.
        :param binary_path The path to the NoisePage binary
        :param host The host on which to run the server
        :param port The port on which to run the server
        """
        self.path = path
        self.binary_path = os.path.join(path, "noisepage")
        self.db_host = host
        self.db_port = port
        self.execution_mode = execution_mode
        self.db_process = None

    def start(self):
        """Start the NoisePage server instance."""
        # Provide the compiled query execution argument, if applicable
        arguments = self.construct_arguments()
        db_process = subprocess.Popen(
            [f"{self.binary_path}{arguments}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        check_line = f"NoisePage - Self-Driving Database Management System [port={self.db_port}] [PID={db_process.pid}]"

        while True:
            log_line = db_process.stdout.readline().decode("utf-8").rstrip("\n")
            if log_line.endswith(check_line):
                self.db_process = db_process
                break
            time.sleep(1.0)

    def stop(self):
        """Stop the NoisePage server instance."""
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

    def construct_arguments(self):
        """Construct the program arguments from options passed to NoisePageServer."""
        if self.execution_mode == ExecutionMode.INTERPRETED:
            return ""
        # Execution mode is compiled
        bytecode_path = os.path.join(self.path, "bytecode_handlers_ir.bc")
        return f" --compiled_query_execution=true --bytecode_handlers_path={bytecode_path}"

