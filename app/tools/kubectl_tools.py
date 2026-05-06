import subprocess


ALLOWED_COMMANDS = {
    "get pods",
    "get events",
    "describe pod",
    "logs",
}


def run_kubectl(args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["kubectl"] + args,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )

        output = result.stdout.strip() or result.stderr.strip()
        return output if output else "No output returned from kubectl."

    except subprocess.TimeoutExpired:
        return "kubectl command timed out."
    except FileNotFoundError:
        return "kubectl is not installed or not found in PATH."


def get_pods(namespace: str) -> str:
    return run_kubectl(["get", "pods", "-n", namespace])


def describe_pod(namespace: str, pod_name: str) -> str:
    return run_kubectl(["describe", "pod", pod_name, "-n", namespace])


def get_logs(namespace: str, pod_name: str) -> str:
    return run_kubectl(["logs", pod_name, "-n", namespace, "--tail=100"])


def get_events(namespace: str) -> str:
    return run_kubectl(["get", "events", "-n", namespace, "--sort-by=.lastTimestamp"])