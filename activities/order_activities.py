import uuid
import asyncio
from temporalio import activity

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from tools.order_tools import calculate_shipping_cost

@activity.defn
async def validate_order(order_id: str) -> dict:
    activity.logger.info(f"Validating order {order_id}")
    # Stub: simulate validation logic
    return {"order_id": order_id, "customer": "Jane Doe", "amount": 99.99, "valid": True}


@activity.defn
async def summarize_order(order_details: dict) -> str:
    activity.logger.info("Summarizing order")

    model = OpenAIChatModel(
        "Qwen/Qwen3-Coder-30B-A3B-Instruct",
        provider=OpenAIProvider(
            base_url="https://router.huggingface.co/v1",
            api_key="PUT API KEY HERE",
        ),
    )
    agent = Agent(
        model,
        instructions=(
            "Summarize the order from the details. "
            "Use the calculate_shipping_cost tool to compute the estimated shipping cost "
            "and include it in your summary."
        ),
        tools=[calculate_shipping_cost],
    )
    result = await agent.run(str(order_details))
    return result.output


@activity.defn
async def charge_payment(order_id: str, amount: float) -> str:
    activity.logger.info(f"Charging ${amount:.2f} for order {order_id}")
    # Stub: simulate payment processing
    await asyncio.sleep(2)
    transaction_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
    activity.logger.info(f"Payment successful — transaction ID: {transaction_id}")
    return transaction_id


@activity.defn
async def send_confirmation(order_id: str, transaction_id: str) -> None:
    activity.logger.info(
        f"Sending confirmation for order {order_id} (transaction {transaction_id})"
    )
    # Stub: simulate email/notification dispatch

    await asyncio.sleep(3)

    activity.logger.info("Confirmation sent.")
