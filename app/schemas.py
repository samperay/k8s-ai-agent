from dataclasses import dataclass


@dataclass
class AnalyzeRequest:
    issue: str
    namespace: str = "default"


@dataclass
class AnalyzeResponse:
    issue: str
    namespace: str
    analysis: str