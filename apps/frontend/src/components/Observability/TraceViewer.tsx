'use client';

import React, { useState, useEffect } from 'react';
import { FlowVisualization, SpanNode } from '@/types/observability';
import { observabilityApiClient } from '@/lib/observability-api-client';
import { formatDistanceToNow } from 'date-fns';

interface TraceViewerProps {
  traceId?: string;
}

const SPAN_TYPE_COLORS: Record<string, string> = {
  llm_call: 'bg-blue-500',
  evaluation: 'bg-green-500',
  retrieval: 'bg-purple-500',
  reasoning: 'bg-yellow-500',
  adversarial_test: 'bg-red-500',
};

export default function TraceViewer({ traceId: initialTraceId }: TraceViewerProps) {
  const [traceId, setTraceId] = useState(initialTraceId || '');
  const [flowData, setFlowData] = useState<FlowVisualization | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedSpan, setSelectedSpan] = useState<SpanNode | null>(null);

  useEffect(() => {
    if (initialTraceId) {
      loadTrace(initialTraceId);
    }
  }, [initialTraceId]);

  const loadTrace = async (id: string) => {
    if (!id) return;

    setLoading(true);
    setError(null);
    try {
      const data = await observabilityApiClient.getTraceFlow(id);
      setFlowData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load trace');
      setFlowData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    loadTrace(traceId);
  };

  const renderSpanNode = (span: SpanNode, depth: number = 0, startTime: Date) => {
    const spanStart = new Date(span.startTime);
    const offset = spanStart.getTime() - startTime.getTime();
    const duration = span.durationMs || 0;

    return (
      <div key={span.spanId} style={{ marginLeft: `${depth * 24}px` }} className="mb-2">
        <div
          className={`border rounded-lg p-3 cursor-pointer hover:shadow-md transition-shadow ${
            selectedSpan?.spanId === span.spanId ? 'ring-2 ring-blue-500' : ''
          }`}
          onClick={() => setSelectedSpan(span)}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <span
                className={`px-2 py-1 rounded text-xs font-semibold text-white ${
                  SPAN_TYPE_COLORS[span.spanType] || 'bg-gray-500'
                }`}
              >
                {span.spanType}
              </span>
              <span className="font-medium">{span.name}</span>
            </div>
            <div className="text-sm text-gray-500">
              {duration}ms
              {offset > 0 && ` (+${offset}ms)`}
            </div>
          </div>

          {/* Waterfall bar */}
          <div className="mt-2 relative h-2 bg-gray-100 rounded">
            <div
              className={`absolute h-full rounded ${SPAN_TYPE_COLORS[span.spanType] || 'bg-gray-500'
                }`}
              style={{
                left: `${(offset / (flowData?.rootSpans[0]?.durationMs || 1000)) * 100}%`,
                width: `${(duration / (flowData?.rootSpans[0]?.durationMs || 1000)) * 100}%`,
              }}
            />
          </div>
        </div>

        {/* Render children */}
        {span.children && span.children.length > 0 && (
          <div className="mt-1">
            {span.children.map((child) => renderSpanNode(child, depth + 1, startTime))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Search Form */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Search Trace by ID</h3>
        <form onSubmit={handleSearch} className="flex space-x-4">
          <input
            type="text"
            value={traceId}
            onChange={(e) => setTraceId(e.target.value)}
            placeholder="Enter trace ID"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            type="submit"
            disabled={loading || !traceId}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Loading...' : 'Load Trace'}
          </button>
        </form>
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}
      </div>

      {/* Trace Overview */}
      {flowData && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Trace Overview</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-sm text-gray-500">Trace ID</p>
              <p className="font-mono text-sm">{flowData.traceId.slice(0, 8)}...</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Status</p>
              <span
                className={`px-2 py-1 rounded text-xs font-semibold ${flowData.status === 'completed'
                  ? 'bg-green-100 text-green-800'
                  : flowData.status === 'error'
                    ? 'bg-red-100 text-red-800'
                    : 'bg-yellow-100 text-yellow-800'
                  }`}
              >
                {flowData.status}
              </span>
            </div>
            <div>
              <p className="text-sm text-gray-500">Total Spans</p>
              <p className="font-semibold">{flowData.totalSpans}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Started</p>
              <p className="text-sm">
                {formatDistanceToNow(new Date(flowData.startTime), { addSuffix: true })}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Waterfall View */}
      {flowData && flowData.rootSpans.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Execution Flow (Waterfall View)</h3>
          <div className="space-y-2">
            {flowData.rootSpans.map((span) =>
              renderSpanNode(span, 0, new Date(flowData.startTime))
            )}
          </div>
        </div>
      )}

      {/* Span Details Panel */}
      {selectedSpan && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Span Details</h3>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-500">Span ID</p>
              <p className="font-mono text-sm">{selectedSpan.spanId}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Name</p>
              <p className="font-semibold">{selectedSpan.name}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Type</p>
              <span
                className={`px-2 py-1 rounded text-xs font-semibold text-white ${SPAN_TYPE_COLORS[selectedSpan.spanType] || 'bg-gray-500'
                  }`}
              >
                {selectedSpan.spanType}
              </span>
            </div>
            <div>
              <p className="text-sm text-gray-500">Duration</p>
              <p className="font-semibold">{selectedSpan.durationMs}ms</p>
            </div>
            {selectedSpan.attributes && Object.keys(selectedSpan.attributes).length > 0 && (
              <div>
                <p className="text-sm text-gray-500 mb-2">Attributes</p>
                <pre className="bg-gray-50 p-3 rounded text-xs overflow-x-auto">
                  {JSON.stringify(selectedSpan.attributes, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Legend */}
      {flowData && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4">Span Type Legend</h3>
          <div className="flex flex-wrap gap-4">
            {Object.entries(SPAN_TYPE_COLORS).map(([type, color]) => (
              <div key={type} className="flex items-center space-x-2">
                <span className={`w-4 h-4 rounded ${color}`} />
                <span className="text-sm">{type.replace(/_/g, ' ')}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
