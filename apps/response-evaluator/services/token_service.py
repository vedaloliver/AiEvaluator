"""Token estimation and cost calculation service."""

import logging
from typing import Optional

from models.evaluation import TokenUsage, CostEstimate
from config.pricing import get_model_pricing

logger = logging.getLogger(__name__)

# Try to import tiktoken for GPT models
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    logger.warning("tiktoken not available, using fallback token estimation")


def estimate_tokens(text: str, model_id: str) -> int:
    """
    Estimate the number of tokens in a text for a given model.

    Args:
        text: The text to estimate tokens for
        model_id: The model identifier

    Returns:
        Estimated number of tokens
    """
    if not text:
        return 0

    # Try to use tiktoken for GPT models
    if TIKTOKEN_AVAILABLE and (model_id.startswith("gpt-") or model_id.startswith("text-")):
        try:
            # Get encoding for the model
            if model_id.startswith("gpt-4"):
                encoding = tiktoken.encoding_for_model("gpt-4")
            elif model_id.startswith("gpt-3.5"):
                encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            else:
                encoding = tiktoken.get_encoding("cl100k_base")

            return len(encoding.encode(text))
        except Exception as e:
            logger.warning(f"Error using tiktoken: {e}, falling back to estimation")

    # Fallback: rough estimation (1 token ≈ 4 characters for English text)
    return len(text) // 4


def calculate_cost(
    model_id: str,
    prompt_tokens: int,
    completion_tokens: int
) -> CostEstimate:
    """
    Calculate the estimated cost for an LLM call.

    Args:
        model_id: The model identifier
        prompt_tokens: Number of input tokens
        completion_tokens: Number of output tokens

    Returns:
        CostEstimate object with amount, currency, and pricing details
    """
    pricing = get_model_pricing(model_id)

    # Calculate cost (pricing is per 1M tokens)
    input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
    output_cost = (completion_tokens / 1_000_000) * pricing["output"]
    total_cost = input_cost + output_cost

    return CostEstimate(
        amount=round(total_cost, 6),  # Round to 6 decimal places
        currency="USD",
        modelPricing=f"${pricing['input']}/{pricing['output']} per 1M tokens"
    )


def calculate_tokens_and_cost(
    query: str,
    system_prompt: str,
    response: str,
    model_id: str
) -> tuple[TokenUsage, CostEstimate]:
    """
    Calculate both token usage and cost for an evaluation.

    Args:
        query: The user query
        system_prompt: The system prompt
        response: The model response
        model_id: The model identifier

    Returns:
        Tuple of (TokenUsage, CostEstimate)
    """
    # Estimate tokens
    prompt_text = f"{system_prompt}\n{query}"
    prompt_tokens = estimate_tokens(prompt_text, model_id)
    completion_tokens = estimate_tokens(response, model_id)
    total_tokens = prompt_tokens + completion_tokens

    # Create TokenUsage object
    token_usage = TokenUsage(
        promptTokens=prompt_tokens,
        completionTokens=completion_tokens,
        totalTokens=total_tokens
    )

    # Calculate cost
    cost_estimate = calculate_cost(model_id, prompt_tokens, completion_tokens)

    return token_usage, cost_estimate
