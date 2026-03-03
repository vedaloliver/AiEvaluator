'use client';

import { ScenarioListItem } from '@ai-evaluator/shared-types';

interface ScenarioSelectorProps {
  scenarios: ScenarioListItem[];
  selectedScenarioId: string;
  onSelectScenario: (scenarioId: string) => void;
  disabled?: boolean;
}

export default function ScenarioSelector({
  scenarios,
  selectedScenarioId,
  onSelectScenario,
  disabled = false,
}: ScenarioSelectorProps) {
  const selectedScenario = scenarios.find((s) => s.id === selectedScenarioId);

  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        1. Select Regulatory Scenario
      </h3>

      <select
        className="input"
        value={selectedScenarioId}
        onChange={(e) => onSelectScenario(e.target.value)}
        disabled={disabled}
      >
        <option value="">Choose a scenario...</option>
        {scenarios.map((scenario) => (
          <option key={scenario.id} value={scenario.id}>
            {scenario.name}
          </option>
        ))}
      </select>

      {selectedScenario && (
        <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
          <p className="text-sm text-gray-700 dark:text-gray-300">
            {selectedScenario.description}
          </p>
        </div>
      )}
    </div>
  );
}
