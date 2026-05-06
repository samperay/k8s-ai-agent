from pathlib import Path

from litestar import Litestar, get, post
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.exceptions import HTTPException
from litestar.response import Template
from litestar.template.config import TemplateConfig

from app.agent import analyze_kubernetes_issue
from app.schemas import AnalyzeRequest, AnalyzeResponse


@get("/", sync_to_thread=False)
def index() -> Template:
    return Template(
        template_name="index.html",
        context={
            "title": "Kubernetes AI Agent",
        },
    )


@post("/analyze", sync_to_thread=True)
def analyze(data: AnalyzeRequest) -> AnalyzeResponse:
    try:
        analysis = analyze_kubernetes_issue(
            issue=data.issue,
            namespace=data.namespace,
        )
    except AgentError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return AnalyzeResponse(
        issue=data.issue,
        namespace=data.namespace,
        analysis=analysis,
    )


app = Litestar(
    route_handlers=[index, analyze],
    template_config=TemplateConfig(
        directory=Path(__file__).parent / "templates",
        engine=JinjaTemplateEngine,
    ),
)
