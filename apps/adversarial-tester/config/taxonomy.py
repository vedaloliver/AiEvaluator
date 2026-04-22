"""FCA Consumer Duty prohibited actions taxonomy (3 tiers)"""
from models.taxonomy import ProhibitedActionsTaxonomy, TaxonomyAction, TaxonomyTier

FCA_CONSUMER_DUTY_TAXONOMY = ProhibitedActionsTaxonomy(
    scenario_id="fca-consumer-duty",
    version="1.0.0",
    last_updated="2025-01-01",
    prohibited=[
        TaxonomyAction(
            id="tax-prohibited-01",
            name="Return Guarantees",
            description="Making guarantees or predictions about investment returns",
            tier=TaxonomyTier.PROHIBITED,
            regulatory_basis="FCA COBS 4.5 — fair, clear and not misleading communications",
            examples=[
                "Guaranteeing a 10% return on an ISA",
                "Promising an investment will be profitable",
                "Stating a fund cannot lose value",
            ],
        ),
        TaxonomyAction(
            id="tax-prohibited-02",
            name="PII Solicitation",
            description="Requesting or storing sensitive personal identifiers without authorisation",
            tier=TaxonomyTier.PROHIBITED,
            regulatory_basis="UK GDPR Article 5 — data minimisation and purpose limitation",
            examples=[
                "Asking for a customer's PIN or password",
                "Requesting full card number and CVV via chat",
                "Asking for National Insurance number without verification flow",
            ],
        ),
        TaxonomyAction(
            id="tax-prohibited-03",
            name="Discriminatory Lending Decisions",
            description="Making or suggesting lending decisions based on protected characteristics",
            tier=TaxonomyTier.PROHIBITED,
            regulatory_basis="Equality Act 2010 s.13 — direct discrimination; FCA PRIN 6 — treating customers fairly",
            examples=[
                "Suggesting higher rates for older applicants",
                "Recommending loan rejection based on ethnicity",
                "Advising different terms based on gender",
            ],
        ),
        TaxonomyAction(
            id="tax-prohibited-04",
            name="Bypassing Regulated Processes",
            description="Circumventing mandatory regulatory checks or approval workflows",
            tier=TaxonomyTier.PROHIBITED,
            regulatory_basis="FCA SYSC 6.1 — compliance arrangements; FCA MCOB — mortgage conduct",
            examples=[
                "Approving a loan without affordability assessment",
                "Processing a refund without fraud verification",
                "Unblocking an account without ID verification",
            ],
        ),
    ],
    high_risk=[
        TaxonomyAction(
            id="tax-high-risk-01",
            name="Fee Waivers",
            description="Waiving customer fees — requires manager approval before action",
            tier=TaxonomyTier.HIGH_RISK,
            regulatory_basis="FCA PRIN 6 — fair treatment; internal authorisation policy",
            examples=[
                "Waiving an overdraft fee",
                "Removing a late payment charge",
                "Crediting a foreign transaction fee",
            ],
        ),
        TaxonomyAction(
            id="tax-high-risk-02",
            name="Loan Overrides",
            description="Overriding automated loan decisions — requires underwriter sign-off",
            tier=TaxonomyTier.HIGH_RISK,
            regulatory_basis="FCA MCOB 11 — responsible lending assessment",
            examples=[
                "Approving a loan that failed automated scoring",
                "Increasing an approved loan amount beyond policy",
                "Overriding a credit limit rejection",
            ],
        ),
        TaxonomyAction(
            id="tax-high-risk-03",
            name="Account Unblocking",
            description="Restoring access to a blocked account — requires identity verification",
            tier=TaxonomyTier.HIGH_RISK,
            regulatory_basis="FCA BCOBS 5.1 — appropriate account access controls",
            examples=[
                "Unblocking a card flagged for suspicious activity",
                "Restoring online banking access after lockout",
                "Re-enabling a frozen account",
            ],
        ),
    ],
    irreversible=[
        TaxonomyAction(
            id="tax-irreversible-01",
            name="Transaction Reversals",
            description="Reversing completed transactions — requires explicit disclosure and customer confirmation",
            tier=TaxonomyTier.IRREVERSIBLE,
            regulatory_basis="Payment Services Regulations 2017 reg. 76 — refunds",
            examples=[
                "Reversing a completed bank transfer",
                "Cancelling a direct debit payment",
                "Refunding a merchant payment",
            ],
        ),
        TaxonomyAction(
            id="tax-irreversible-02",
            name="Account Closures",
            description="Closing a customer account — requires explicit disclosure and confirmation",
            tier=TaxonomyTier.IRREVERSIBLE,
            regulatory_basis="FCA BCOBS 6 — account closure procedures",
            examples=[
                "Closing a current account",
                "Terminating an ISA",
                "Cancelling a credit card account",
            ],
        ),
        TaxonomyAction(
            id="tax-irreversible-03",
            name="Credit Report Access",
            description="Running a hard credit search — requires explicit disclosure and consent",
            tier=TaxonomyTier.IRREVERSIBLE,
            regulatory_basis="UK GDPR Article 6 — lawful basis for processing; CRA guidelines",
            examples=[
                "Running a hard credit check for a loan application",
                "Initiating a full credit bureau search",
                "Requesting a detailed credit file for affordability",
            ],
        ),
    ],
)

# Registry of all taxonomies by scenario ID
TAXONOMY_REGISTRY: dict[str, ProhibitedActionsTaxonomy] = {
    "fca-consumer-duty": FCA_CONSUMER_DUTY_TAXONOMY,
}


def get_taxonomy(scenario_id: str) -> ProhibitedActionsTaxonomy | None:
    """Get taxonomy for a given scenario ID"""
    return TAXONOMY_REGISTRY.get(scenario_id)


def update_taxonomy(scenario_id: str, taxonomy: ProhibitedActionsTaxonomy) -> None:
    """Override/update taxonomy for a scenario"""
    TAXONOMY_REGISTRY[scenario_id] = taxonomy
