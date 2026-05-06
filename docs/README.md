# Documentation

This folder contains the learning material for the Kubernetes AI Agent.

## Start Here

- [AI learning path](ai-learning-path.md): a step-by-step path for learning how the agent works.
- [Architecture notes](architecture.md): a concise map of the app, AI flow, and Kubernetes tool boundary.

## Learning Goals

By the end of this project, you should understand:

- How a web request becomes an AI troubleshooting response.
- How Kubernetes context is gathered before calling a model.
- Why prompt design matters for reliable answers.
- How mock tool output makes agent development safer.
- How to move from mock tools to real `kubectl` reads carefully.

## Suggested Practice Loop

1. Pick a Kubernetes failure scenario.
2. Add or edit mock output in `app/tools/mock_tools.py`.
3. Submit the issue through the web UI.
4. Compare the AI response with the raw context.
5. Improve the prompt or context collection.
6. Repeat until the response is clear, safe, and useful.
