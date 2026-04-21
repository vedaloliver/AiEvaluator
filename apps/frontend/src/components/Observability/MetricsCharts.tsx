'use client';

import React from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { EvaluationRun } from '@/types/observability';

interface MetricsChartsProps {
  runs: EvaluationRun[];
}

export default function MetricsCharts({ runs }: MetricsChartsProps) {
  // Prepare latency over time data
  const latencyData = runs
    .slice(-20) // Last 20 runs
    .map((run) => ({
      timestamp: new Date(run.timestamp).toLocaleTimeString(),
      latency: run.durationMs,
      model: run.modelId,
    }));

  // Prepare cost accumulation data
  const costData = runs
    .slice(-20)
    .reduce((acc, run, index) => {
      const prevCost = index > 0 ? acc[index - 1].cost : 0;
      acc.push({
        timestamp: new Date(run.timestamp).toLocaleTimeString(),
        cost: prevCost + (run.estimatedCost || 0),
      });
      return acc;
    }, [] as { timestamp: string; cost: number }[]);

  // Prepare token usage by model
  const tokensByModel = runs.reduce((acc, run) => {
    if (!acc[run.modelId]) {
      acc[run.modelId] = 0;
    }
    acc[run.modelId] += run.totalTokens || 0;
    return acc;
  }, {} as Record<string, number>);

  const tokenData = Object.entries(tokensByModel).map(([model, tokens]) => ({
    model,
    tokens,
  }));

  // Prepare decision distribution
  const decisionCounts = runs.reduce((acc, run) => {
    const decision = run.governanceDecision?.decision || run.governanceDecision?.status || 'UNKNOWN';
    if (!acc[decision]) {
      acc[decision] = 0;
    }
    acc[decision]++;
    return acc;
  }, {} as Record<string, number>);

  const decisionData = Object.entries(decisionCounts).map(([decision, count]) => ({
    name: decision,
    value: count,
  }));

  const COLORS = {
    PASS: '#10b981',
    WARN: '#f59e0b',
    FAIL: '#ef4444',
    UNKNOWN: '#6b7280',
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Latency Over Time */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Latency Over Time</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={latencyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="timestamp" tick={{ fontSize: 12 }} />
            <YAxis label={{ value: 'ms', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="latency" stroke="#3b82f6" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Cumulative Cost */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Cumulative Cost</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={costData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="timestamp" tick={{ fontSize: 12 }} />
            <YAxis label={{ value: 'USD', angle: -90, position: 'insideLeft' }} />
            <Tooltip formatter={(value: number) => `$${value.toFixed(4)}`} />
            <Legend />
            <Line type="monotone" dataKey="cost" stroke="#10b981" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Token Usage by Model */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Token Usage by Model</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={tokenData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="model" tick={{ fontSize: 12 }} />
            <YAxis label={{ value: 'Tokens', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Bar dataKey="tokens" fill="#8b5cf6" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Decision Distribution */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Governance Decision Distribution</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={decisionData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={(entry) => `${entry.name}: ${entry.value}`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {decisionData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[entry.name as keyof typeof COLORS] || COLORS.UNKNOWN} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
