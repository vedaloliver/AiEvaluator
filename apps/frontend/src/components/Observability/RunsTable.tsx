'use client';

import React, { useState } from 'react';
import { EvaluationRun } from '@/types/observability';
import { formatDistanceToNow } from 'date-fns';

interface RunsTableProps {
  runs: EvaluationRun[];
  onRunClick?: (run: EvaluationRun) => void;
}

export default function RunsTable({ runs, onRunClick }: RunsTableProps) {
  const [sortField, setSortField] = useState<keyof EvaluationRun>('timestamp');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');

  const handleSort = (field: keyof EvaluationRun) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  const sortedRuns = [...runs].sort((a, b) => {
    const aVal = a[sortField];
    const bVal = b[sortField];

    if (typeof aVal === 'number' && typeof bVal === 'number') {
      return sortDirection === 'asc' ? aVal - bVal : bVal - aVal;
    }

    if (typeof aVal === 'string' && typeof bVal === 'string') {
      return sortDirection === 'asc'
        ? aVal.localeCompare(bVal)
        : bVal.localeCompare(aVal);
    }

    return 0;
  });

  const getDecisionBadgeColor = (decision: string) => {
    switch (decision?.toUpperCase()) {
      case 'PASS':
        return 'bg-green-100 text-green-800';
      case 'WARN':
        return 'bg-yellow-100 text-yellow-800';
      case 'FAIL':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              onClick={() => handleSort('timestamp')}
            >
              Timestamp {sortField === 'timestamp' && (sortDirection === 'asc' ? '↑' : '↓')}
            </th>
            <th
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              onClick={() => handleSort('modelId')}
            >
              Model {sortField === 'modelId' && (sortDirection === 'asc' ? '↑' : '↓')}
            </th>
            <th
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              onClick={() => handleSort('scenarioId')}
            >
              Scenario {sortField === 'scenarioId' && (sortDirection === 'asc' ? '↑' : '↓')}
            </th>
            <th
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              onClick={() => handleSort('durationMs')}
            >
              Duration {sortField === 'durationMs' && (sortDirection === 'asc' ? '↑' : '↓')}
            </th>
            <th
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              onClick={() => handleSort('totalTokens')}
            >
              Tokens {sortField === 'totalTokens' && (sortDirection === 'asc' ? '↑' : '↓')}
            </th>
            <th
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              onClick={() => handleSort('estimatedCost')}
            >
              Cost {sortField === 'estimatedCost' && (sortDirection === 'asc' ? '↑' : '↓')}
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Decision
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {sortedRuns.map((run) => (
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
                {run.durationMs}ms
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {run.totalTokens?.toLocaleString() || 'N/A'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {run.estimatedCost ? `$${run.estimatedCost.toFixed(6)}` : 'N/A'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span
                  className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getDecisionBadgeColor(
                    run.governanceDecision?.decision || run.governanceDecision?.status
                  )}`}
                >
                  {run.governanceDecision?.decision || run.governanceDecision?.status || 'UNKNOWN'}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {onRunClick && (
                  <button
                    onClick={() => onRunClick(run)}
                    className="text-blue-600 hover:text-blue-900"
                  >
                    View Details
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {runs.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No evaluation runs found
        </div>
      )}
    </div>
  );
}
