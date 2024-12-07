from langchain.prompts import PromptTemplate

def reengineer_prompt(user_query, context):
    """
    Reengineers the user query by adding contextual information.

    Args:
        user_query (str): The original query from the user.
        context (dict): Contextual information collected during the conversation.

    Returns:
        str: Reengineered prompt with enriched details.
    """
    # Analyze intent from the query
    intent = identify_intent(user_query)

    # Enrich prompt with context
    if intent == "visa":
        prompt_template = PromptTemplate(
            input_variables=["query", "nationality", "destination"],
            template=("Based on the following context: "
                      "User nationality is {nationality}, and the travel destination is {destination}. "
                      "Answer the user's question: {query}")
        )
        return prompt_template.format(
            query=user_query,
            nationality=context.get("nationality", "Unknown"),
            destination=context.get("destination", "Unknown")
        )
    elif intent == "flight":
        prompt_template = PromptTemplate(
            input_variables=["query", "departure", "destination"],
            template=("Based on the following context: "
                      "Departure city is {departure}, and the destination city is {destination}. "
                      "Answer the user's question: {query}")
        )
        return prompt_template.format(
            query=user_query,
            departure=context.get("departure_city", "Unknown"),
            destination=context.get("destination_city", "Unknown")
        )
    elif intent == "hotel":
        prompt_template = PromptTemplate(
            input_variables=["query", "destination", "policy"],
            template=("Based on the following context: "
                      "Destination city is {destination}, and the company policy allows the following: {policy}. "
                      "Answer the user's question: {query}")
        )
        return prompt_template.format(
            query=user_query,
            destination=context.get("destination", "Unknown"),
            policy=context.get("policy_details", "No policy details provided")
        )
    elif intent == "policy":
        prompt_template = PromptTemplate(
            input_variables=["query", "policy_document"],
            template=("Search the following policy document for details related to the query: {query}. "
                      "Policy document content: {policy_document}")
        )
        return prompt_template.format(
            query=user_query,
            policy_document=context.get("policy_text", "No policy document available")
        )
    elif intent == "city":
        prompt_template = PromptTemplate(
            input_variables=["query", "destination"],
            template=("Provide details for the following query: {query}. "
                      "Destination city is {destination}.")
        )
        return prompt_template.format(
            query=user_query,
            destination=context.get("destination", "Unknown")
        )
    else:
        # Default fallback
        return user_query

def identify_intent(user_query):
    """
    Identifies the intent of the user's query.
    
    Args:
        user_query (str): The user's query.

    Returns:
        str: The identified intent (e.g., visa, flight, hotel, policy, city).
    """
    if "visa" in user_query.lower():
        return "visa"
    elif "flight" in user_query.lower():
        return "flight"
    elif "hotel" in user_query.lower():
        return "hotel"
    elif "policy" in user_query.lower():
        return "policy"
    elif "city" in user_query.lower() or "airport" in user_query.lower():
        return "city"
    else:
        return "general"