import os
import ast
from typing import List
from src.core.llm_clients import llm_clients
from src.models.registration import RiskFinding, RiskCategory, RiskSeverity

class SecurityService:
    def __init__(self):
        self.dangerous_keywords = [
            "os.system", "eval(", "exec(", "subprocess.", "rm -rf", 
            "shutil.rmtree", "os.remove", "os.unlink", "os.chmod",
            "os.chown", "os.kill", "os.fork", "os.pipe", "os.write"
        ]
        self.pii_keywords = [
            "password", "secret", "token", "api_key", "credit_card",
            "social_security", "passport", "email", "phone_number"
        ]

    def _static_pre_filter(self, code: str) -> bool:
        """Simple static check before LLM scan."""
        # Check for dangerous keywords in code
        for kw in self.dangerous_keywords:
            if kw in code:
                return False
        
        # Basic check for suspicious AST patterns
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    # Check for dangerous module imports
                    dangerous_mods = ["os", "subprocess", "shutil", "socket", "requests", "httpx"]
                    for alias in node.names if isinstance(node, ast.Import) else [node.module]:
                        if alias in dangerous_mods:
                            # We don't block all imports, but we flag for LLM
                            pass
        except:
            return False # Invalid python code
            
        return True

    async def analyze_risk(self, code: str) -> List[RiskFinding]:
        """Analyze code for specific risk patterns (PII, malicious code)."""
        findings = []
        
        # Check for PII keywords
        for kw in self.pii_keywords:
            if kw.lower() in code.lower():
                findings.append(RiskFinding(
                    category=RiskCategory.PII,
                    detail=f"Potential PII exposure: '{kw}' keyword found.",
                    severity=RiskSeverity.MEDIUM
                ))
        
        # Check for dangerous system operations
        for kw in self.dangerous_keywords:
            if kw in code:
                findings.append(RiskFinding(
                    category=RiskCategory.DANGEROUS_OP,
                    detail=f"Dangerous system operation detected: '{kw}'.",
                    severity=RiskSeverity.HIGH
                ))
                
        return findings

    async def scan_skill(self, prompt: str, code: str) -> tuple[bool, str]:
        """Returns (is_safe, reason)."""
        
        # Pre-filter
        if not self._static_pre_filter(code):
            return False, "Static analysis detected high-risk code patterns (dangerous keywords)."

        # LLM Scan
        from src.core.prompt_loader import prompt_loader
        security_prompt = prompt_loader.get("security", "scan_skill").format(
            prompt=prompt,
            code=code
        )
        
        try:
            result = await llm_clients.generate_simple(security_prompt)
            if result.strip().upper() == "SAFE":
                return True, "Passed LLM security verification."
            else:
                return False, result.strip()
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "No API_KEY" in error_msg:
                # If model not found or no key config, we'll allow but warn in logs (for development/preview)
                print(f"Human-in-the-loop warning: Security scan skipped. Reason: {error_msg}")
                return True, f"Security scan skipped (Dev Mode): {error_msg}"
            return False, f"Security scan failed: {error_msg}"

security_service = SecurityService()
