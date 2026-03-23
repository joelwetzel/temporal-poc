# Temporal POC — Order Processing Workflow

This documentation assumes you are on macOS.

A minimal proof-of-concept demonstrating [Temporal](https://temporal.io), a durable execution platform for building reliable distributed systems.

## What is Temporal?

Temporal lets you write long-running, fault-tolerant business logic as ordinary code. Instead of managing retries, timeouts, and state yourself, Temporal handles all of that for you.

A few core concepts used in this POC:

| Concept | Description |
|---|---|
| **Workflow** | The orchestration logic — defines the sequence of steps. Workflows are durable: they survive worker crashes and server restarts. |
| **Activity** | A single unit of work (an API call, a database write, etc.). Activities are retried automatically on failure. |
| **Worker** | A process you run that executes Workflows and Activities. Workers poll a Task Queue for work. |
| **Task Queue** | A named queue that routes work from the Temporal server to the right Workers. |
| **Temporal Server** | The durable backend that persists workflow state and coordinates execution. |

### This POC

A simple order processing workflow with three activities executed in sequence:

```
validate_order → charge_payment → send_confirmation
```

All activity implementations are stubs — the point is to see the orchestration pattern in action.

---

## Prerequisites

- **Python 3.11+** with [uv](https://docs.astral.sh/uv/) (`brew install uv`)
- **Temporal CLI** (`brew install temporal`)

---

## Setup

```bash
uv sync
```

This creates a virtual environment and installs `temporalio`.

uv is a more modern way to create virtual environments than the older 'python -m venv venv' method.  uv reads the requirements from the pyproject.toml file.

---

## Running the POC

You'll need three terminal windows.

### Terminal 1 — Start the Temporal dev server

```bash
temporal server start-dev
```

This starts a local Temporal server with an in-memory store. The web UI is available at **http://localhost:8233**.

### Terminal 2 — Start the Worker

```bash
uv run worker.py
```

The worker connects to the server and begins polling the `order-processing` task queue. You'll see activity logs here as the workflow executes.

### Terminal 3 — Run the Workflow

```bash
uv run starter.py
```

This starts a single workflow execution (`order-ORD-001`) and waits for it to complete, then prints the result.

---

## What to look for

### Worker logs (Terminal 2)

As each activity runs, you'll see log output like:

```
INFO  Validating order ORD-001
INFO  Charging $99.99 for order ORD-001
INFO  Payment successful — transaction ID: TXN-A3F2B1C9
INFO  Sending confirmation for order ORD-001 (transaction TXN-A3F2B1C9)
INFO  Confirmation sent.
```

### Starter output (Terminal 3)

Once the workflow completes:

```
Workflow completed:
  order_id: ORD-001
  customer: Jane Doe
  amount: 99.99
  transaction_id: TXN-A3F2B1C9
  status: completed
```

### Temporal UI (http://localhost:8233)

1. Open **http://localhost:8233** in a browser
2. Click on the **default** namespace
3. You'll see the `order-ORD-001` workflow in the list — click it
4. The **Event History** tab shows every step Temporal recorded: workflow started, activities scheduled/started/completed, and the final workflow completion with the return value
5. Each activity shows its input arguments and return value

The event history is the key insight: this is exactly what Temporal would use to reconstruct workflow state after a crash.

---

## Project Structure

```
temporal-pocs/
├── pyproject.toml               # dependencies
├── worker.py                    # starts the worker process
├── starter.py                   # triggers a workflow execution
├── workflows/
│   └── order_workflow.py        # OrderWorkflow — orchestration logic
└── activities/
    └── order_activities.py      # validate_order, charge_payment, send_confirmation
```
