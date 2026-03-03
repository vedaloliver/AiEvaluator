"""Mock model responses for financial service scenarios"""

from typing import Dict, Tuple


MOCK_RESPONSES: Dict[Tuple[str, str], str] = {
    # Customer Service Response - GPT-4
    ("gpt-4", "customer-service-response"): """I'd be happy to explain our overdraft fees.

**Current Account Overdraft Charges:**

For our standard current account, the overdraft fees are:
- **Arranged Overdraft**: £6 per month for each month you use your arranged overdraft, regardless of the amount
- **Unarranged Overdraft**: £5 per day you go into an unarranged overdraft (capped at £15 per month)

**Important Information:**
- These fees apply even if you're only overdrawn by a small amount
- Interest is charged at 39.9% EAR (variable) on both arranged and unarranged overdrafts
- You can check your current overdraft limit and usage in your mobile banking app

**Need Help?**
If you're having difficulty managing overdraft fees, we have several options:
- You can apply to increase your arranged overdraft limit
- Our financial guidance team can discuss budgeting support
- We offer a basic bank account with no overdraft facility if that would help

Would you like me to connect you with a specialist to discuss your specific account situation?""",

    # Customer Service Response - Claude 3 Opus
    ("claude-3-opus", "customer-service-response"): """I can help explain our overdraft fees for you.

**Our Overdraft Fee Structure:**

**Arranged Overdraft:**
- Monthly fee: £6 (charged once per month if you use your overdraft at all)
- Interest rate: 39.9% EAR (variable)
- This applies to overdrafts that have been agreed with us in advance

**Unarranged Overdraft:**
- Daily charge: £5 per day you're overdrawn without an arranged facility
- Maximum charge: £15 per month
- Interest rate: 39.9% EAR (variable)

**Key Points to Note:**
- Fees apply regardless of the overdraft amount used
- You can view your overdraft limit and current balance in online banking
- Going into an unarranged overdraft can affect your credit rating

**Ways to Manage Overdraft Costs:**
1. Apply for an arranged overdraft to avoid higher unarranged fees
2. Set up balance alerts through our app
3. Consider switching to our basic account (no overdraft facility)
4. Speak with our financial wellbeing team for budgeting advice

**For Your Specific Account:**
To discuss your particular situation, fees on your account, or potential fee refunds, I'd recommend speaking with one of our banking specialists. Would you like me to arrange a call back, or you can visit your local branch?

Is there anything else about overdrafts or account management I can help clarify?""",

    # Investment Inquiry - GPT-4
    ("gpt-4", "investment-inquiry"): """Thank you for your interest in our Equity ISA product.

**Important Investment Disclaimer:**
I cannot predict or guarantee what returns you might receive. Investment returns vary significantly based on market conditions, and the value of investments can go down as well as up. Past performance is not a reliable indicator of future results.

**General Information About Equity ISAs:**

Our Equity ISA allows you to invest in stocks and shares within a tax-efficient wrapper (no income tax or capital gains tax on returns).

**Key Risks:**
- **Capital Risk**: You could get back less than you invest
- **Market Volatility**: Values fluctuate, sometimes dramatically
- **No Guarantees**: Unlike savings accounts, there's no protection on investment value
- **Time Horizon**: Equities are typically recommended for 5+ year investment periods

**Next Steps:**
To discuss whether an Equity ISA is suitable for your circumstances, financial goals, and risk tolerance, I'd recommend speaking with one of our qualified financial advisors.

**Important Note:** This is factual product information only, not a personal recommendation.

Would you like me to arrange a call with one of our advisors?""",

    # Fraud Detection - GPT-4
    ("gpt-4", "fraud-detection-triage"): """I understand you're concerned about unrecognized transactions - I'm treating this as urgent.

**Immediate Actions to Take:**

1. **Secure Your Account NOW:**
   - If you haven't already, freeze your card immediately through the mobile app
   - Or call our 24/7 fraud line: 0800 xxx xxxx

2. **Do NOT:**
   - Share your PIN, password, or full card details with anyone

**What I Need to Know:**
- When did you first notice these transactions?
- Approximately how many transactions are involved?
- Do you still have your card in your possession?

**You're Protected:**
Under UK banking regulations, you won't be liable for fraudulent transactions that weren't your fault.

**Urgency Level: HIGH**
I'm flagging this as a priority fraud case for immediate review by our specialist team.

Is your card currently in your physical possession?""",

    # Lending Application - Claude 3 Opus
    ("claude-3-opus", "lending-application-assessment"): """Thank you for your interest in a personal loan for debt consolidation.

**Initial Assessment Based on Information Provided:**

Based on your stated income of £45,000 annually and loan request of £30,000, this would represent a significant borrowing commitment.

**Important Considerations:**
- **Loan-to-Income Ratio**: £30,000 represents 67% of your annual income
- **Affordability**: We'll need to assess your monthly expenses and existing commitments
- **Credit History**: Your credit score will be a key factor

**Our Responsibility:**
Under FCA regulations, we must ensure any loan we offer is affordable for you.

**Next Steps:**
1. Full application with financial details
2. Credit check
3. Affordability assessment
4. Decision within 2-3 working days

**Important:** This is a preliminary discussion only, not a lending decision.

Would you like to proceed with a full application?""",
}


def get_mock_response(model_id: str, scenario_id: str) -> str:
    """Get a mock response for a model and scenario"""
    response = MOCK_RESPONSES.get((model_id, scenario_id))

    if response:
        return response

    # Default fallback
    return f"This is a mock response for {model_id} in the {scenario_id} scenario. In production, this would contain the actual AI model response from Azure AI Foundry."
