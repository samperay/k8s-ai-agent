# AI Learning Path

This learning path uses the current codebase to teach practical AI agent development for Kubernetes troubleshooting.

## 1. Understand The Agent Shape

An AI agent is more than a model call. In this project, the agent has four parts:

- Input: the issue and namespace submitted by the user.
- Tools: mock Kubernetes outputs or real `kubectl` commands.
- Context: the issue plus pods, events, describe output, and logs.
- Reasoning response: the model output shaped by the system prompt.

Read these files first:

- `app/main.py`
- `app/agent.py`
- `app/prompts.py`
- `app/tools/mock_tools.py`

## 2. Run With Mock Tools

Start with mock tools so the behavior is predictable and safe.

```env
USE_MOCK_TOOLS=true
OLLAMA_MODEL=llama3.2
```

Run the app:

```bash
litestar --app app.main:app run --reload
```

Try this issue:

```text
backend pod is CrashLoopBackOff
```

The mock data includes a backend pod in `CrashLoopBackOff` and logs showing a missing `DATABASE_URL`. The model should connect those clues and recommend safe next commands.

## 3. Study Prompt Behavior

Open `app/prompts.py` and inspect `SYSTEM_PROMPT`.

The prompt asks the model to:

- Explain the issue simply.
- Analyze Kubernetes command output.
- Identify the likely cause.
- Suggest safe next troubleshooting steps.
- Avoid destructive commands unless clearly marked as risky.

Practice change:

1. Add a stronger rule that the model must quote the exact evidence it used.
2. Run the same issue again.
3. Compare whether the answer is easier to verify.

## 4. Study Context Engineering

Open `collect_kubernetes_context()` in `app/agent.py`.

The model receives one combined context block containing:

- User issue.
- Namespace.
- `kubectl get pods`.
- `kubectl get events`.
- `kubectl describe pod`.
- `kubectl logs`.

This is context engineering: giving the model enough structured evidence to reason from without asking it to guess.

Practice change:

1. Add a fake image pull failure to `mock_tools.py`.
2. Update the issue text to mention `ImagePullBackOff`.
3. Confirm whether the model points to the image or registry problem.

## 5. Learn The Tool Boundary

The app has two tool layers:

- `app/tools/mock_tools.py` returns fixed sample output.
- `app/tools/kubectl_tools.py` runs read-only `kubectl` commands.

This boundary is important because it lets you develop the agent without needing a live cluster.

Practice change:

1. Add another mock function for `kubectl get deployment`.
2. Add its output to the context block.
3. Check whether deployment details improve the answer.

## 6. Move Carefully To Real Kubernetes

Only switch to real tools when you understand the mock workflow.

```env
USE_MOCK_TOOLS=false
OLLAMA_MODEL=llama3.2
```

Before running the app with real tools:

- Confirm `kubectl` is installed.
- Confirm `kubectl config current-context` points to the intended cluster.
- Start with a non-production namespace.
- Keep commands read-only.

The current real tool layer reads pods, events, one described pod, and logs. It does not apply, delete, scale, restart, or patch resources.

## 7. Improve The Agent

Once the baseline flow is clear, improve one area at a time:

- Dynamic pod selection instead of the hard-coded backend pod name.
- Better error handling when Ollama is unavailable.
- More Kubernetes context such as deployments, services, config maps, and recent replica set events.
- Tests for mock context collection and API responses.
- A response format that separates evidence, hypothesis, confidence, and next steps.

## 8. Learning Milestones

Use these checkpoints to measure progress:

- You can explain the request flow without looking at the code.
- You can predict what context the model receives.
- You can modify mock data to create a new failure scenario.
- You can improve the prompt and compare the answer quality.
- You understand why real cluster access should stay read-only.
- You can describe what should be tested before trusting the agent.
