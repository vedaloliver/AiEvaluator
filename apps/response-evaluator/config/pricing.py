"""Model pricing configuration for cost estimation."""

# Model pricing in USD per 1M tokens
# Format: {"input": price_per_1M_input_tokens, "output": price_per_1M_output_tokens}
MODEL_PRICING = {
    # OpenAI GPT-4 models
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-4": {"input": 30.00, "output": 60.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},

    # Anthropic Claude models
    "claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-opus": {"input": 15.00, "output": 75.00},
    "claude-3-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},

    # Meta Llama models (example pricing)
    "llama-3-70b": {"input": 0.90, "output": 0.90},
    "llama-3-8b": {"input": 0.20, "output": 0.20},

    # Default fallback pricing
    "default": {"input": 1.00, "output": 2.00},
}


def get_model_pricing(model_id: str) -> dict:
    """
    Get pricing for a specific model.

    Args:
        model_id: The model identifier

    Returns:
        Dict with 'input' and 'output' prices per 1M tokens
    """
    # Try exact match first
    if model_id in MODEL_PRICING:
        return MODEL_PRICING[model_id]

    # Try partial match (e.g., "gpt-4o-2024-05-13" matches "gpt-4o")
    for model_key in MODEL_PRICING.keys():
        if model_id.startswith(model_key):
            return MODEL_PRICING[model_key]

    # Return default pricing
    return MODEL_PRICING["default"]
