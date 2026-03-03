import { GovernanceThresholds, SafetyFlag } from './governance';

export type ScenarioCategory = 'financial' | 'medical' | 'legal' | 'hr';

export interface RegulatoryScenario {
  id: string;
  name: string;
  category: ScenarioCategory;
  description: string;
  exampleQuery: string;
  systemPrompt: string;
  criticalFlags: SafetyFlag[];
  customThresholds?: Partial<GovernanceThresholds>;
}

export interface ScenarioListItem {
  id: string;
  name: string;
  category: ScenarioCategory;
  description: string;
  exampleQuery: string;
}
