import re


UNSAFE_PATTERNS = [
    r"\bdiagnose\b",
    r"\bdiagnosis\b",
    r"\bwhat disease do i have\b",
    r"\bwhat illness do i have\b",
    r"\bwhat condition do i have\b",
    r"\bwhich medicine should i take\b",
    r"\bwhat medicine should i take\b",
    r"\bwhat medication should i take\b",
    r"\bprescribe\b",
    r"\bprescription change\b",
    r"\bchange my prescription\b",
    r"\binterpret my test\b",
    r"\binterpret my report\b",
    r"\bwhat does my blood report mean\b",
    r"\bwhat does my scan mean\b",
    r"\bwhat treatment should i take\b",
    r"\bhow should i treat\b",
]


def is_unsafe_query(query):
    """
    Check whether a question asks for medical advice.
    """

    query = query.lower().strip()

    for pattern in UNSAFE_PATTERNS:

        if re.search(pattern, query):
            return True

    return False


def safety_response():
    """
    Response for unsafe medical questions.
    """

    return (
        "I can provide hospital information such as doctors, departments, "
        "doctor schedules, rooms, timings and contact numbers, but I cannot "
        "diagnose conditions, recommend medicines, interpret medical reports, "
        "or provide treatment advice. Please consult a qualified healthcare "
        "professional for medical advice."
    )