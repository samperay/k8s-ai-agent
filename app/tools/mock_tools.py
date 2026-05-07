def get_pods(namespace: str) -> str:
    return f"""
NAMESPACE     NAME                          READY   STATUS             RESTARTS   AGE
{namespace}   frontend-7fc74cb778-bgjmd     1/1     Running            0          2h
{namespace}   backend-bf5894f7-d4knx        0/1     CrashLoopBackOff   8          45m
{namespace}   postgres-0                   1/1     Running            0          2h
"""


def describe_pod(namespace: str, pod_name: str = "backend-bf5894f7-d4knx") -> str:
    return f"""
Name:             {pod_name}
Namespace:        {namespace}
Status:           Running
Containers:
  backend:
    State:        Waiting
      Reason:     CrashLoopBackOff
    Last State:   Terminated
      Reason:     Error
      Exit Code:  1
Events:
  Warning  BackOff  kubelet  Back-off restarting failed container backend
"""


def get_logs(namespace: str, pod_name: str = "backend-bf5894f7-d4knx") -> str:
    return """
Traceback (most recent call last):
  File "/app/main.py", line 14, in <module>
    connect_to_database()
Exception: DATABASE_URL environment variable is missing
"""


def get_events(namespace: str) -> str:
    return f"""
LAST SEEN   TYPE      REASON    OBJECT                              MESSAGE
10m         Warning   BackOff   pod/backend-bf5894f7-d4knx          Back-off restarting failed container backend
8m          Normal    Pulled    pod/backend-bf5894f7-d4knx          Successfully pulled image
"""

def get_ImagePullBackOff(namespace: str, pod_name: str = "backend-bf5894f7-d4knx") -> str:
  return f"""
NAME       READY   STATUS             RESTARTS   AGE
backend-bf5894f7-d4knx   0/1     ImagePullBackOff   0          1m5s
"""