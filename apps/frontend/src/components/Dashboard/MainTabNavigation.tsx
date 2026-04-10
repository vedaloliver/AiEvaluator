'use client';

interface MainTabNavigationProps {
  activeTab: 'comparison' | 'individual';
  onTabChange: (tab: 'comparison' | 'individual') => void;
  hasResults: boolean;
}

export default function MainTabNavigation({
  activeTab,
  onTabChange,
  hasResults,
}: MainTabNavigationProps) {
  return (
    <div className="flex gap-3 mb-6 px-6">
      <button
        onClick={() => onTabChange('comparison')}
        className={`px-6 py-3 rounded-lg text-base font-medium transition-all duration-200 ${
          activeTab === 'comparison'
            ? 'glass-card border-vibrant-purple shadow-lg'
            : 'bg-white/5 hover:bg-white/10 border border-white/10'
        }`}
      >
        📊 Model Comparison
      </button>
      <button
        onClick={() => onTabChange('individual')}
        disabled={!hasResults}
        className={`px-6 py-3 rounded-lg text-base font-medium transition-all duration-200 ${
          activeTab === 'individual'
            ? 'glass-card border-vibrant-purple shadow-lg'
            : hasResults
            ? 'bg-white/5 hover:bg-white/10 border border-white/10'
            : 'bg-white/5 border border-white/10 opacity-50 cursor-not-allowed'
        }`}
      >
        🎯 Individual Performance
      </button>
    </div>
  );
}
