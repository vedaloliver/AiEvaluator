import axios, { AxiosInstance } from 'axios';
import {
  EvaluationResult,
  MultiModelEvaluationRequest,
  MultiModelEvaluationResponse,
  RegulatoryScenario,
  ModelInfo,
  ScenarioListItem,
} from '@ai-evaluator/shared-types';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000';
    this.client = axios.create({
      baseURL: `${baseURL}/api`,
      timeout: 120000, // 2 minutes for evaluation
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  /**
   * Evaluates a query across multiple models
   */
  async evaluate(
    request: MultiModelEvaluationRequest
  ): Promise<EvaluationResult[]> {
    try {
      const response = await this.client.post<MultiModelEvaluationResponse>(
        '/evaluate',
        request
      );
      return response.data.results;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(
          error.response?.data?.error?.message ||
            'Failed to evaluate models'
        );
      }
      throw error;
    }
  }

  /**
   * Gets all available scenarios
   */
  async getScenarios(): Promise<ScenarioListItem[]> {
    try {
      const response = await this.client.get<{ scenarios: ScenarioListItem[] }>(
        '/scenarios'
      );
      return response.data.scenarios;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(
          error.response?.data?.error?.message ||
            'Failed to fetch scenarios'
        );
      }
      throw error;
    }
  }

  /**
   * Gets a specific scenario by ID
   */
  async getScenario(id: string): Promise<RegulatoryScenario> {
    try {
      const response = await this.client.get<RegulatoryScenario>(
        `/scenarios/${id}`
      );
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(
          error.response?.data?.error?.message ||
            `Failed to fetch scenario ${id}`
        );
      }
      throw error;
    }
  }

  /**
   * Gets all available models
   */
  async getModels(): Promise<ModelInfo[]> {
    try {
      const response = await this.client.get<{ models: ModelInfo[] }>(
        '/models'
      );
      return response.data.models;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(
          error.response?.data?.error?.message ||
            'Failed to fetch models'
        );
      }
      throw error;
    }
  }
}

export const apiClient = new ApiClient();
