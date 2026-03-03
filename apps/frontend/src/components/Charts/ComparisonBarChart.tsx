'use client';

import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { BarDataPoint, getModelColor, getModelDisplayName } from '@/lib/chart-utils';

interface ComparisonBarChartProps {
  data: BarDataPoint[];
  modelIds: string[];
}

export default function ComparisonBarChart({ data, modelIds }: ComparisonBarChartProps) {
  if (data.length === 0 || modelIds.length === 0) {
    return null;
  }

  return (
    <ResponsiveContainer width="100%" height="100%">
      <RechartsBarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#ffffff20" />
        <XAxis
          dataKey="metric"
          tick={{ fill: '#9ca3af', fontSize: 12 }}
          axisLine={{ stroke: '#4b5563' }}
        />
        <YAxis
          domain={[0, 100]}
          tick={{ fill: '#9ca3af', fontSize: 12 }}
          axisLine={{ stroke: '#4b5563' }}
          label={{ value: 'Score', angle: -90, position: 'insideLeft', fill: '#9ca3af' }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            border: 'none',
            borderRadius: '8px',
            color: '#fff',
          }}
        />
        <Legend
          wrapperStyle={{
            paddingTop: '10px',
            fontSize: '12px',
          }}
        />
        {modelIds.map((modelId, index) => (
          <Bar
            key={modelId}
            dataKey={modelId}
            name={getModelDisplayName(modelId)}
            fill={getModelColor(index)}
            radius={[8, 8, 0, 0]}
          />
        ))}
      </RechartsBarChart>
    </ResponsiveContainer>
  );
}
