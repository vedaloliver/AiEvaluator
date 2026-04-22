"""Azure AI Foundry Red Team Service.

Dispatches to the mock implementation when ``use_mock_data=True`` (default).

Real implementation uses:
- ``azure-ai-evaluation`` for the RedTeam runner and risk evaluators
- ``azure-ai-projects`` (AIProjectClient) as the project connection handle
- ``azure-identity`` (DefaultAzureCredential) for auth

The actual ``azure.ai.evaluation.red_team.RedTeam`` class runs attacks locally
against a target callback.  A fully cloud-submitted "fire and forget" eval API
is not yet in the public SDK — this service is scaffolded for when it lands or
for a custom wrapper around the local runner.
"""
from config.settings import settings
from models.azure_red_team import AzureRedTeamRequest, AzureRedTeamRunResult, TaxonomyUploadResult
from models.taxonomy import ProhibitedActionsTaxonomy


class AzureNotConfiguredError(Exception):
    """Raised when Azure SDK or credentials are unavailable."""


class AzureRedTeamService:
    """Public Azure red team service — delegates to mock or real backend."""

    def __init__(self) -> None:
        if settings.use_mock_data:
            from mocks.azure_red_team import MockAzureRedTeamService
            self._backend = MockAzureRedTeamService()
        else:
            self._backend = _RealAzureRedTeamBackend()

    async def upload_taxonomy(self, taxonomy: ProhibitedActionsTaxonomy) -> TaxonomyUploadResult:
        return await self._backend.upload_taxonomy(taxonomy)

    async def run_cloud_eval(self, request: AzureRedTeamRequest) -> AzureRedTeamRunResult:
        return await self._backend.run_cloud_eval(request)


# ---------------------------------------------------------------------------
# Real backend (requires azure-ai-evaluation + azure-ai-projects installed)
# ---------------------------------------------------------------------------

class _RealAzureRedTeamBackend:
    """Skeleton real implementation.  Raises AzureNotConfiguredError until
    the SDK calls are filled in and credentials are configured.

    Validation is deferred to first use so the app starts cleanly even when
    Azure credentials are not yet configured.
    """

    def __init__(self) -> None:
        self._project_client = None  # lazily initialised

    def _get_client(self):
        if self._project_client is not None:
            return self._project_client

        if not settings.use_azure_red_team:
            raise AzureNotConfiguredError(
                "Azure red teaming is disabled. "
                "Set USE_AZURE_RED_TEAM=true and AZURE_AI_PROJECT_ENDPOINT."
            )
        if not settings.azure_ai_project_endpoint:
            raise AzureNotConfiguredError(
                "AZURE_AI_PROJECT_ENDPOINT is not configured."
            )

        try:
            from azure.ai.projects import AIProjectClient  # type: ignore[import-not-found]
            from azure.identity import DefaultAzureCredential  # type: ignore[import-not-found]
            import azure.ai.evaluation  # noqa: F401 — validates package is present  # type: ignore[import-not-found]
        except ImportError as exc:
            raise AzureNotConfiguredError(
                "Required Azure packages are not installed. "
                "Install azure-ai-evaluation, azure-ai-projects, and azure-identity."
            ) from exc

        self._project_client = AIProjectClient(
            endpoint=settings.azure_ai_project_endpoint,
            credential=DefaultAzureCredential(),
        )
        return self._project_client

    async def upload_taxonomy(self, taxonomy: ProhibitedActionsTaxonomy) -> TaxonomyUploadResult:
        self._get_client()
        # TODO: Serialise taxonomy to Azure AI datasets format and upload.
        # The azure-ai-evaluation SDK does not yet expose a public taxonomy
        # upload API — implement here when available.
        raise NotImplementedError(
            "Taxonomy upload requires Azure AI Evaluation SDK support. "
            "Not yet available — use USE_MOCK_DATA=true."
        )

    async def run_cloud_eval(self, request: AzureRedTeamRequest) -> AzureRedTeamRunResult:
        self._get_client()
        # TODO: Wire up azure.ai.evaluation.red_team.RedTeam once a target
        # callback / agent endpoint is available.
        #
        # Example structure (local runner, not cloud-submitted):
        #
        #   from azure.ai.evaluation.red_team import RedTeam, AttackStrategy, RiskCategory
        #   red_team = RedTeam(
        #       azure_ai_project=self._project_client,
        #       attack_strategies=[AttackStrategy[s.value.upper()] for s in request.attack_strategies],
        #       risk_categories=[RiskCategory[c] for c in request.risk_categories],
        #       num_turns=request.num_turns,
        #   )
        #   result = await red_team.run(target=<agent_callback>)
        #
        raise NotImplementedError(
            "Cloud eval run requires a configured agent target endpoint. "
            "Not yet implemented — use USE_MOCK_DATA=true."
        )
