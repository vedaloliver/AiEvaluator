import { ModelInfo } from '@ai-evaluator/shared-types';

// Pre-defined list of available models
// In a real implementation, this would query the Azure AI Foundry catalog
const AVAILABLE_MODELS: ModelInfo[] = [
  {
    id: 'gpt-4',
    name: 'GPT-4',
    provider: 'OpenAI',
    description: 'Most capable GPT-4 model for complex reasoning and analysis',
    capabilities: ['chat', 'reasoning', 'code'],
    maxTokens: 8192,
  },
  {
    id: 'claude-3-opus',
    name: 'Claude 3 Opus',
    provider: 'Anthropic',
    description: 'Highest performance Claude model with superior reasoning',
    capabilities: ['chat', 'reasoning', 'code', 'analysis'],
    maxTokens: 200000,
  },
  {
    id: 'mistral-large',
    name: 'Mistral Large',
    provider: 'Mistral AI',
    description: 'Advanced multilingual model with strong performance',
    capabilities: ['chat', 'reasoning', 'code'],
    maxTokens: 32000,
  },
  {
    id: 'gemini-pro',
    name: 'Gemini Pro',
    provider: 'Google',
    description: 'Google\'s powerful multimodal AI model',
    capabilities: ['chat', 'reasoning', 'multimodal'],
    maxTokens: 30720,
  },
  {
    id: 'llama-3-70b',
    name: 'Llama 3 70B',
    provider: 'Meta',
    description: 'Open-source large language model with strong capabilities',
    capabilities: ['chat', 'reasoning'],
    maxTokens: 8192,
  },
];

export class ModelService {
  /**
   * Gets all available models
   */
  public getAllModels(): ModelInfo[] {
    return AVAILABLE_MODELS;
  }

  /**
   * Gets a specific model by ID
   */
  public getModelById(modelId: string): ModelInfo | undefined {
    return AVAILABLE_MODELS.find((model) => model.id === modelId);
  }

  /**
   * Validates if a model ID is available
   */
  public isModelAvailable(modelId: string): boolean {
    return AVAILABLE_MODELS.some((model) => model.id === modelId);
  }

  /**
   * Gets models by capability
   */
  public getModelsByCapability(capability: string): ModelInfo[] {
    return AVAILABLE_MODELS.filter((model) =>
      model.capabilities.includes(capability)
    );
  }

  /**
   * Gets models by provider
   */
  public getModelsByProvider(provider: string): ModelInfo[] {
    return AVAILABLE_MODELS.filter(
      (model) => model.provider.toLowerCase() === provider.toLowerCase()
    );
  }
}
