import httpx
import asyncio

async def verify_skills():
    """Verify registration and execution of specific skills."""
    base_url = "http://localhost:8000"
    repo_url = "https://github.com/ComposioHQ/awesome-claude-skills"
    test_paths = [
        "skills/calculator",
        "skills/weather",
        "skills/gmail",
        "skills/slack"
    ]
    
    async with httpx.AsyncClient() as client:
        # 1. Register
        print(f"Registering skills from {repo_url}...")
        resp = await client.post(f"{base_url}/skills/register-bulk", json={
            "repo_url": repo_url,
            "selected_paths": test_paths
        }, timeout=60.0)
        
        if resp.status_code != 200:
            print(f"Registration failed: {resp.text}")
            return
            
        print("Registration successful.")
        
        # 2. Verify in list
        resp = await client.get(f"{base_url}/skills")
        skills = resp.json()
        print(f"Total skills in registry: {len(skills)}")
        
        # 3. Execute each
        for path in test_paths:
            skill_name = path.split("/")[-1]
            print(f"Testing execution for {skill_name}...")
            # We use a query that matches the name for simplicity in search
            exec_resp = await client.post(f"{base_url}/skills/execute", json={
                "query": f"Use {skill_name} to do something"
            }, timeout=30.0)
            
            if exec_resp.status_code == 200:
                print(f"  Result: {exec_resp.json()['outcome']}")
            else:
                print(f"  Result: FAILED ({exec_resp.status_code})")

if __name__ == "__main__":
    asyncio.run(verify_skills())
