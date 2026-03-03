'use client';

import { useEvaluation } from '@/hooks/useEvaluation';
import DashboardLayout from '@/components/Dashboard/DashboardLayout';

export default function Home() {
  const {
    scenarios,
    selectedScenarioId,
    query,
    results,
    streamingResults,
    isLoading,
    isStreaming,
    error,
    isInitializing,
    setSelectedScenarioId,
    setQuery,
    evaluate,
  } = useEvaluation();

  if (isInitializing) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-vibrant-purple mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            Initializing AI Evaluator...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen p-4">
        <div className="glass-card p-8 max-w-md">
          <div className="text-6xl mb-4 text-center">⚠️</div>
          <h2 className="text-xl font-bold text-fail mb-4 text-center">Error</h2>
          <p className="text-gray-700 dark:text-gray-300 text-center">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <DashboardLayout
      scenarios={scenarios}
      selectedScenarioId={selectedScenarioId}
      query={query}
      results={results}
      isLoading={isLoading}
      isStreaming={isStreaming}
      streamingResults={streamingResults}
      onSelectScenario={setSelectedScenarioId}
      onQueryChange={setQuery}
      onEvaluate={evaluate}
    />
  );
}
