'use client';

interface EmptyChartPlaceholderProps {
  title: string;
  icon?: string;
}

export default function EmptyChartPlaceholder({
  title,
  icon = '📊',
}: EmptyChartPlaceholderProps) {
  return (
    <div className="flex flex-col items-center justify-center h-full animate-fade-in">
      <div className="text-6xl mb-4 opacity-50">{icon}</div>
      <h3 className="text-lg font-semibold text-gray-600 dark:text-gray-400 mb-2">
        {title}
      </h3>
      <p className="text-sm text-gray-500 dark:text-gray-500">
        Run an evaluation to see results
      </p>
    </div>
  );
}
