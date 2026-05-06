# Kubernetes AI Agent

A small Litestar web app for learning how an AI assistant can troubleshoot Kubernetes issues. The app collects Kubernetes context, sends it to an Ollama model with a focused troubleshooting prompt, and returns a simple root-cause analysis with suggested next commands.

The project is intentionally mock-first so you can learn the AI workflow before connecting it to a live cluster.

## Features

- Litestar web UI for submitting Kubernetes issues.
- JSON API endpoint at `POST /analyze`.
- Mock Kubernetes tool output for safe local learning.
- Optional real `kubectl` command integration.
- Ollama-backed local model analysis.
- Prompt designed for beginner-friendly Kubernetes troubleshooting.

## Project Structure

```text
.
|-- app/
|   |-- agent.py                 # Collects context and calls Ollama
|   |-- main.py                  # Litestar routes and app setup
|   |-- prompts.py               # System prompt for the AI assistant
|   |-- schemas.py               # Request and response dataclasses
|   |-- templates/index.html     # Simple browser UI
|   `-- tools/
|       |-- kubectl_tools.py     # Real kubectl command wrappers
|       `-- mock_tools.py        # Safe sample Kubernetes outputs
|-- docs/
|   |-- README.md
|   |-- ai-learning-path.md
|   `-- architecture.md
|-- pyproject.toml
|-- requirements.txt
`-- README.md
```

## How It Works

1. A user submits an issue and namespace from the web page.
2. `app/main.py` receives the request at `POST /analyze`.
3. `app/agent.py` collects Kubernetes context from mock tools or `kubectl`.
4. The collected context is combined with `SYSTEM_PROMPT`.
5. Ollama runs the configured model and returns troubleshooting guidance.
6. The web UI displays the model response.

## Setup

```bash
git clone <your-repo-url>
cd k8s-ai-agent
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

If you prefer `requirements.txt`, install the listed web dependencies and make sure the Ollama Python package is also available:

```bash
pip install -r requirements.txt ollama
```

## Ollama Setup

Install and start Ollama, then pull the default model:

```bash
ollama pull llama3.2
```

The app uses `llama3.2` unless you override it with `OLLAMA_MODEL`.

## Environment Variables

Create a `.env` file in the project root:

```env
USE_MOCK_TOOLS=true
OLLAMA_MODEL=llama3.2
```

Set `USE_MOCK_TOOLS=false` only when you have `kubectl` installed, a working Kubernetes context, and permission to inspect the target namespace.

## Run The App

```bash
litestar --app app.main:app run --reload
```

Open the local URL printed by Litestar, then submit an issue such as:

```text
backend pod is CrashLoopBackOff
```

## API Example

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"issue":"backend pod is CrashLoopBackOff","namespace":"k8s-learning"}'
```

## Learning Path

Start here if your goal is to learn how AI agents work in Kubernetes troubleshooting:

- [Docs overview](docs/README.md)
- [AI learning path](docs/ai-learning-path.md)
- [Architecture notes](docs/architecture.md)

Recommended order:

1. Run the app with mock tools.
2. Read the prompt in `app/prompts.py`.
3. Trace the request flow from `app/main.py` to `app/agent.py`.
4. Modify mock outputs and observe how the AI response changes.
5. Switch to real `kubectl` only after the mock workflow is clear.

## Safety Notes

- Keep `USE_MOCK_TOOLS=true` while learning.
- Treat real `kubectl` access as read-only for this project.
- Do not add destructive commands to the tool layer without explicit guardrails.
- Review model suggestions before running any command in a cluster.
