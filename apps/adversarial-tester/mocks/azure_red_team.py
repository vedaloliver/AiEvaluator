"""Mock Azure AI Foundry red team service.

Returns deterministic canned responses that look realistic — no Azure
credentials or SDK packages required.

Taxonomy IDs and run IDs are derived from the request content so the same
request always returns the same IDs (useful for tests that check round-trips).
"""
import hashlib

from models.azure_red_team import AzureRedTeamRequest, AzureRedTeamRunResult, TaxonomyUploadResult
from models.taxonomy import ProhibitedActionsTaxonomy


def _stable_id(seed: str, prefix: str = "") -> str:
    """Return a short stable hex ID derived from *seed*."""
    digest = hashlib.md5(seed.encode()).hexdigest()
    return f"{prefix}{digest[:12]}" if prefix else digest[:12]


class MockAzureRedTeamService:
    """Deterministic mock — no Azure calls, no credentials needed."""

    async def upload_taxonomy(self, taxonomy: ProhibitedActionsTaxonomy) -> TaxonomyUploadResult:
        """Return a fake taxonomy file ID derived from the scenario ID."""
        taxonomy_file_id = _stable_id(taxonomy.scenario_id, prefix="tax-")
        return TaxonomyUploadResult(
            taxonomyFileId=taxonomy_file_id,
            scenarioId=taxonomy.scenario_id,
            message=(
                f"[MOCK] Taxonomy for scenario '{taxonomy.scenario_id}' registered. "
                f"File ID: {taxonomy_file_id}"
            ),
        )

    async def run_cloud_eval(self, request: AzureRedTeamRequest) -> AzureRedTeamRunResult:
        """Return a canned completed run result without hitting Azure."""
        seed = f"{request.agent_name}:{request.agent_version}"
        run_id = _stable_id(seed, prefix="run-")

        strategy_values = [s.value for s in request.attack_strategies]

        mock_details = {
            "mock": True,
            "numTurns": request.num_turns,
            "attacksAttempted": len(strategy_values) * len(request.risk_categories),
            "attacksBlocked": len(strategy_values),
            "attackSuccessRate": round(
                1 - (len(strategy_values) / max(len(strategy_values) * len(request.risk_categories), 1)),
                3,
            ),
            "summaryByStrategy": {
                strategy: {
                    "attempted": len(request.risk_categories),
                    "blocked": 1,
                    "succeeded": len(request.risk_categories) - 1,
                }
                for strategy in strategy_values
            },
            "summaryByRiskCategory": {
                category: {
                    "attempted": len(strategy_values),
                    "violated": max(len(strategy_values) - 1, 0),
                }
                for category in request.risk_categories
            },
        }

        return AzureRedTeamRunResult(
            runId=run_id,
            status="completed",
            agentName=request.agent_name,
            agentVersion=request.agent_version,
            attackStrategies=strategy_values,
            riskCategories=request.risk_categories,
            details=mock_details,
        )
