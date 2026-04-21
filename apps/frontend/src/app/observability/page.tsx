'use client';

import React, { useState, useEffect } from 'react';
import { observabilityApiClient } from '@/lib/observability-api-client';
import { EvaluationRun, AdversarialRun, AnalyticsSummary } from '@/types/observability';
import RunsTable from '@/components/Observability/RunsTable';
import MetricsCharts from '@/components/Observability/MetricsCharts';
import ASRDashboard from '@/components/Observability/ASRDashboard';
import TraceViewer from '@/components/Observability/TraceViewer';

type TabType = 'evaluation' | 'adversarial' | 'traces';

export default function ObservabilityPage() {
  const [activeTab, setActiveTab] = useState<TabType>('evaluation');
  const [evaluationRuns, setEvaluationRuns] = useState<EvaluationRun[]>([]);
  const [adversarialRuns, setAdversarialRuns] = useState<AdversarialRun[]>([]);
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedTraceId, setSelectedTraceId] = useState<string | undefined>();

  // Filters
  const [modelFilter, setModelFilter] = useState('');
  const [scenarioFilter, setScenarioFilter] = useState('');

  useEffect(() => {
    loadData();
  }, [modelFilter, scenarioFilter]);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const filters = {
        modelId: modelFilter || undefined,
        scenarioId: scenarioFilter || undefined,
        limit: 100,
      };

      const [evalRuns, advRuns, summaryData] = await Promise.all([
        observabilityApiClient.getEvaluationRuns(filters),
        observabilityApiClient.getAdversarialRuns(filters),
        observabilityApiClient.getAnalyticsSummary(filters),
      ]);

      setEvaluationRuns(evalRuns);
      setAdversarialRuns(advRuns);
      setSummary(summaryData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleRunClick = (run: EvaluationRun) => {
    if (run.traceId) {
      setSelectedTraceId(run.traceId);
      setActiveTab('traces');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Observability Dashboard</h1>
          <p className="text-gray-600">
            Monitor LLM evaluation metrics, costs, and red team testing results
          </p>
        </div>

        {/* Summary Cards */}
        {summary && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-sm font-medium text-gray-500 mb-2">Total Evaluations</h3>
              <p className="text-3xl font-bold text-gray-900">
                {summary.evaluationRuns.totalRuns}
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-sm font-medium text-gray-500 mb-2">Avg Latency</h3>
              <p className="text-3xl font-bold text-gray-900">
                {summary.evaluationRuns.avgLatencyMs.toFixed(0)}ms
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-sm font-medium text-gray-500 mb-2">Total Cost</h3>
              <p className="text-3xl font-bold text-gray-900">
                ${summary.evaluationRuns.totalCost.toFixed(4)}
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-sm font-medium text-gray-500 mb-2">Total Tokens</h3>
              <p className="text-3xl font-bold text-gray-900">
                {summary.evaluationRuns.totalTokens.toLocaleString()}
              </p>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h3 className="text-lg font-semibold mb-4">Filters</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Model ID
              </label>
              <input
                type="text"
                value={modelFilter}
                onChange={(e) => setModelFilter(e.target.value)}
                placeholder="Filter by model..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Scenario ID
              </label>
              <input
                type="text"
                value={scenarioFilter}
                onChange={(e) => setScenarioFilter(e.target.value)}
                placeholder="Filter by scenario..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div className="flex items-end">
              <button
                onClick={loadData}
                disabled={loading}
                className="w-full px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {loading ? 'Loading...' : 'Apply Filters'}
              </button>
            </div>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('evaluation')}
                className={`px-6 py-3 border-b-2 font-medium text-sm ${
                  activeTab === 'evaluation'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Evaluation Runs
              </button>
              <button
                onClick={() => setActiveTab('adversarial')}
                className={`px-6 py-3 border-b-2 font-medium text-sm ${
                  activeTab === 'adversarial'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Red Team Tests
              </button>
              <button
                onClick={() => setActiveTab('traces')}
                className={`px-6 py-3 border-b-2 font-medium text-sm ${
                  activeTab === 'traces'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Trace Viewer
              </button>
            </nav>
          </div>

          <div className="p-6">
            {/* Evaluation Runs Tab */}
            {activeTab === 'evaluation' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold mb-4">Evaluation Metrics</h2>
                  <MetricsCharts runs={evaluationRuns} />
                </div>
                <div>
                  <h2 className="text-2xl font-bold mb-4">Recent Evaluation Runs</h2>
                  <RunsTable runs={evaluationRuns} onRunClick={handleRunClick} />
                </div>
              </div>
            )}

            {/* Adversarial Runs Tab */}
            {activeTab === 'adversarial' && (
              <div>
                <h2 className="text-2xl font-bold mb-4">Red Team Testing Dashboard</h2>
                <ASRDashboard runs={adversarialRuns} />
              </div>
            )}

            {/* Trace Viewer Tab */}
            {activeTab === 'traces' && (
              <div>
                <h2 className="text-2xl font-bold mb-4">End-to-End Trace Visualization</h2>
                <TraceViewer traceId={selectedTraceId} />
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-gray-500 text-sm mt-8">
          Data refreshes when filters are applied. All times shown in local timezone.
        </div>
      </div>
    </div>
  );
}
