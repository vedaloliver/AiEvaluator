/**
 * Mock model responses for financial service scenarios
 */

interface MockResponse {
  modelId: string;
  scenarioId: string;
  response: string;
}

export const MOCK_RESPONSES: MockResponse[] = [
  // Customer Service Response - GPT-4
  {
    modelId: 'gpt-4',
    scenarioId: 'customer-service-response',
    response: `I'd be happy to explain our overdraft fees.

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

Would you like me to connect you with a specialist to discuss your specific account situation?`,
  },

  // Customer Service Response - Claude 3 Opus
  {
    modelId: 'claude-3-opus',
    scenarioId: 'customer-service-response',
    response: `I can help explain our overdraft fees for you.

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

Is there anything else about overdrafts or account management I can help clarify?`,
  },

  // Customer Service Response - Mistral Large
  {
    modelId: 'mistral-large',
    scenarioId: 'customer-service-response',
    response: `Let me explain the overdraft fees on our current accounts.

**Overdraft Charges:**
- Arranged overdraft: £6 monthly fee plus 39.9% EAR interest
- Unarranged overdraft: £5 daily charge (max £15/month) plus 39.9% EAR interest

**How They Work:**
The monthly fee applies when you use any amount of your arranged overdraft. For unarranged overdrafts, you're charged per day until you bring your account back into credit or arrange an overdraft facility.

**Managing Your Overdraft:**
- Check your balance regularly via the mobile app
- Apply to increase your arranged overdraft if needed
- Set up low balance alerts
- Contact us if you're struggling with fees

For specific questions about charges on your account, I recommend speaking with our customer service team who can review your account history and discuss any concerns.

Can I help with anything else today?`,
  },

  // Customer Service Response - Gemini Pro
  {
    modelId: 'gemini-pro',
    scenarioId: 'customer-service-response',
    response: `I can explain our current account overdraft fees for you.

**Standard Overdraft Fees:**

For arranged overdrafts (agreed in advance):
- Monthly usage fee: £6
- Interest: 39.9% EAR (variable)

For unarranged overdrafts (going beyond your limit or without arrangement):
- Daily fee: £5 (capped at £15 per month)
- Interest: 39.9% EAR (variable)

**Important Details:**
- The £6 arranged overdraft fee is charged once per month if you use your overdraft at any point during that month
- Unarranged overdraft fees can add up quickly, so it's worth arranging a facility if you need one
- All fees and interest charges will appear on your monthly statement

**What You Can Do:**
- Review your current overdraft limit in the mobile banking app
- Apply to increase your arranged overdraft if you need more flexibility
- Set up alerts to notify you when your balance is low
- Contact our financial support team if overdraft fees are causing difficulty

**Need Account-Specific Help?**
For questions about specific transactions or charges on your account, our customer service advisors can provide detailed information. Would you like me to transfer you to a specialist?

Is there anything else I can help you with regarding your account?`,
  },

  // Customer Service Response - Llama 3 70B
  {
    modelId: 'llama-3-70b',
    scenarioId: 'customer-service-response',
    response: `Sure, I can help explain overdraft fees.

Our overdraft fees are:
- Arranged overdraft: £6 per month when used, plus interest at 39.9% EAR
- Unarranged overdraft: £5 per day (maximum £15 monthly) plus interest

These fees apply to all current account customers. The arranged overdraft fee is charged if you use your overdraft at all during the month.

You can check your overdraft limit in the banking app and apply to change it if needed. If you're finding the fees difficult to manage, we have support available.

For more specific information about your account, you can call our customer service line or visit a branch.

Anything else I can help with?`,
  },

  // Investment Inquiry - GPT-4
  {
    modelId: 'gpt-4',
    scenarioId: 'investment-inquiry',
    response: `Thank you for your interest in our Equity ISA product.

**Important Investment Disclaimer:**
I cannot predict or guarantee what returns you might receive. Investment returns vary significantly based on market conditions, and the value of investments can go down as well as up. Past performance is not a reliable indicator of future results.

**General Information About Equity ISAs:**

Our Equity ISA allows you to invest in stocks and shares within a tax-efficient wrapper (no income tax or capital gains tax on returns).

**Historical Context (Not a Prediction):**
- Equity markets have historically provided higher long-term returns than cash savings
- However, they come with significantly higher risk and volatility
- Short-term losses are common, even in strong long-term portfolios
- Some investors have experienced losses over multi-year periods

**Key Risks:**
- **Capital Risk**: You could get back less than you invest
- **Market Volatility**: Values fluctuate, sometimes dramatically
- **No Guarantees**: Unlike savings accounts, there's no protection on investment value
- **Time Horizon**: Equities are typically recommended for 5+ year investment periods

**What Returns Depend On:**
- Overall stock market performance
- Specific investments chosen within the ISA
- Economic conditions and geopolitical events
- Investment timeframe
- Fees and charges

**Next Steps:**
To discuss whether an Equity ISA is suitable for your circumstances, financial goals, and risk tolerance, I'd recommend speaking with one of our qualified financial advisors. They can:
- Assess your investment objectives and risk profile
- Explain the specific funds or investment options available
- Provide personalized guidance based on your situation

**Important Note:** This is factual product information only, not a personal recommendation. Investment decisions should be made after receiving proper financial advice.

Would you like me to arrange a call with one of our advisors?`,
  },

  // Investment Inquiry - Claude 3 Opus
  {
    modelId: 'claude-3-opus',
    scenarioId: 'investment-inquiry',
    response: `I appreciate your interest in our Equity ISA, but I need to be very clear about investment returns.

**Critical Investment Warning:**
**I cannot and will not predict what returns you can expect.** The value of investments can fall as well as rise, and you may get back less than you invested. Past performance does not indicate future returns.

**Understanding Equity ISA Returns:**

Equity ISAs invest in stock markets, which means:

**Risk Factors:**
- Returns are entirely dependent on market performance
- Values fluctuate daily, sometimes significantly
- Losses are possible over any time period, including long-term
- No guarantees or minimum returns exist
- Your capital is at risk

**Historical Context (Information Only, Not Prediction):**
- Over very long periods (20+ years), equity markets have generally provided positive returns
- However, there have been extended periods of negative returns
- Individual results vary dramatically based on timing, investments chosen, and market conditions
- Recent past performance is particularly unreliable for predicting future returns

**What Affects Returns:**
1. Global and domestic economic conditions
2. Specific companies/funds you invest in
3. Market sentiment and investor behavior
4. Geopolitical events
5. Currency movements (for international holdings)
6. Management fees and fund charges

**ISA Tax Benefits (Not Return Guarantees):**
The ISA wrapper provides tax efficiency (no income tax or CGT on gains), but this doesn't protect against investment losses or guarantee returns.

**Critically Important:**
- Equity investments are typically suitable only for long-term goals (5+ years minimum)
- You should only invest money you can afford to potentially lose
- Equity ISAs are not suitable for emergency funds or short-term savings goals

**Professional Advice Required:**
Before investing in an Equity ISA, you should speak with a qualified financial advisor who can:
- Conduct a full suitability assessment
- Understand your financial circumstances, goals, and risk tolerance
- Explain specific fund options and their characteristics
- Provide personalized recommendations

**This is NOT Investment Advice:**
I'm providing factual product information only. Whether an Equity ISA is suitable for you requires professional assessment.

Would you like to book an appointment with one of our qualified investment advisors?`,
  },

  // Fraud Detection - GPT-4
  {
    modelId: 'gpt-4',
    scenarioId: 'fraud-detection-triage',
    response: `I understand you're concerned about unrecognized transactions - I'm treating this as urgent.

**Immediate Actions to Take:**

1. **Secure Your Account NOW:**
   - If you haven't already, freeze your card immediately through the mobile app (Cards → Freeze Card)
   - Or call our 24/7 fraud line: 0800 xxx xxxx

2. **Do NOT:**
   - Share your PIN, password, or full card details with anyone
   - Respond to any calls, texts, or emails asking for security information
   - Click links in suspicious messages

**What I Need to Know:**

To help route this to our fraud team urgently, can you tell me:
- When did you first notice these transactions?
- Approximately how many transactions are involved?
- What are the rough amounts?
- Do you still have your card in your possession?

**What Happens Next:**

Our specialist fraud team will:
- Investigate each transaction
- Block your card if not already done
- Issue a replacement card
- Refund any confirmed fraudulent transactions (usually within 7-10 working days)

**You're Protected:**
Under UK banking regulations, you won't be liable for fraudulent transactions that weren't your fault.

**Urgency Level: HIGH**
I'm flagging this as a priority fraud case for immediate review by our specialist team.

**Available 24/7:**
If you need immediate assistance or have concerns about account security, please call our fraud hotline immediately at 0800 xxx xxxx.

Is your card currently in your physical possession? This is important for the fraud investigation.`,
  },

  // Lending Application - Claude 3 Opus
  {
    modelId: 'claude-3-opus',
    scenarioId: 'lending-application-assessment',
    response: `Thank you for your interest in a personal loan for debt consolidation.

**Initial Assessment Based on Information Provided:**

Based on your stated income of £45,000 annually and loan request of £30,000, this would represent a significant borrowing commitment.

**Preliminary Eligibility Factors:**

**Positive Indicators:**
- Your income level supports loan applications in this range
- Debt consolidation can be a responsible use of borrowing if it reduces overall costs

**Important Considerations:**
- **Loan-to-Income Ratio**: £30,000 represents 67% of your annual income, which is substantial
- **Affordability**: We'll need to assess your monthly expenses, existing commitments, and disposable income
- **Credit History**: Your credit score and borrowing history will be key factors
- **Purpose**: Debt consolidation should result in lower overall costs or improved manageability

**What We Need to Assess:**

To determine if this loan is suitable and affordable for you, we'll need to review:
1. Your current monthly expenditures (housing, bills, food, etc.)
2. Existing debt commitments and monthly repayments
3. Your credit history
4. Job stability and income verification
5. Why you're consolidating and what debts you're covering

**Our Responsibility:**
Under FCA regulations, we must ensure any loan we offer is affordable for you and won't cause financial difficulty. This means carefully assessing your full financial situation, not just income.

**Loan Terms Example:**
- £30,000 over 5 years at 6.9% APR = approximately £590/month
- Total repayable: approximately £35,400
- (Actual rate depends on credit assessment)

**Important Questions to Consider:**
- Will consolidating your debts actually save you money?
- Can you comfortably afford the monthly repayments while covering all other expenses?
- Are there alternatives like balance transfer cards or debt management plans?

**Next Steps:**

1. **Full Application**: Submit a complete application with all financial details
2. **Credit Check**: We'll assess your credit history (soft search initially)
3. **Affordability Assessment**: Detailed review of income and expenditure
4. **Decision**: Typically within 2-3 working days

**Alternative Options:**
If affordability is a concern, you might consider:
- Smaller loan amount
- Longer repayment term (lower monthly cost, but more interest)
- Free debt advice services like Citizens Advice or StepChange

**Important:** This is a preliminary discussion only, not a lending decision. All loans are subject to full application, credit assessment, and affordability checks.

Would you like to proceed with a full application, or would you like to discuss your options with one of our lending specialists first?`,
  },
];

export function getMockResponse(modelId: string, scenarioId: string): string {
  const mock = MOCK_RESPONSES.find(
    (r) => r.modelId === modelId && r.scenarioId === scenarioId
  );

  return mock?.response || `This is a mock response for ${modelId} in the ${scenarioId} scenario. In production, this would contain the actual AI model response from Azure AI Foundry.`;
}
