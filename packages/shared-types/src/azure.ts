export interface AzureAIConfig {
  endpoint: string;
  subscriptionId: string;
  tenantId: string;
  clientId: string;
  clientSecret: string;
}

export interface ModelInfo {
  id: string;
  name: string;
  provider: string;
  description: string;
  capabilities: string[];
  maxTokens: number;
}

export interface AzureChatMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface AzureChatRequest {
  messages: AzureChatMessage[];
  temperature?: number;
  maxTokens?: number;
  topP?: number;
}

export interface AzureChatResponse {
  id: string;
  model: string;
  choices: Array<{
    index: number;
    message: AzureChatMessage;
    finishReason: string;
  }>;
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
}

export interface AzureEvaluatorRequest {
  query: string;
  response: string;
  context?: string;
}

export interface AzureEvaluatorResponse {
  score: number;
  rationale: string;
  severity?: string;
}
