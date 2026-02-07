import shutil
from pathlib import Path
from src.services.github import github_service

def test_clone_subdirectory():
    # URL from user request
    url = "https://github.com/ComposioHQ/awesome-claude-skills/tree/master/activecampaign-automation"
    
    print(f"Cloning {url}...")
    try:
        path = github_service.clone_repository(url)
        print(f"Cloned path: {path}")
        
        assert path.exists()
        assert path.is_dir()
        # Check if it's the correct subdirectory
        assert path.name == "activecampaign-automation"
        assert (path / "skill.yaml").exists() or (path.parent / "README.md").exists()
        
        print("Verification successful!")
        
        # Cleanup
        github_service.cleanup(path)
        print("Cleanup successful!")
        
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    test_clone_subdirectory()
