'use client';

import { EvaluationResult, ScenarioListItem } from '@ai-evaluator/shared-types';
import TopControlBar from './TopControlBar';
import ChartArea from './ChartArea';
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
  const displayResults = isStreaming ? streamingResults : results;

  return (
    <div className="min-h-screen">
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

      {/* Main Dashboard Grid */}
      <div className="pt-20 px-4 h-screen">
        <div className="grid grid-cols-1 lg:grid-cols-[60%_40%] gap-4 h-[calc(100vh-5.5rem)]">
          {/* Left: Chart Area */}
          <div className="overflow-hidden">
            <ChartArea results={displayResults} />
          </div>

          {/* Right: Results Stream */}
          <div className="overflow-hidden">
            <ResultsStream results={displayResults} isStreaming={isStreaming} />
          </div>
        </div>
      </div>
    </div>
  );
}
