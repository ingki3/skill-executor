
import pytest
import time
from src.core.prompt_loader import PromptLoader, prompt_loader
from pathlib import Path

def test_prompt_loader_basic(tmp_path):
    # Setup mock prompt file
    prompt_dir = tmp_path / "prompt"
    prompt_dir.mkdir()
    security_yaml = prompt_dir / "security.yaml"
    security_yaml.write_text("risk_scan: 'Analyze this: {code}'")

    loader = PromptLoader(prompt_dir=str(prompt_dir))
    
    # Test retrieval
    template = loader.get("security", "risk_scan")
    assert template == "Analyze this: {code}"
    
    # Test formatting
    formatted = template.format(code="print('hi')")
    assert formatted == "Analyze this: print('hi')"

def test_prompt_loader_missing_key(tmp_path):
    prompt_dir = tmp_path / "prompt"
    prompt_dir.mkdir()
    (prompt_dir / "test.yaml").write_text("key1: val1")
    
    loader = PromptLoader(prompt_dir=str(prompt_dir))
    assert "[test:missing]" in loader.get("test", "missing")

def test_prompt_loader_performance(tmp_path):
    prompt_dir = tmp_path / "prompt"
    prompt_dir.mkdir()
    (prompt_dir / "perf.yaml").write_text("fast: 'speed'")
    
    loader = PromptLoader(prompt_dir=str(prompt_dir))
    
    # First load (disk)
    start = time.perf_counter()
    loader.get("perf", "fast")
    disk_time = time.perf_counter() - start
    
    # Second load (cache)
    start = time.perf_counter()
    loader.get("perf", "fast")
    cache_time = time.perf_counter() - start
    
    print(f"Disk time: {disk_time:.6f}s, Cache time: {cache_time:.6f}s")
    # Cache should be significantly faster, and sub-millisecond
    assert cache_time < 0.001
    assert cache_time < disk_time

def test_prompt_loader_reload(tmp_path):
    prompt_dir = tmp_path / "prompt"
    prompt_dir.mkdir()
    file = prompt_dir / "change.yaml"
    file.write_text("msg: 'old'")
    
    loader = PromptLoader(prompt_dir=str(prompt_dir))
    assert loader.get("change", "msg") == "old"
    
    # Change file
    file.write_text("msg: 'new'")
    # Should still be old due to cache
    assert loader.get("change", "msg") == "old"
    
    # Reload
    loader.reload()
    assert loader.get("change", "msg") == "new"
