'use client';

import { useState } from 'react';
import { EvaluationResult } from '@ai-evaluator/shared-types';
import ModelDetailsTab from '@/components/ModelPerformance/ModelDetailsTab';
import PrebuiltEvaluatorsTab from '@/components/ModelPerformance/PrebuiltEvaluatorsTab';
import CustomEvaluatorsTab from '@/components/ModelPerformance/CustomEvaluatorsTab';
import ResponseTab from '@/components/ModelPerformance/ResponseTab';
import GovernanceDecisionBadge from '@/components/EvaluationMetrics/GovernanceDecisionBadge';

interface IndividualModelViewProps {
  results: EvaluationResult[];
}

type PerformanceTab = 'details' | 'prebuilt' | 'custom' | 'response';

export default function IndividualModelView({ results }: IndividualModelViewProps) {
  const [selectedModelId, setSelectedModelId] = useState<string | null>(
    results.length > 0 ? results[0].modelId : null
  );
  const [activeTab, setActiveTab] = useState<PerformanceTab>('details');

  const selectedResult = results.find((r) => r.modelId === selectedModelId);

  if (results.length === 0) {
    return (
      <div className="glass-card p-8 h-full flex items-center justify-center">
        <div className="text-center">
          <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
            🎯 Individual Model Performance
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Run an evaluation to view detailed per-model analysis
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col min-h-0">
      {/* Model Selector */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 px-6">
          Select Model
        </h3>
        <div className="flex gap-3 px-6 overflow-x-auto pb-2">
          {results.map((result) => (
            <button
              key={result.modelId}
              onClick={() => setSelectedModelId(result.modelId)}
              className={`px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 whitespace-nowrap flex items-center gap-2 ${
                selectedModelId === result.modelId
                  ? 'glass-card border-vibrant-purple shadow-lg ring-2 ring-vibrant-purple/30'
                  : 'bg-white/5 hover:bg-white/10 border border-white/10'
              }`}
            >
              <span>{result.modelId}</span>
              <GovernanceDecisionBadge
                status={result.governanceDecision.status}
                size="sm"
              />
            </button>
          ))}
        </div>
      </div>

      {/* Performance Sub-tabs */}
      {selectedResult && (
        <>
          <div className="flex gap-2 mb-4 px-6">
            <button
              onClick={() => setActiveTab('details')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                activeTab === 'details'
                  ? 'glass-card border-vibrant-purple'
                  : 'bg-white/5 hover:bg-white/10 border border-white/10'
              }`}
            >
              📋 Details
            </button>
            <button
              onClick={() => setActiveTab('prebuilt')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                activeTab === 'prebuilt'
                  ? 'glass-card border-vibrant-purple'
                  : 'bg-white/5 hover:bg-white/10 border border-white/10'
              }`}
            >
              🔧 Prebuilt
            </button>
            <button
              onClick={() => setActiveTab('custom')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                activeTab === 'custom'
                  ? 'glass-card border-vibrant-purple'
                  : 'bg-white/5 hover:bg-white/10 border border-white/10'
              }`}
            >
              ⚙️ Custom
            </button>
            <button
              onClick={() => setActiveTab('response')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                activeTab === 'response'
                  ? 'glass-card border-vibrant-purple'
                  : 'bg-white/5 hover:bg-white/10 border border-white/10'
              }`}
            >
              💬 Response
            </button>
          </div>

          {/* Tab Content */}
          <div className="flex-1 overflow-hidden min-h-0">
            <div className="glass-card h-full">
              {activeTab === 'details' && (
                <div className="animate-fade-in h-full">
                  <ModelDetailsTab result={selectedResult} />
                </div>
              )}
              {activeTab === 'prebuilt' && (
                <div className="animate-fade-in h-full">
                  <PrebuiltEvaluatorsTab result={selectedResult} />
                </div>
              )}
              {activeTab === 'custom' && (
                <div className="animate-fade-in h-full">
                  <CustomEvaluatorsTab result={selectedResult} />
                </div>
              )}
              {activeTab === 'response' && (
                <div className="animate-fade-in h-full">
                  <ResponseTab result={selectedResult} />
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
