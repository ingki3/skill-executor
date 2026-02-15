import sys
import io
import contextlib
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def run(args: dict) -> dict:
    """
    Execute a snippet of Python code and return the output.
    Expects 'code' in args.
    """
    code = args.get("code")
    if not code:
        return {"error": "Missing 'code' parameter"}

    stdout = io.StringIO()
    stderr = io.StringIO()

    try:
        # Caution: This is executing untrusted code in the same process.
        # Per spec, we treat internal tools as trusted for now.
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            # Using a shared global/local dict for execution
            exec_globals = {}
            exec(code, exec_globals)
            
        return {
            "stdout": stdout.getvalue(),
            "stderr": stderr.getvalue(),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Code execution error: {e}")
        return {
            "stdout": stdout.getvalue(),
            "stderr": stderr.getvalue(),
            "status": "error",
            "error": str(e)
        }
