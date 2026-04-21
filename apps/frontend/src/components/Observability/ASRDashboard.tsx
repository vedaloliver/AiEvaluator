'use client';

import React from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { AdversarialRun } from '@/types/observability';
import { formatDistanceToNow } from 'date-fns';

interface ASRDashboardProps {
  runs: AdversarialRun[];
}

export default function ASRDashboard({ runs }: ASRDashboardProps) {
  // Prepare ASR trend data
  const asrTrendData = runs.slice(-10).map((run) => ({
    timestamp: new Date(run.timestamp).toLocaleTimeString(),
    asr: run.attackSuccessRate * 100, // Convert to percentage
    model: run.modelId,
  }));

  // Prepare vulnerability heatmap by category
  const categoryVulnerabilities = runs.reduce((acc, run) => {
    run.vulnerabilities.forEach((vuln: any) => {
      if (!acc[vuln.category]) {
        acc[vuln.category] = 0;
      }
      acc[vuln.category]++;
    });
    return acc;
  }, {} as Record<string, number>);

  const categoryData = Object.entries(categoryVulnerabilities)
    .map(([category, count]) => ({
      category: category.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
      count,
    }))
    .sort((a, b) => b.count - a.count);

  // Most effective attack strategies
  const strategyEffectiveness = runs.reduce((acc, run) => {
    run.vulnerabilities.forEach((vuln: any) => {
      const strategy = vuln.attackStrategy || 'unknown';
      if (!acc[strategy]) {
        acc[strategy] = { success: 0, total: 0 };
      }
      acc[strategy].success++;
    });
    run.allResults.forEach((result: any) => {
      const strategy = result.attackStrategy || 'unknown';
      if (!acc[strategy]) {
        acc[strategy] = { success: 0, total: 0 };
      }
      acc[strategy].total++;
    });
    return acc;
  }, {} as Record<string, { success: number; total: number }>);

  const strategyData = Object.entries(strategyEffectiveness)
    .map(([strategy, stats]) => ({
      strategy: strategy.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
      effectiveness: stats.total > 0 ? (stats.success / stats.total) * 100 : 0,
      attempts: stats.total,
    }))
    .sort((a, b) => b.effectiveness - a.effectiveness)
    .slice(0, 5);

  const getASRColor = (asr: number) => {
    if (asr < 20) return '#10b981'; // Green - good security
    if (asr < 50) return '#f59e0b'; // Yellow - moderate risk
    return '#ef4444'; // Red - high risk
  };

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow">
          <h4 className="text-sm font-medium text-gray-500 mb-2">Total Suites Run</h4>
          <p className="text-3xl font-bold text-gray-900">{runs.length}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h4 className="text-sm font-medium text-gray-500 mb-2">Avg Attack Success Rate</h4>
          <p className="text-3xl font-bold text-gray-900">
            {runs.length > 0
              ? (
                  (runs.reduce((sum, run) => sum + run.attackSuccessRate, 0) / runs.length) *
                  100
                ).toFixed(1)
              : 0}
            %
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h4 className="text-sm font-medium text-gray-500 mb-2">Total Attacks</h4>
          <p className="text-3xl font-bold text-gray-900">
            {runs.reduce((sum, run) => sum + run.totalAttacks, 0)}
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h4 className="text-sm font-medium text-gray-500 mb-2">Vulnerabilities Found</h4>
          <p className="text-3xl font-bold text-red-600">
            {runs.reduce((sum, run) => sum + run.successfulAttacks, 0)}
          </p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* ASR Trend */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Attack Success Rate Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={asrTrendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" tick={{ fontSize: 12 }} />
              <YAxis
                label={{ value: 'ASR %', angle: -90, position: 'insideLeft' }}
                domain={[0, 100]}
              />
              <Tooltip formatter={(value: number) => `${value.toFixed(1)}%`} />
              <Legend />
              <Line type="monotone" dataKey="asr" stroke="#ef4444" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Vulnerability by Category */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Vulnerabilities by Category</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={categoryData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="category" type="category" width={150} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#ef4444" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Most Effective Attack Strategies */}
        <div className="bg-white p-6 rounded-lg shadow md:col-span-2">
          <h3 className="text-lg font-semibold mb-4">Most Effective Attack Strategies</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={strategyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="strategy" tick={{ fontSize: 12 }} />
              <YAxis
                label={{ value: 'Success Rate %', angle: -90, position: 'insideLeft' }}
                domain={[0, 100]}
              />
              <Tooltip
                formatter={(value: number, name: string) =>
                  name === 'effectiveness' ? `${value.toFixed(1)}%` : value
                }
              />
              <Legend />
              <Bar dataKey="effectiveness" fill="#f59e0b" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Runs Table */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Recent Red Team Runs</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Time
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Model
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Scenario
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Total Attacks
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Successful
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ASR
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {runs.slice(0, 10).map((run) => (
                <tr key={run.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatDistanceToNow(new Date(run.timestamp), { addSuffix: true })}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {run.modelId}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {run.scenarioId}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {run.totalAttacks}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600 font-semibold">
                    {run.successfulAttacks}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                      style={{
                        backgroundColor: `${getASRColor(run.attackSuccessRate * 100)}20`,
                        color: getASRColor(run.attackSuccessRate * 100),
                      }}
                    >
                      {(run.attackSuccessRate * 100).toFixed(1)}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
