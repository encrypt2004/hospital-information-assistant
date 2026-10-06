import re


POLICY_KEYWORDS = [
    "policy",
    "policies",
    "operating hours",
    "hospital hours",
    "appointment policy",
    "appointment rules",
    "room policy",
    "room change",
    "pharmacy policy",
    "prescription policy",
    "laboratory policy",
    "billing policy",
    "insurance policy",
    "privacy",
    "privacy policy",
    "assistant",
    "what can you",
    "what can't you",
    "emergency policy",
]


STRUCTURED_KEYWORDS = [
    "doctor",
    "dr.",
    "specialist",
    "specialization",
    "department",
    "room",
    "schedule",
    "timing",
    "time",
    "phone",
    "contact",
    "number",
    "appointment",
    "hospital",
    "floor",
    "cardiology",
    "neurology",
    "orthopedic",
    "orthopaedic",
    "pediatrics",
    "paediatrics",
    "dermatology",
    "gastroenterology",
    "gynecology",
    "gynaecology",
]


def route_question(query):
    """
    Decide which source should handle the question.

    Returns:
        structured
        policy
    """

    query = query.lower().strip()

    policy_score = 0
    structured_score = 0

    for keyword in POLICY_KEYWORDS:

        if keyword in query:
            policy_score += 2

    for keyword in STRUCTURED_KEYWORDS:

        if keyword in query:
            structured_score += 1

    # Strong policy questions should go to PDF.
    if policy_score > structured_score:
        return "policy"

    return "structured"