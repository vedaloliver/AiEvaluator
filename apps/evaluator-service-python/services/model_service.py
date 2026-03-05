from models import ModelInfo


# Pre-defined list of available models
# In a real implementation, this would query the Azure AI Foundry catalog
# Currently only gpt-4 has mock fixtures for testing
AVAILABLE_MODELS: list[ModelInfo] = [
    ModelInfo(
        id="gpt-4",
        name="GPT-4",
        provider="OpenAI",
        description="Most capable GPT-4 model for complex reasoning and analysis",
        capabilities=["chat", "reasoning", "code"],
        maxTokens=8192
    ),
]


class ModelService:
    """Service for managing AI model information"""

    def get_all_models(self) -> list[ModelInfo]:
        """Gets all available models"""
        return AVAILABLE_MODELS

    def get_model_by_id(self, model_id: str) -> ModelInfo | None:
        """Gets a specific model by ID"""
        for model in AVAILABLE_MODELS:
            if model.id == model_id:
                return model
        return None

    def is_model_available(self, model_id: str) -> bool:
        """Validates if a model ID is available"""
        return any(model.id == model_id for model in AVAILABLE_MODELS)

    def get_models_by_capability(self, capability: str) -> list[ModelInfo]:
        """Gets models by capability"""
        return [
            model for model in AVAILABLE_MODELS
            if capability in model.capabilities
        ]

    def get_models_by_provider(self, provider: str) -> list[ModelInfo]:
        """Gets models by provider"""
        return [
            model for model in AVAILABLE_MODELS
            if model.provider.lower() == provider.lower()
        ]
