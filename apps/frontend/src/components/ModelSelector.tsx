'use client';

import { ModelInfo } from '@ai-evaluator/shared-types';

interface ModelSelectorProps {
  models: ModelInfo[];
  selectedModelIds: string[];
  onToggleModel: (modelId: string) => void;
  disabled?: boolean;
}

export default function ModelSelector({
  models,
  selectedModelIds,
  onToggleModel,
  disabled = false,
}: ModelSelectorProps) {
  return (
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        2. Select Models to Compare
      </h3>

      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
        Choose 1-4 models for comparison. More models will take longer to evaluate.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {models.map((model) => {
          const isSelected = selectedModelIds.includes(model.id);
          const isDisabled = disabled || (!isSelected && selectedModelIds.length >= 4);

          return (
            <label
              key={model.id}
              className={`flex items-start p-4 border-2 rounded-lg cursor-pointer transition-all ${
                isSelected
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                  : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
              } ${isDisabled ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <input
                type="checkbox"
                className="mt-1 mr-3"
                checked={isSelected}
                onChange={() => onToggleModel(model.id)}
                disabled={isDisabled}
              />
              <div className="flex-1">
                <div className="font-semibold text-gray-900 dark:text-white">
                  {model.name}
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">
                  {model.provider} • {model.maxTokens.toLocaleString()} tokens
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-300">
                  {model.description}
                </div>
              </div>
            </label>
          );
        })}
      </div>

      {selectedModelIds.length > 0 && (
        <div className="mt-4 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
          <p className="text-sm text-green-800 dark:text-green-200">
            {selectedModelIds.length} model{selectedModelIds.length > 1 ? 's' : ''} selected
          </p>
        </div>
      )}
    </div>
  );
}
