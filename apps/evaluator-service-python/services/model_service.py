from models import ModelInfo


# Pre-defined list of available models
# In a real implementation, this would query the Azure AI Foundry catalog
AVAILABLE_MODELS: list[ModelInfo] = [
    ModelInfo(
        id="gpt-4",
        name="GPT-4",
        provider="OpenAI",
        description="Most capable GPT-4 model for complex reasoning and analysis",
        capabilities=["chat", "reasoning", "code"],
        maxTokens=8192
    ),
    ModelInfo(
        id="claude-3-opus",
        name="Claude 3 Opus",
        provider="Anthropic",
        description="Highest performance Claude model with superior reasoning",
        capabilities=["chat", "reasoning", "code", "analysis"],
        maxTokens=200000
    ),
    ModelInfo(
        id="mistral-large",
        name="Mistral Large",
        provider="Mistral AI",
        description="Advanced multilingual model with strong performance",
        capabilities=["chat", "reasoning", "code"],
        maxTokens=32000
    ),
    ModelInfo(
        id="gemini-pro",
        name="Gemini Pro",
        provider="Google",
        description="Google's powerful multimodal AI model",
        capabilities=["chat", "reasoning", "multimodal"],
        maxTokens=30720
    ),
    ModelInfo(
        id="llama-3-70b",
        name="Llama 3 70B",
        provider="Meta",
        description="Open-source large language model with strong capabilities",
        capabilities=["chat", "reasoning"],
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
