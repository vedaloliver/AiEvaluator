'use client';

import { useState } from 'react';
import { EvaluationResult } from '@ai-evaluator/shared-types';
import RadarChart from '@/components/Charts/RadarChart';
import ComparisonBarChart from '@/components/Charts/ComparisonBarChart';
import EmptyChartPlaceholder from '@/components/Cards/EmptyChartPlaceholder';
import { transformToRadarData, transformToBarData } from '@/lib/chart-utils';

interface ChartAreaProps {
  results: EvaluationResult[];
}

export default function ChartArea({ results }: ChartAreaProps) {
  const [activeTab, setActiveTab] = useState<'radar' | 'bar'>('radar');
  const hasResults = results.length > 0;
  const radarData = hasResults ? transformToRadarData(results) : [];
  const barData = hasResults ? transformToBarData(results) : [];
  const modelIds = hasResults ? results.map((r) => r.modelId) : [];

  return (
    <div className="h-full flex flex-col">
      {/* Tab Navigation */}
      <div className="flex gap-2 mb-4 px-6 pt-6">
        <button
          onClick={() => setActiveTab('radar')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
            activeTab === 'radar'
              ? 'glass-card border-vibrant-purple'
              : 'bg-white/5 hover:bg-white/10 border border-white/10'
          }`}
        >
          🕸️ Multi-Metric
        </button>
        <button
          onClick={() => setActiveTab('bar')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
            activeTab === 'bar'
              ? 'glass-card border-vibrant-purple'
              : 'bg-white/5 hover:bg-white/10 border border-white/10'
          }`}
        >
          📊 Side-by-Side
        </button>
      </div>

      {/* Chart Content */}
      <div className="flex-1 px-6 pb-6 overflow-hidden">
        {activeTab === 'radar' && (
          <div className="glass-card p-6 h-full flex flex-col animate-fade-in">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <span>🕸️</span>
              Multi-Metric Comparison
            </h3>
            {hasResults ? (
              <div className="flex-1">
                <RadarChart data={radarData} modelIds={modelIds} />
              </div>
            ) : (
              <div className="flex-1 flex items-center justify-center">
                <EmptyChartPlaceholder title="Multi-Metric Radar" icon="🕸️" />
              </div>
            )}
          </div>
        )}

        {activeTab === 'bar' && (
          <div className="glass-card p-6 h-full flex flex-col animate-fade-in">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <span>📊</span>
              Side-by-Side Comparison
            </h3>
            {hasResults ? (
              <div className="flex-1">
                <ComparisonBarChart data={barData} modelIds={modelIds} />
              </div>
            ) : (
              <div className="flex-1 flex items-center justify-center">
                <EmptyChartPlaceholder title="Bar Chart Comparison" icon="📊" />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
