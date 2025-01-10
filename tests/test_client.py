import pytest
from httpx import AsyncClient
from mix_tools_sdk import MixToolsClient

@pytest.fixture
async def client():
    """Create a test client instance"""
    async with MixToolsClient("http://test-api") as client:
        # Replace the httpx client with a mock
        client.client = AsyncClient(base_url="http://test-api")
        yield client

@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint"""
    client.client.get = lambda *args, **kwargs: MockResponse({"status": "healthy"})
    result = await client.health_check()
    assert result["status"] == "healthy"

@pytest.mark.asyncio
async def test_list_tools(client):
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
    client.client.get = lambda *args, **kwargs: MockResponse(mock_tools)
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
    client.client.get = lambda *args, format="openai", **kwargs: MockResponse(mock_tools)
    result = await client.list_tools(format="openai")
    assert "tools" in result
    assert len(result["tools"]) == 1
    assert result["tools"][0]["type"] == "function"

@pytest.mark.asyncio
async def test_execute_tool(client):
    """Test tool execution"""
    mock_result = {
        "result": {
            "output": "TEST RESULT"
        }
    }
    client.client.post = lambda *args, **kwargs: MockResponse(mock_result)
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
