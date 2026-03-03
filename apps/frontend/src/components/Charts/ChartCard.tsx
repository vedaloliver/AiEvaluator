'use client';

import { ReactNode } from 'react';

interface ChartCardProps {
  title: string;
  icon?: string;
  children: ReactNode;
}

export default function ChartCard({ title, icon, children }: ChartCardProps) {
  return (
    <div className="glass-card p-6 animate-slide-in">
      <div className="flex items-center gap-2 mb-4">
        {icon && <span className="text-2xl">{icon}</span>}
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          {title}
        </h3>
      </div>
      <div className="w-full">
        {children}
      </div>
    </div>
  );
}
