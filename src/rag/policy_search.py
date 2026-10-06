def search_policy(vectorstore, query, k=4):
    """
    Search hospital policy using FAISS.
    """

    documents = vectorstore.similarity_search(
        query,
        k=k
    )

    return documents


def format_policy_context(documents):
    """
    Convert retrieved policy documents into LLM context.
    """

    if not documents:
        return "No relevant hospital policy information was found."

    context_parts = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "Hospital Policy PDF"
        )

        page = document.metadata.get(
            "page",
            "unknown"
        )

        context_parts.append(
            f"Source: {source}, Page: {page}\n"
            f"{document.page_content}"
        )

    return "\n\n".join(context_parts)