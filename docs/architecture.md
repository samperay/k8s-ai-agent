# Architecture Notes

## Runtime Flow

```text
Browser UI
  |
  v
POST /analyze
  |
  v
app.main.analyze()
  |
  v
app.agent.analyze_kubernetes_issue()
  |
  v
collect_kubernetes_context()
  |
  +-- mock_tools.py, when USE_MOCK_TOOLS=true
  |
  +-- kubectl_tools.py, when USE_MOCK_TOOLS=false
  |
  v
ollama.chat()
  |
  v
AnalyzeResponse
```

## Main Modules

`app/main.py`

Defines the Litestar application, the home page route, and the `/analyze` API route.

`app/agent.py`

Loads environment variables, chooses mock or real tools, builds the Kubernetes context, calls Ollama, and returns the model response.

`app/prompts.py`

Stores the system prompt. This is where the model is instructed to behave like a Kubernetes troubleshooting assistant and keep guidance safe for learners.

`app/schemas.py`

Defines the request and response dataclasses used by the API.

`app/tools/mock_tools.py`

Provides stable sample Kubernetes command output. This is the safest place to create new troubleshooting scenarios while learning.

`app/tools/kubectl_tools.py`

Wraps read-only `kubectl` commands with timeout and basic error handling.

## AI Design

The current design is a context-first assistant:

1. Gather evidence.
2. Format the evidence into one clear input.
3. Ask the model to reason from that evidence.
4. Return a structured troubleshooting answer.

This is a good beginner pattern because the model is not allowed to freely inspect the cluster. The application decides what evidence is collected.

## Current Limitations

- The real `kubectl` path uses a hard-coded pod name for `describe` and `logs`.
- There is no automated test suite yet.
- The model response is plain text, not structured JSON.
- The tool layer is read-only, which is safer but limited.
- Ollama must be running locally for analysis to work.

## Good Next Improvements

- Select the failing pod dynamically from `kubectl get pods`.
- Add tests for `/analyze` with mock tools enabled.
- Add model availability checks at startup or before analysis.
- Add more context sources such as deployments, services, config maps, and previous pod logs.
- Convert the model output into structured fields for evidence, root cause, confidence, and recommended commands.
