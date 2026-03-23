import uuid
from temporalio import activity


@activity.defn
async def validate_order(order_id: str) -> dict:
    activity.logger.info(f"Validating order {order_id}")
    # Stub: simulate validation logic
    return {"order_id": order_id, "customer": "Jane Doe", "amount": 99.99, "valid": True}


@activity.defn
async def charge_payment(order_id: str, amount: float) -> str:
    activity.logger.info(f"Charging ${amount:.2f} for order {order_id}")
    # Stub: simulate payment processing
    transaction_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
    activity.logger.info(f"Payment successful — transaction ID: {transaction_id}")
    return transaction_id


@activity.defn
async def send_confirmation(order_id: str, transaction_id: str) -> None:
    activity.logger.info(
        f"Sending confirmation for order {order_id} (transaction {transaction_id})"
    )
    # Stub: simulate email/notification dispatch
    activity.logger.info("Confirmation sent.")
