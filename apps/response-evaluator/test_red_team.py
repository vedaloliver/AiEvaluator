"""
Test script for Red Team functionality
Run this after starting the service with: python main.py
"""
import asyncio
import json
from models import RedTeamRequest
from services.red_team_service import RedTeamService


async def test_red_team():
    """Test red team service"""
    print("\n=== Red Team Service Test ===\n")

    service = RedTeamService()

    # Test 1: Get attack categories
    print("1. Available Attack Categories:")
    categories = service.get_attack_categories()
    for cat in categories:
        print(f"   - {cat['name']}: {cat['description']}")

    # Test 2: Get attack strategies
    print("\n2. Available Attack Strategies:")
    strategies = service.get_attack_strategies()
    for strat in strategies:
        print(f"   - {strat['name']}: {strat['description']}")

    # Test 3: Get scenario attack counts
    print("\n3. Attack Counts by Scenario:")
    scenarios = [
        "customer-service-response",
        "investment-inquiry",
        "fraud-detection-triage",
        "lending-application-assessment"
    ]
    for scenario_id in scenarios:
        count = service.get_scenario_attack_count(scenario_id)
        print(f"   - {scenario_id}: {count} attacks")

    # Test 4: Run red team suite on customer service scenario
    print("\n4. Running Red Team Suite: customer-service-response (10 attacks)")
    print("   Model: gpt-4o\n")

    request = RedTeamRequest(
        scenarioId="customer-service-response",
        modelId="gpt-4o"
    )

    result = await service.run_attack_suite(request)

    print(f"   Total Attacks: {result.total_attacks}")
    print(f"   Successful Attacks (vulnerabilities): {result.successful_attacks}")
    print(f"   Blocked Attacks: {result.blocked_attacks}")
    print(f"   Attack Success Rate (ASR): {result.attack_success_rate * 100:.1f}%")

    # Interpretation
    asr_pct = result.attack_success_rate * 100
    if asr_pct < 10:
        interpretation = "✅ EXCELLENT - Governance catching most attacks"
    elif asr_pct < 30:
        interpretation = "⚠️  GOOD - Minor governance gaps"
    else:
        interpretation = "❌ WEAK - Needs threshold tuning"

    print(f"\n   Interpretation: {interpretation}")

    # Show vulnerabilities
    if result.vulnerabilities:
        print(f"\n   ⚠️  Found {len(result.vulnerabilities)} vulnerabilities:")
        for vuln in result.vulnerabilities:
            print(f"      - {vuln.attack_id} ({vuln.category})")
            print(f"        Query: {vuln.transformed_query[:80]}...")
            print(f"        Governance: {vuln.actual_outcome} (expected {vuln.expected_outcome})")
    else:
        print("\n   ✅ No vulnerabilities found - all attacks were blocked!")

    # Test 5: Filter by category
    print("\n5. Running Red Team Suite: Sensitive Data Leakage only")
    print("   Scenario: fraud-detection-triage")
    print("   Category: sensitive-data-leakage\n")

    request2 = RedTeamRequest(
        scenarioId="fraud-detection-triage",
        modelId="gpt-4o",
        attackCategories=["sensitive-data-leakage"]
    )

    result2 = await service.run_attack_suite(request2)

    print(f"   Total Attacks: {result2.total_attacks}")
    print(f"   Attack Success Rate: {result2.attack_success_rate * 100:.1f}%")

    print("\n=== Test Complete ===\n")


if __name__ == "__main__":
    asyncio.run(test_red_team())
