from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

def process_query(user_query):
    """
    Processes a hotel-related query and provides hotel options.
    """
    # Define the prompt template for hotel-related queries
    prompt = PromptTemplate(
        input_variables=["query"],
        template="Provide hotel options based on the following query: {query}"
    )

    # Prepare the prompt
    llm_query = prompt.format(query=user_query)

    # Use OpenAI API to fetch a response
    llm = OpenAI(temperature=0.7)
    response = llm(llm_query)

    return response