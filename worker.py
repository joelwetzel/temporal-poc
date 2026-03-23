import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker

from workflows.order_workflow import OrderWorkflow
from activities.order_activities import validate_order, charge_payment, send_confirmation

TASK_QUEUE = "order-processing"


async def main():
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[OrderWorkflow],
        activities=[validate_order, charge_payment, send_confirmation],
    )

    print(f"Worker started on task queue '{TASK_QUEUE}'. Press Ctrl+C to stop.")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
