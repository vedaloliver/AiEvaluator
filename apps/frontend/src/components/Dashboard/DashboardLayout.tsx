'use client';

import { useState } from 'react';
import { EvaluationResult, ScenarioListItem } from '@ai-evaluator/shared-types';
import TopControlBar from './TopControlBar';
import MainTabNavigation from './MainTabNavigation';
import ModelComparisonView from './ModelComparisonView';
import IndividualModelView from './IndividualModelView';
import ResultsStream from './ResultsStream';

interface DashboardLayoutProps {
  scenarios: ScenarioListItem[];
  selectedScenarioId: string;
  query: string;
  results: EvaluationResult[];
  isLoading: boolean;
  isStreaming: boolean;
  streamingResults: EvaluationResult[];
  onSelectScenario: (id: string) => void;
  onQueryChange: (query: string) => void;
  onEvaluate: () => void;
}

export default function DashboardLayout({
  scenarios,
  selectedScenarioId,
  query,
  results,
  isLoading,
  isStreaming,
  streamingResults,
  onSelectScenario,
  onQueryChange,
  onEvaluate,
}: DashboardLayoutProps) {
  const [mainTab, setMainTab] = useState<'comparison' | 'individual'>('comparison');
  const displayResults = isStreaming ? streamingResults : results;

  return (
    <div className="flex flex-col h-screen">
      {/* Top Control Bar */}
      <TopControlBar
        scenarios={scenarios}
        selectedScenarioId={selectedScenarioId}
        query={query}
        isLoading={isLoading}
        onSelectScenario={onSelectScenario}
        onQueryChange={onQueryChange}
        onEvaluate={onEvaluate}
      />

      {/* Main Content Area */}
      <div className="flex-1 overflow-hidden pt-20">
        {/* Main Tab Navigation */}
        <div className="pt-6">
          <MainTabNavigation
            activeTab={mainTab}
            onTabChange={setMainTab}
            hasResults={displayResults.length > 0}
          />
        </div>

        {/* Content Views */}
        <div className="h-[calc(100%-120px)] overflow-hidden">
          {mainTab === 'comparison' && (
            <div className="grid grid-cols-1 lg:grid-cols-[60%_40%] gap-4 h-full px-4">
              {/* Left: Model Comparison View */}
              <div className="overflow-hidden min-h-0">
                <ModelComparisonView results={displayResults} />
              </div>

              {/* Right: Results Stream */}
              <div className="overflow-hidden min-h-0">
                <ResultsStream results={displayResults} isStreaming={isStreaming} />
              </div>
            </div>
          )}

          {mainTab === 'individual' && (
            <div className="h-full px-4 animate-fade-in">
              <IndividualModelView results={displayResults} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
