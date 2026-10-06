import re
import pandas as pd


# ============================================================
# 1. TEXT NORMALIZATION
# ============================================================

def normalize(text):
    """
    Convert text into a clean, lowercase searchable format.
    """

    if text is None:
        return ""

    text = str(text).lower()

    # Common language variations
    replacements = {
        "speciality": "specialization",
        "specialty": "specialization",
        "specialisation": "specialization",
        "specialised": "specialized",
        "specialised": "specialized",
        "dr.": "doctor",
        "dr ": "doctor ",
        "timing": "time",
        "timings": "time",
        "hours": "time",
        "phone": "contact",
        "number": "contact",
        "numbers": "contact",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove punctuation
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text):
    """
    Convert text into useful searchable words.
    """

    text = normalize(text)

    stop_words = {
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
        "what",
        "which",
        "who",
        "where",
        "when",
        "how",
        "can",
        "could",
        "would",
        "please",
        "me",
        "my",
        "your",
        "their",
        "with",
        "and",
        "or",
        "of",
        "in",
        "on",
        "for",
        "to",
        "tell",
        "give",
        "show",
        "get",
        "find",
        "available",
        "there",
        "does",
        "do",
    }

    return [
        word
        for word in text.split()
        if len(word) > 2 and word not in stop_words
    ]


def row_to_text(row):
    """
    Convert a pandas row into readable text.
    """

    values = []

    for column, value in row.items():

        if pd.notna(value):

            values.append(
                f"{column}: {value}"
            )

    return ", ".join(values)


# ============================================================
# 2. INTENT DETECTION
# ============================================================

def detect_intent(query):
    """
    Determine what type of hospital information
    the user is asking for.

    This is intentionally lightweight.
    No LLM or LangGraph is used here.
    """

    query = normalize(query)

    intents = {
        "doctor": [
            "doctor",
            "doctors",
            "physician",
            "specialist",
        ],

        "specialization": [
            "specialization",
            "specialized",
            "field",
            "expertise",
            "specialist",
            "specialization field",
        ],

        "department": [
            "department",
            "departments",
            "division",
        ],

        "schedule": [
            "schedule",
            "time",
            "available",
            "availability",
            "working",
            "hours",
        ],

        "hospital_timing": [
            "hospital time",
            "hospital opening",
            "hospital open",
            "hospital working",
            "hospital operating",
        ],

        "contact": [
            "contact",
            "phone",
            "call",
            "number",
        ],

        "appointment": [
            "appointment",
            "booking",
            "book",
        ],

        "emergency": [
            "emergency",
            "urgent",
        ],

        "pharmacy": [
            "pharmacy",
        ],

        "laboratory": [
            "laboratory",
            "lab",
            "test",
        ],

        "billing": [
            "billing",
            "bill",
            "insurance",
            "payment",
        ],

        "hospital_info": [
            "hospital",
            "address",
            "location",
            "name",
        ],
    }

    detected = set()

    for intent, keywords in intents.items():

        for keyword in keywords:

            if keyword in query:
                detected.add(intent)
                break

    return detected


# ============================================================
# 3. RELEVANCE SCORING
# ============================================================

def calculate_score(query, text):
    """
    Calculate how relevant a row is to the question.

    Higher score = more relevant.
    """

    query_words = set(
        tokenize(query)
    )

    text_words = set(
        tokenize(text)
    )

    if not query_words or not text_words:
        return 0

    common_words = query_words.intersection(
        text_words
    )

    score = len(common_words)

    # Stronger score when exact phrases match
    normalized_query = normalize(query)
    normalized_text = normalize(text)

    for word in common_words:

        if word in normalized_text:
            score += 1

    # Important concepts get extra weight
    important_terms = {
        "doctor": 3,
        "specialization": 3,
        "department": 3,
        "schedule": 3,
        "time": 2,
        "contact": 2,
        "appointment": 3,
        "emergency": 3,
        "pharmacy": 3,
        "laboratory": 3,
        "billing": 3,
    }

    for term, weight in important_terms.items():

        if term in normalized_query:

            if term in normalized_text:
                score += weight

    return score


# ============================================================
# 4. GENERIC RANKING
# ============================================================

def rank_rows(df, query, columns):
    """
    Rank dataframe rows according to relevance.

    Returns:
        List of (score, row)
    """

    ranked = []

    for _, row in df.iterrows():

        searchable_text = " ".join(
            str(row[column])
            for column in columns
            if column in row.index
            and pd.notna(row[column])
        )

        score = calculate_score(
            query,
            searchable_text,
        )

        if score > 0:

            ranked.append(
                (score, row)
            )

    ranked.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return ranked


# ============================================================
# 5. HOSPITAL INFORMATION SEARCH
# ============================================================

def search_hospital_info(df, query):

    normalized_query = normalize(query)

    # --------------------------------------------------------
    # Hospital timing
    # --------------------------------------------------------

    timing_words = [
        "hospital time",
        "hospital opening",
        "hospital open",
        "hospital working",
        "hospital operating",
        "opening time",
        "opening time",
        "working time",
    ]

    if any(
        phrase in normalized_query
        for phrase in timing_words
    ):

        results = []

        for _, row in df.iterrows():

            field = normalize(
                row["Field"]
            )

            if any(
                word in field
                for word in [
                    "hour",
                    "time",
                    "timing",
                    "opening",
                    "operating",
                    "working",
                ]
            ):

                results.append(
                    row_to_text(row)
                )

        if results:
            return results

    # --------------------------------------------------------
    # Hospital name
    # --------------------------------------------------------

    if any(
        phrase in normalized_query
        for phrase in [
            "hospital name",
            "name hospital",
            "which hospital",
        ]
    ):

        results = []

        for _, row in df.iterrows():

            if "name" in normalize(
                row["Field"]
            ):

                results.append(
                    row_to_text(row)
                )

        if results:
            return results

    # --------------------------------------------------------
    # Hospital address
    # --------------------------------------------------------

    if any(
        phrase in normalized_query
        for phrase in [
            "hospital address",
            "hospital location",
            "where hospital",
            "where is hospital",
        ]
    ):

        results = []

        for _, row in df.iterrows():

            field = normalize(
                row["Field"]
            )

            if (
                "address" in field
                or "location" in field
            ):

                results.append(
                    row_to_text(row)
                )

        if results:
            return results

    # --------------------------------------------------------
    # General relevance search
    # --------------------------------------------------------

    ranked = rank_rows(
        df,
        query,
        [
            "Field",
            "Value",
        ],
    )

    return [
        row_to_text(row)
        for score, row in ranked[:5]
    ]


# ============================================================
# 6. DEPARTMENT SEARCH
# ============================================================

def search_departments(df, query):

    normalized_query = normalize(query)

    # --------------------------------------------------------
    # List all departments
    # --------------------------------------------------------

    list_request = any(
        phrase in normalized_query
        for phrase in [
            "list department",
            "all department",
            "show department",
            "what department",
            "which department",
            "department available",
        ]
    )

    if list_request:

        return [
            row_to_text(row)
            for _, row in df.iterrows()
        ]

    # --------------------------------------------------------
    # Search specific department
    # --------------------------------------------------------

    ranked = rank_rows(
        df,
        query,
        [
            "Department",
            "Description",
            "Floor",
            "Room_Range",
        ],
    )

    return [
        row_to_text(row)
        for score, row in ranked[:5]
    ]


# ============================================================
# 7. DOCTOR SEARCH
# ============================================================

def search_doctors(
    doctors_df,
    schedule_df,
    query,
):

    normalized_query = normalize(query)

    intents = detect_intent(
        query
    )

    # --------------------------------------------------------
    # Detect broad doctor requests
    # --------------------------------------------------------

    all_doctors_request = any(
        phrase in normalized_query
        for phrase in [
            "list doctor",
            "all doctor",
            "show doctor",
            "doctor list",
            "who doctor",
            "give doctor",
            "doctor available",
            "doctor in hospital",
        ]
    )

    specialization_request = (
        "specialization" in intents
        or "field" in normalized_query
        or "expertise" in normalized_query
    )

    department_request = (
        "department" in intents
    )

    schedule_request = (
        "schedule" in intents
    )

    # --------------------------------------------------------
    # Case 1:
    #
    # "Give doctors with their field of speciality"
    #
    # Return all doctors with specialization.
    # --------------------------------------------------------

    if (
        all_doctors_request
        and (
            specialization_request
            or department_request
        )
    ):

        return [
            row_to_text(row)
            for _, row in doctors_df.iterrows()
        ]

    # --------------------------------------------------------
    # Case 2:
    #
    # "List all doctors"
    # --------------------------------------------------------

    if all_doctors_request:

        return [
            row_to_text(row)
            for _, row in doctors_df.iterrows()
        ]

    # --------------------------------------------------------
    # Case 3:
    #
    # Search specific doctors
    # --------------------------------------------------------

    ranked = rank_rows(
        doctors_df,
        query,
        [
            "Doctor_Name",
            "Department",
            "Specialization",
            "Room_No",
            "Contact_No",
        ],
    )

    # --------------------------------------------------------
    # Keep only reasonably relevant doctors
    # --------------------------------------------------------

    selected = [
        row
        for score, row in ranked
        if score >= 2
    ]

    # --------------------------------------------------------
    # If no strong match was found,
    # return top relevant rows.
    # --------------------------------------------------------

    if not selected and ranked:

        selected = [
            row
            for score, row in ranked[:3]
        ]

    # --------------------------------------------------------
    # Add schedules when requested
    # --------------------------------------------------------

    results = []

    for doctor in selected:

        doctor_text = row_to_text(
            doctor
        )

        if schedule_request:

            doctor_id = doctor[
                "Doctor_ID"
            ]

            schedules = schedule_df[
                schedule_df[
                    "Doctor_ID"
                ].astype(str)
                == str(doctor_id)
            ]

            schedule_text = []

            for _, schedule in schedules.iterrows():

                schedule_text.append(
                    row_to_text(
                        schedule
                    )
                )

            if schedule_text:

                doctor_text += (
                    "\nSchedule:\n"
                    + "\n".join(
                        schedule_text
                    )
                )

        results.append(
            doctor_text
        )

    return results


# ============================================================
# 8. CONTACT SEARCH
# ============================================================

def search_contacts(df, query):

    normalized_query = normalize(
        query
    )

    service_keywords = {

        "appointment": [
            "appointment",
            "booking",
            "book",
        ],

        "emergency": [
            "emergency",
            "urgent",
        ],

        "pharmacy": [
            "pharmacy",
            "medicine",
        ],

        "laboratory": [
            "laboratory",
            "lab",
            "test",
            "report",
        ],

        "billing": [
            "billing",
            "bill",
            "payment",
            "insurance",
        ],
    }

    requested_services = []

    for service, keywords in service_keywords.items():

        if any(
            keyword in normalized_query
            for keyword in keywords
        ):

            requested_services.append(
                service
            )

    if requested_services:

        results = []

        for _, row in df.iterrows():

            service = normalize(
                row["Service"]
            )

            if service in requested_services:

                results.append(
                    row_to_text(row)
                )

        if results:
            return results

    # Generic relevance fallback
    ranked = rank_rows(
        df,
        query,
        [
            "Service",
            "Phone_No",
            "Purpose",
            "Availability",
        ],
    )

    return [
        row_to_text(row)
        for score, row in ranked[:5]
    ]


# ============================================================
# 9. MAIN STRUCTURED SEARCH
# ============================================================

def structured_search(data, query):

    normalized_query = normalize(
        query
    )

    intents = detect_intent(
        query
    )

    results = []

    # --------------------------------------------------------
    # Doctor-specific questions
    # --------------------------------------------------------

    if (
        "doctor" in intents
        or "specialization" in intents
        or "specialist" in normalized_query
    ):

        results.extend(
            search_doctors(
                data["doctors"],
                data["doctor_schedule"],
                query,
            )
        )

    # --------------------------------------------------------
    # Department questions
    # --------------------------------------------------------

    if "department" in intents:

        results.extend(
            search_departments(
                data["departments"],
                query,
            )
        )

    # --------------------------------------------------------
    # Contact questions
    # --------------------------------------------------------

    if (
        "contact" in intents
        or "appointment" in intents
        or "emergency" in intents
        or "pharmacy" in intents
        or "laboratory" in intents
        or "billing" in intents
    ):

        results.extend(
            search_contacts(
                data["contacts"],
                query,
            )
        )

    # --------------------------------------------------------
    # Hospital information
    # --------------------------------------------------------

    if (
        "hospital_info" in intents
        or "hospital_timing" in intents
    ):

        results.extend(
            search_hospital_info(
                data["hospital_info"],
                query,
            )
        )

    # --------------------------------------------------------
    # If nothing matched an intent,
    # try all structured sources.
    # --------------------------------------------------------

    if not results:

        results.extend(
            search_hospital_info(
                data["hospital_info"],
                query,
            )
        )

        results.extend(
            search_departments(
                data["departments"],
                query,
            )
        )

        results.extend(
            search_doctors(
                data["doctors"],
                data["doctor_schedule"],
                query,
            )
        )

        results.extend(
            search_contacts(
                data["contacts"],
                query,
            )
        )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    results = list(
        dict.fromkeys(results)
    )

    return results


# ============================================================
# 10. FORMAT CONTEXT FOR GEMINI
# ============================================================

def format_structured_context(results):

    if not results:

        return (
            "No relevant hospital information was found."
        )

    return "\n\n".join(
        f"- {result}"
        for result in results
    )