from pydantic import BaseModel, Field
from typing import Optional, Literal


class AzureAIConfig(BaseModel):
    """Azure AI configuration"""
    endpoint: str
    subscription_id: str = Field(alias="subscriptionId")
    tenant_id: str = Field(alias="tenantId")
    client_id: str = Field(alias="clientId")
    client_secret: str = Field(alias="clientSecret")

    class Config:
        populate_by_name = True


class ModelInfo(BaseModel):
    """Information about an AI model"""
    id: str
    name: str
    provider: str
    description: str
    capabilities: list[str]
    max_tokens: int = Field(alias="maxTokens")

    class Config:
        populate_by_name = True
        protected_namespaces = ()


MessageRole = Literal["system", "user", "assistant"]


class AzureChatMessage(BaseModel):
    """Azure chat message"""
    role: MessageRole
    content: str


class AzureChatRequest(BaseModel):
    """Request for Azure chat completion"""
    messages: list[AzureChatMessage]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = Field(default=None, alias="maxTokens")
    top_p: Optional[float] = Field(default=None, alias="topP")

    class Config:
        populate_by_name = True


class ChatChoice(BaseModel):
    """Chat completion choice"""
    index: int
    message: AzureChatMessage
    finish_reason: str = Field(alias="finishReason")

    class Config:
        populate_by_name = True


class ChatUsage(BaseModel):
    """Token usage information"""
    prompt_tokens: int = Field(alias="promptTokens")
    completion_tokens: int = Field(alias="completionTokens")
    total_tokens: int = Field(alias="totalTokens")

    class Config:
        populate_by_name = True


class AzureChatResponse(BaseModel):
    """Response from Azure chat completion"""
    id: str
    model: str
    choices: list[ChatChoice]
    usage: ChatUsage


class AzureEvaluatorRequest(BaseModel):
    """Request for Azure evaluator"""
    query: str
    response: str
    context: Optional[str] = None


class AzureEvaluatorResponse(BaseModel):
    """Response from Azure evaluator"""
    score: float
    rationale: str
    severity: Optional[str] = None
