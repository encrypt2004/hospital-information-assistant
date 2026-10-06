from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm():
    """
    Create Gemini chat model.
    """

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    )