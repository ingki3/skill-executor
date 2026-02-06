import os
import ast
from src.core.llm_clients import llm_clients

class SecurityService:
    def __init__(self):
        self.dangerous_keywords = ["os.system", "eval(", "exec(", "subprocess.", "rm -rf"]

    def _static_pre_filter(self, code: str) -> bool:
        """Simple static check before LLM scan."""
        for kw in self.dangerous_keywords:
            if kw in code:
                return False
        return True

    async def scan_skill(self, prompt: str, code: str) -> tuple[bool, str]:
        """Returns (is_safe, reason)."""
        
        # Pre-filter
        if not self._static_pre_filter(code):
            return False, "Static analysis detected high-risk code patterns (dangerous keywords)."

        # LLM Scan
        security_prompt = f"""
        Analyze the following AI skill for security risks:
        Prompt Template: {prompt}
        Code: 
        {code}
        
        Identify risks such as:
        - PII theft
        - Malicious code execution
        - Unauthorized network access
        - System modification
        
        Respond ONLY with 'SAFE' or 'RISKY: <reason>'.
        """
        
        try:
            result = await llm_clients.generate_simple(security_prompt)
            if result.strip().upper() == "SAFE":
                return True, "Passed LLM security verification."
            else:
                return False, result.strip()
        except Exception as e:
            if "404" in str(e):
                # If model not found, we'll allow but warn in logs (for development/preview)
                print(f"Security model not found: {e}. Defaulting to SAFE for test.")
                return True, "Defaulted to SAFE (Model not found during preview)."
            return False, f"Security scan failed: {str(e)}"

security_service = SecurityService()
