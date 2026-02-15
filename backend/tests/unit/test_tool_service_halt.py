import pytest
import json
import os
from pathlib import Path
from src.services.tool_service import ToolService
from src.models.tool import ToolType

@pytest.fixture
def service_factory(tmp_path):
    def _create_service(name):
        config_file = tmp_path / f"tools_{name}.json"
        mcp_file = tmp_path / f"mcp_{name}.json"
        
        # Initialize empty files
        with open(mcp_file, "w") as f:
            json.dump({"mcp_servers": {}}, f)
            
        service = ToolService(tools_config_path=str(config_file), mcp_config_path=str(mcp_file))
        service.tools_config_path = Path(config_file)
        service.mcp_config_path = Path(mcp_file)
        service.reset_for_test()
        return service, config_file
    return _create_service

@pytest.mark.asyncio
async def test_halt_on_malformed_json(service_factory):
    service_obj, config_file = service_factory("malformed")
    with open(config_file, "w") as f:
        f.write("{ invalid json")
    
    with pytest.raises(SystemExit) as excinfo:
        await service_obj.load_registry()
    # Check for the start of our error message
    assert "Halt: Registry failure" in str(excinfo.value)

@pytest.mark.asyncio
async def test_halt_on_schema_violation(service_factory):
    service_obj, config_file = service_factory("schema")
    data = {
        "tools": [
            {
                "name": "bad_tool",
                "description": "missing type",
                "input_schema": {}
            }
        ]
    }
    with open(config_file, "w") as f:
        json.dump(data, f)
    
    with pytest.raises(SystemExit) as excinfo:
        await service_obj.load_registry()
    assert "Halt: Registry failure" in str(excinfo.value)
