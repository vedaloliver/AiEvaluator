import {
  GovernanceDecision,
  GovernanceThresholds,
  MetricStatus,
  EvaluationMetrics,
  SafetyFlag,
} from '@ai-evaluator/shared-types';

export class GovernanceService {
  /**
   * Evaluates a single metric score against thresholds
   */
  private evaluateMetric(
    score: number,
    thresholds: { pass: number; warn: number }
  ): MetricStatus {
    if (score >= thresholds.pass) {
      return 'PASS';
    }
    if (score >= thresholds.warn) {
      return 'WARN';
    }
    return 'FAIL';
  }

  /**
   * Checks if any critical flags are present in the evaluation
   */
  private checkCriticalFlags(
    evaluations: EvaluationMetrics,
    criticalFlags: SafetyFlag[],
    criticalSeverities: string[]
  ): string[] {
    const detectedFlags: string[] = [];

    // Check if safety evaluation indicates critical severity
    if (
      evaluations.safety.severity &&
      criticalSeverities.includes(evaluations.safety.severity.toLowerCase())
    ) {
      const matchingFlag = criticalFlags.find(
        (flag) => evaluations.safety.rationale.toLowerCase().includes(flag.name.toLowerCase())
      );
      if (matchingFlag) {
        detectedFlags.push(matchingFlag.name);
      } else {
        detectedFlags.push(`Critical safety concern: ${evaluations.safety.severity}`);
      }
    }

    // Check for specific flag keywords in rationales
    criticalFlags.forEach((flag) => {
      if (criticalSeverities.includes(flag.severity.toLowerCase())) {
        const searchText = `${evaluations.safety.rationale} ${evaluations.relevance.rationale}`.toLowerCase();
        if (searchText.includes(flag.name.toLowerCase()) || searchText.includes(flag.id.toLowerCase())) {
          if (!detectedFlags.includes(flag.name)) {
            detectedFlags.push(flag.name);
          }
        }
      }
    });

    return detectedFlags;
  }

  /**
   * Makes governance decision based on evaluation scores and thresholds
   */
  public makeDecision(
    evaluations: EvaluationMetrics,
    thresholds: GovernanceThresholds,
    criticalFlags: SafetyFlag[] = []
  ): GovernanceDecision {
    const reasons: string[] = [];

    // Check for critical flags first (auto-FAIL)
    const detectedCriticalFlags = this.checkCriticalFlags(
      evaluations,
      criticalFlags,
      thresholds.criticalSeverities || ['critical', 'high']
    );

    if (detectedCriticalFlags.length > 0) {
      return {
        status: 'FAIL',
        reasons: ['Critical safety flags detected'],
        criticalFlags: detectedCriticalFlags,
        metricDecisions: {
          safety: this.evaluateMetric(evaluations.safety.score, thresholds.safety),
          relevance: this.evaluateMetric(evaluations.relevance.score, thresholds.relevance),
          coherence: this.evaluateMetric(evaluations.coherence.score, thresholds.coherence),
          fluency: this.evaluateMetric(evaluations.fluency.score, thresholds.fluency),
        },
      };
    }

    // Evaluate each metric
    const metricDecisions = {
      safety: this.evaluateMetric(evaluations.safety.score, thresholds.safety),
      relevance: this.evaluateMetric(evaluations.relevance.score, thresholds.relevance),
      coherence: this.evaluateMetric(evaluations.coherence.score, thresholds.coherence),
      fluency: this.evaluateMetric(evaluations.fluency.score, thresholds.fluency),
    };

    // Track which metrics failed or warned
    const failedMetrics: string[] = [];
    const warnedMetrics: string[] = [];

    Object.entries(metricDecisions).forEach(([metric, status]) => {
      if (status === 'FAIL') {
        failedMetrics.push(metric);
      } else if (status === 'WARN') {
        warnedMetrics.push(metric);
      }
    });

    // Determine overall status
    let overallStatus: 'PASS' | 'WARN' | 'FAIL';

    if (failedMetrics.length > 0) {
      overallStatus = 'FAIL';
      reasons.push(`Failed metrics: ${failedMetrics.join(', ')}`);
    } else if (warnedMetrics.length > 0) {
      overallStatus = 'WARN';
      reasons.push(`Warning metrics: ${warnedMetrics.join(', ')}`);
    } else {
      overallStatus = 'PASS';
      reasons.push('All metrics passed thresholds');
    }

    return {
      status: overallStatus,
      reasons,
      criticalFlags: detectedCriticalFlags,
      metricDecisions,
    };
  }

  /**
   * Provides explanation for a governance decision
   */
  public explainDecision(decision: GovernanceDecision): string {
    let explanation = `Governance Decision: ${decision.status}\n\n`;

    if (decision.criticalFlags.length > 0) {
      explanation += `Critical Flags: ${decision.criticalFlags.join(', ')}\n`;
    }

    if (decision.metricDecisions) {
      explanation += '\nMetric Decisions:\n';
      Object.entries(decision.metricDecisions).forEach(([metric, status]) => {
        explanation += `  - ${metric}: ${status}\n`;
      });
    }

    explanation += `\nReasons:\n${decision.reasons.map(r => `  - ${r}`).join('\n')}`;

    return explanation;
  }
}
