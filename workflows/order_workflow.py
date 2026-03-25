from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from pydantic_ai.durable_exec.temporal import PydanticAIWorkflow
    from activities.order_activities import validate_order, summarize_order, charge_payment, send_confirmation
    from agents.order_agents import temporal_agent

@workflow.defn
class OrderWorkflow(PydanticAIWorkflow):
    __pydantic_ai_agents__ = [temporal_agent]

    @workflow.run
    async def run(self, order_id: str, amount: float) -> dict:
        workflow.logger.info(f"Starting order workflow for {order_id}")

        order = await workflow.execute_activity(
            validate_order,
            order_id,
            start_to_close_timeout=timedelta(seconds=30),
        )

        summary = await workflow.execute_activity(
            summarize_order,
            order,
            start_to_close_timeout=timedelta(seconds=60)
        )

        # summary = (await temporal_agent.run(str(order))).output

        transaction_id = await workflow.execute_activity(
            charge_payment,
            args=[order_id, amount],
            start_to_close_timeout=timedelta(seconds=30),
        )

        await workflow.execute_activity(
            send_confirmation,
            args=[order_id, transaction_id],
            start_to_close_timeout=timedelta(seconds=60),
        )

        return {
            "order_id": order_id,
            "customer": order["customer"],
            "amount": amount,
            "transaction_id": transaction_id,
            "status": "completed",
            "summary": summary
        }
