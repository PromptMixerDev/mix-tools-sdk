import os
import pytest
from httpx import AsyncClient
from mix_tools_sdk import MixToolsClient

@pytest.mark.asyncio
async def test_client_init_no_api_key():
    """Test client initialization with no API key"""
    with pytest.raises(ValueError, match="API key must be provided"):
        MixToolsClient("http://test-api")

@pytest.mark.asyncio
async def test_client_init_env_api_key():
    """Test client initialization with API key from environment"""
    os.environ["MIXTOOLS_API_KEY"] = "test-env-key"
    client = MixToolsClient("http://test-api")
    assert client.api_key == "test-env-key"
    del os.environ["MIXTOOLS_API_KEY"]

@pytest.fixture
async def client():
    """Create a test client instance"""
    async with MixToolsClient("http://test-api", api_key="test-api-key") as client:
        # Replace the httpx client with a mock
        client.client = AsyncClient(base_url="http://test-api")
        yield client

@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint"""
    async def mock_get(*args, **kwargs):
        return MockResponse({"status": "healthy"})
    client.client.get = mock_get
    result = await client.health_check()
    assert result["status"] == "healthy"

@pytest.mark.asyncio
async def test_list_tools_with_tags_string(client):
    """Test listing tools with tag filter as string"""
    mock_tools = {
        "tools": [
            {
                "name": "test_tool",
                "description": "A test tool",
                "tags": ["test"]
            }
        ]
    }
    async def mock_get(*args, **kwargs):
        assert kwargs.get("params", {}).get("tags") == "test"
        return MockResponse(mock_tools)
    client.client.get = mock_get
    result = await client.list_tools(tags="test")
    assert result["tools"][0]["tags"] == ["test"]

@pytest.mark.asyncio
async def test_list_tools_with_tags_list(client):
    """Test listing tools with tag filter as list"""
    mock_tools = {
        "tools": [
            {
                "name": "test_tool",
                "description": "A test tool",
                "tags": ["test1", "test2"]
            }
        ]
    }
    async def mock_get(*args, **kwargs):
        assert kwargs.get("params", {}).get("tags") == "test1,test2"
        return MockResponse(mock_tools)
    client.client.get = mock_get
    result = await client.list_tools(tags=["test1", "test2"])
    assert result["tools"][0]["tags"] == ["test1", "test2"]

@pytest.mark.asyncio
async def test_list_tools_with_toolkit(client):
    """Test listing tools with toolkit filter"""
    mock_tools = {
        "tools": [
            {
                "name": "test_tool",
                "description": "A test tool",
                "toolkit": "test_toolkit"
            }
        ]
    }
    async def mock_get(*args, **kwargs):
        assert kwargs.get("params", {}).get("toolkit") == "test_toolkit"
        return MockResponse(mock_tools)
    client.client.get = mock_get
    result = await client.list_tools(toolkit="test_toolkit")
    assert result["tools"][0]["toolkit"] == "test_toolkit"

@pytest.mark.asyncio
async def test_list_tools_basic(client):
    """Test listing tools"""
    mock_tools = {
        "tools": [
            {
                "name": "test_tool",
                "description": "A test tool",
                "properties": [
                    {
                        "name": "input",
                        "description": "Input value",
                        "type": "str",
                        "required": True
                    }
                ]
            }
        ]
    }
    async def mock_get(*args, **kwargs):
        return MockResponse(mock_tools)
    client.client.get = mock_get
    result = await client.list_tools()
    assert "tools" in result
    assert len(result["tools"]) == 1
    assert result["tools"][0]["name"] == "test_tool"

@pytest.mark.asyncio
async def test_list_tools_with_format(client):
    """Test listing tools with specific format"""
    mock_tools = {
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "test_tool",
                    "description": "A test tool",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "input": {
                                "type": "string",
                                "description": "Input value"
                            }
                        },
                        "required": ["input"]
                    }
                }
            }
        ]
    }
    async def mock_get(*args, **kwargs):
        return MockResponse(mock_tools)
    client.client.get = mock_get
    result = await client.list_tools(format="openai")
    assert "tools" in result
    assert len(result["tools"]) == 1
    assert result["tools"][0]["type"] == "function"

@pytest.mark.asyncio
async def test_execute_tool_with_format(client):
    """Test tool execution with format"""
    mock_result = {
        "result": {
            "output": "TEST RESULT"
        }
    }
    async def mock_post(*args, **kwargs):
        assert kwargs.get("params", {}).get("format") == "openai"
        return MockResponse(mock_result)
    client.client.post = mock_post
    result = await client.execute_tool(
        "test_tool",
        {"input": "test"},
        format="openai"
    )
    assert result["result"]["output"] == "TEST RESULT"

@pytest.mark.asyncio
async def test_execute_tool_with_tool_call_id(client):
    """Test tool execution with tool call ID"""
    mock_result = {
        "result": {
            "output": "TEST RESULT"
        }
    }
    async def mock_post(*args, **kwargs):
        assert kwargs.get("params", {}).get("tool_call_id") == "test-id"
        return MockResponse(mock_result)
    client.client.post = mock_post
    result = await client.execute_tool(
        "test_tool",
        {"input": "test"},
        tool_call_id="test-id"
    )
    assert result["result"]["output"] == "TEST RESULT"

@pytest.mark.asyncio
async def test_execute_tool_basic(client):
    """Test tool execution"""
    mock_result = {
        "result": {
            "output": "TEST RESULT"
        }
    }
    async def mock_post(*args, **kwargs):
        return MockResponse(mock_result)
    client.client.post = mock_post
    result = await client.execute_tool(
        "test_tool",
        {"input": "test"}
    )
    assert "result" in result
    assert result["result"]["output"] == "TEST RESULT"

class MockResponse:
    """Mock HTTP response"""
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data

    def raise_for_status(self):
        pass
