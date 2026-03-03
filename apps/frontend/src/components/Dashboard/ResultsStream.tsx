'use client';

import { EvaluationResult } from '@ai-evaluator/shared-types';
import ModelResultCard from '@/components/Cards/ModelResultCard';

interface ResultsStreamProps {
  results: EvaluationResult[];
  isStreaming: boolean;
}

export default function ResultsStream({ results, isStreaming }: ResultsStreamProps) {
  if (results.length === 0 && !isStreaming) {
    return (
      <div className="flex items-center justify-center h-full p-6">
        <div className="text-center">
          <div className="text-6xl mb-4 opacity-50">🤖</div>
          <h3 className="text-lg font-semibold text-gray-600 dark:text-gray-400 mb-2">
            No Results Yet
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-500">
            Select a scenario and query to begin evaluation
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-3 p-4 overflow-auto h-full">
      {/* Results Header */}
      <div className="flex items-center justify-between mb-1">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
          <span>Model Results</span>
          {isStreaming && (
            <span className="inline-flex items-center gap-1 text-sm font-normal text-vibrant-purple">
              <span className="animate-pulse">⚡</span>
              Streaming...
            </span>
          )}
        </h2>
        <div className="text-sm text-gray-500 dark:text-gray-400">
          {results.length} {results.length === 1 ? 'model' : 'models'}
        </div>
      </div>

      {/* Result Cards */}
      {results.map((result, index) => (
        <ModelResultCard key={result.modelId} result={result} index={index} />
      ))}

      {/* Loading Indicator for Streaming */}
      {isStreaming && (
        <div className="glass-card p-6 animate-pulse">
          <div className="flex items-center justify-center gap-3">
            <div className="w-2 h-2 bg-vibrant-purple rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 bg-vibrant-pink rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 bg-vibrant-blue rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
        </div>
      )}
    </div>
  );
}
