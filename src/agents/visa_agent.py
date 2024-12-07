from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

def process_query(user_query):
    """
    Processes a visa-related query and fetches visa requirements.
    """
    # Define the prompt template
    prompt = PromptTemplate(
        input_variables=["query"],
        template="Provide visa requirements for the following query: {query}"
    )

    # Prepare the prompt
    llm_query = prompt.format(query=user_query)

    # Use OpenAI API to fetch a response
    llm = OpenAI(temperature=0.7)
    response = llm(llm_query)

    return response