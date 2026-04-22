"""Mock implementations for adversarial tester services.

All mocks are deterministic (seeded RNG or canned data) so test runs are
reproducible without any external dependencies.

Usage
-----
Services check ``settings.use_mock_data`` at instantiation time and import
from here when mocks are enabled.
"""

from mocks.llm_judge import MockLLMJudgeService
from mocks.azure_red_team import MockAzureRedTeamService

__all__ = [
    "MockLLMJudgeService",
    "MockAzureRedTeamService",
]
