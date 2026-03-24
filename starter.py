import asyncio
from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter

from workflows.order_workflow import OrderWorkflow

TASK_QUEUE = "order-processing"


async def main():
    client = await Client.connect("localhost:7233", data_converter=pydantic_data_converter)

    result = await client.execute_workflow(
        OrderWorkflow.run,
        args=["ORD-001", 99.99],
        id="order-ORD-001",
        task_queue=TASK_QUEUE,
    )

    print("Workflow completed:")
    for key, value in result.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
