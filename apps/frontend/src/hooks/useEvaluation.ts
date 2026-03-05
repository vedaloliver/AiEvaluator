'use client';

import { useState, useEffect } from 'react';
import {
  ScenarioListItem,
  ModelInfo,
  EvaluationResult,
  MultiModelEvaluationRequest,
} from '@ai-evaluator/shared-types';
import { apiClient } from '@/lib/api-client';

interface HistoryItem {
  id: string;
  timestamp: string;
  scenarioId: string;
  query: string;
  results: EvaluationResult[];
}

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export function useEvaluation() {
  const [scenarios, setScenarios] = useState<ScenarioListItem[]>([]);
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [selectedScenarioId, setSelectedScenarioId] = useState<string>('');
  const [selectedModelIds, setSelectedModelIds] = useState<string[]>([]);
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<EvaluationResult[]>([]);
  const [streamingResults, setStreamingResults] = useState<EvaluationResult[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isStreaming, setIsStreaming] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [isInitializing, setIsInitializing] = useState<boolean>(true);
  const [evaluationHistory, setEvaluationHistory] = useState<HistoryItem[]>([]);

  // Load scenarios and models on mount
  useEffect(() => {
    const loadData = async () => {
      try {
        const [scenariosData, modelsData] = await Promise.all([
          apiClient.getScenarios(),
          apiClient.getModels(),
        ]);
        setScenarios(scenariosData);
        setModels(modelsData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load data');
      } finally {
        setIsInitializing(false);
      }
    };

    loadData();
  }, []);

  // Load evaluation history from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem('evaluation-history');
      if (saved) {
        setEvaluationHistory(JSON.parse(saved));
      }
    } catch (err) {
      console.error('Failed to load evaluation history:', err);
    }
  }, []);

  // Auto-select all models and set example query when scenario is selected
  useEffect(() => {
    if (selectedScenarioId && models.length > 0) {
      const allModelIds = models.map((m) => m.id);
      setSelectedModelIds(allModelIds);

      // Auto-populate query with scenario's example query
      const scenario = scenarios.find((s) => s.id === selectedScenarioId);
      if (scenario?.exampleQuery) {
        setQuery(scenario.exampleQuery);
      }
    }
  }, [selectedScenarioId, models, scenarios]);

  const toggleModel = (modelId: string) => {
    setSelectedModelIds((prev) =>
      prev.includes(modelId)
        ? prev.filter((id) => id !== modelId)
        : [...prev, modelId]
    );
  };

  const saveToHistory = (evaluation: EvaluationResult[]) => {
    try {
      const historyItem: HistoryItem = {
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
        scenarioId: selectedScenarioId,
        query: query.substring(0, 100),
        results: evaluation,
      };

      const updated = [historyItem, ...evaluationHistory].slice(0, 10);
      setEvaluationHistory(updated);
      localStorage.setItem('evaluation-history', JSON.stringify(updated));
    } catch (err) {
      console.error('Failed to save evaluation history:', err);
    }
  };

  const evaluate = async () => {
    if (!selectedScenarioId || selectedModelIds.length === 0 || !query.trim()) {
      setError('Please select a scenario and a test query');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResults([]);
    setStreamingResults([]);

    try {
      const request: MultiModelEvaluationRequest = {
        scenarioId: selectedScenarioId,
        modelIds: selectedModelIds,
        query: query.trim(),
      };

      const evaluationResults = await apiClient.evaluate(request);

      // Simulate streaming by adding results one by one
      setIsStreaming(true);
      setIsLoading(false); // Stop loading spinner, start streaming

      for (let i = 0; i < evaluationResults.length; i++) {
        await delay(500); // 500ms between each result
        setStreamingResults((prev) => [...prev, evaluationResults[i]]);
      }

      setIsStreaming(false);
      setResults(evaluationResults);

      // Save to history
      saveToHistory(evaluationResults);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Evaluation failed');
      setIsStreaming(false);
    } finally {
      setIsLoading(false);
    }
  };

  const reset = () => {
    setSelectedScenarioId('');
    setSelectedModelIds([]);
    setQuery('');
    setResults([]);
    setStreamingResults([]);
    setError(null);
  };

  return {
    scenarios,
    models,
    selectedScenarioId,
    selectedModelIds,
    query,
    results,
    streamingResults,
    isLoading,
    isStreaming,
    error,
    isInitializing,
    evaluationHistory,
    setSelectedScenarioId,
    toggleModel,
    setQuery,
    evaluate,
    reset,
  };
}
