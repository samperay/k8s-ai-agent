import os

import ollama
from dotenv import load_dotenv

from app.prompts import SYSTEM_PROMPT
from app.tools import kubectl_tools, mock_tools

load_dotenv()


class AgentError(Exception):
    pass


def use_mock_tools() -> bool:
    return os.getenv("USE_MOCK_TOOLS", "true").lower() == "true"


def get_ollama_model() -> str:
    return os.getenv("OLLAMA_MODEL", "llama3.2")


def collect_kubernetes_context(issue: str, namespace: str) -> str:
    if use_mock_tools():
        pods = mock_tools.get_pods(namespace)
        events = mock_tools.get_events(namespace)
        describe = mock_tools.describe_pod(namespace)
        logs = mock_tools.get_logs(namespace)
        ImagePullBackOff = mock_tools.get_ImagePullBackOff(namespace)
    else:
        pods = kubectl_tools.get_pods(namespace)
        events = kubectl_tools.get_events(namespace)

        pod_name = "backend-bf5894f7-d4knx"
        describe = kubectl_tools.describe_pod(namespace, pod_name)
        logs = kubectl_tools.get_logs(namespace, pod_name)

    return f"""
User issue:
{issue}

Namespace:
{namespace}

kubectl get pods:
{pods}

kubectl get events:
{events}

kubectl describe pod:
{describe}

kubectl logs:
{logs}
"""

# main.py(UI) calls this function
def analyze_kubernetes_issue(issue: str, namespace: str) -> str:
    try:
        context = collect_kubernetes_context(issue, namespace)

        response = ollama.chat(
            model=get_ollama_model(),
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": context,
                },
            ],
        )

        return response["message"]["content"]

    except Exception as exc:
        raise AgentError(f"Failed to analyze Kubernetes issue: {exc}") from exc