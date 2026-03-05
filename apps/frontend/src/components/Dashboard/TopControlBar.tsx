'use client';

import { ScenarioListItem } from '@ai-evaluator/shared-types';

interface TopControlBarProps {
  scenarios: ScenarioListItem[];
  selectedScenarioId: string;
  query: string;
  isLoading: boolean;
  onSelectScenario: (id: string) => void;
  onQueryChange: (query: string) => void;
  onEvaluate: () => void;
}

export default function TopControlBar({
  scenarios,
  selectedScenarioId,
  query,
  isLoading,
  onSelectScenario,
  onQueryChange,
  onEvaluate,
}: TopControlBarProps) {
  const selectedScenario = scenarios.find((s) => s.id === selectedScenarioId);

  return (
    <div className="fixed top-0 left-0 right-0 z-50 glass-card mx-4 mt-4 animate-fade-in">
      <div className="flex items-center gap-4 px-6 py-3">
        {/* Logo/Title */}
        <div className="flex items-center gap-2 shrink-0">
          <div className="w-8 h-8 rounded-lg bg-gradient-vibrant flex items-center justify-center">
            <span className="text-white font-bold text-lg">AI</span>
          </div>
          <h1 className="text-xl font-bold bg-gradient-to-r from-gradient-from via-gradient-via to-gradient-to bg-clip-text text-transparent">
            Evaluator
          </h1>
        </div>

        {/* Scenario Dropdown */}
        <select
          value={selectedScenarioId}
          onChange={(e) => onSelectScenario(e.target.value)}
          disabled={isLoading}
          className="glass-select disabled:opacity-50 disabled:cursor-not-allowed min-w-[300px] flex-1"
        >
          <option value="">Select Scenario</option>
          {scenarios.map((scenario) => (
            <option key={scenario.id} value={scenario.id}>
              {scenario.name}
            </option>
          ))}
        </select>

        {/* Show selected query preview */}
        {selectedScenario && query && (
          <div className="flex-1 text-sm text-gray-600 dark:text-gray-400 truncate max-w-[400px]">
            Query: {query.substring(0, 60)}...
          </div>
        )}

        {/* Evaluate Button */}
        <button
          onClick={onEvaluate}
          disabled={!selectedScenarioId || !query || isLoading}
          className="btn btn-primary shrink-0 disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden group"
        >
          {isLoading ? (
            <>
              <span className="animate-spin inline-block mr-2">⚡</span>
              Evaluating...
            </>
          ) : (
            <>
              <span className="mr-2">🚀</span>
              Evaluate Models
            </>
          )}
        </button>
      </div>
    </div>
  );
}
