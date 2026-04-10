'use client';

import { EvaluationResult } from '@ai-evaluator/shared-types';
import MetricCard from '@/components/EvaluationMetrics/MetricCard';

interface CustomEvaluatorsTabProps {
  result: EvaluationResult;
}

export default function CustomEvaluatorsTab({ result }: CustomEvaluatorsTabProps) {
  const { evaluations, governanceDecision } = result;

  return (
    <div className="h-full overflow-y-auto">
      <div className="p-6">
        <div className="mb-6">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
            Custom Domain Evaluators
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            FCA-specific evaluation metrics for compliance and risk assessment
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <MetricCard
            name="Disclaimer Compliance"
            evaluation={evaluations.disclaimerCompliance}
            status={governanceDecision.metricDecisions?.disclaimerCompliance}
          />
          <MetricCard
            name="Prohibited Language"
            evaluation={evaluations.prohibitedLanguage}
            status={governanceDecision.metricDecisions?.prohibitedLanguage}
          />
          <MetricCard
            name="Suitability Assessment"
            evaluation={evaluations.suitabilityAssessment}
            status={governanceDecision.metricDecisions?.suitabilityAssessment}
          />
          <MetricCard
            name="Risk Disclosure"
            evaluation={evaluations.riskDisclosure}
            status={governanceDecision.metricDecisions?.riskDisclosure}
          />
        </div>
      </div>
    </div>
  );
}
