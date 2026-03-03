'use client';

import {
  Radar,
  RadarChart as RechartsRadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts';
import { RadarDataPoint, getModelColor, getModelDisplayName } from '@/lib/chart-utils';

interface RadarChartProps {
  data: RadarDataPoint[];
  modelIds: string[];
}

export default function RadarChart({ data, modelIds }: RadarChartProps) {
  if (data.length === 0 || modelIds.length === 0) {
    return null;
  }

  return (
    <ResponsiveContainer width="100%" height="100%">
      <RechartsRadarChart data={data}>
        <PolarGrid stroke="#ffffff20" />
        <PolarAngleAxis
          dataKey="metric"
          tick={{ fill: '#9ca3af', fontSize: 12 }}
        />
        <PolarRadiusAxis
          domain={[0, 100]}
          tick={{ fill: '#9ca3af', fontSize: 10 }}
          axisLine={false}
        />
        {modelIds.map((modelId, index) => (
          <Radar
            key={modelId}
            name={getModelDisplayName(modelId)}
            dataKey={modelId}
            stroke={getModelColor(index)}
            fill={getModelColor(index)}
            fillOpacity={0.25}
            strokeWidth={2}
          />
        ))}
        <Legend
          wrapperStyle={{
            paddingTop: '20px',
            fontSize: '12px',
          }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            border: 'none',
            borderRadius: '8px',
            color: '#fff',
          }}
        />
      </RechartsRadarChart>
    </ResponsiveContainer>
  );
}
