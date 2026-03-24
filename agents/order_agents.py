from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.durable_exec.temporal import TemporalAgent

from tools.order_tools import calculate_shipping_cost

# Important for Temporal:
# 1) put the MCP server on the base agent at construction time
# 2) give the MCP server a stable id
fetch_server = MCPServerStdio(
    command="uvx",
    args=["mcp-server-time"],
    id="time-mcp",
    timeout=10,
)

model = OpenAIChatModel(
        "Qwen/Qwen3-Coder-30B-A3B-Instruct",
        provider=OpenAIProvider(
            base_url="https://router.huggingface.co/v1",
            api_key="PUT API KEY HERE",
        ),
    )

agent = Agent(
    model,
    name="order_summarizer",
    instructions=(
        "Summarize the order from the details. "
        "Use the calculate_shipping_cost tool to compute the estimated shipping cost "
        "and include it in your summary. "
        "Add a timestamp to your summary."
    ),
    tools=[calculate_shipping_cost],
    toolsets=[fetch_server],
)

temporal_agent = TemporalAgent(agent)