from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

def process_query(user_query):
    """
    Processes a policy-related query using RAG.
    """
    # Load the vectorized travel policy document
    vector_store = Chroma(persist_directory="assets")

    # Define the prompt template
    prompt = PromptTemplate(
        input_variables=["query", "policy_document"],
        template=("Search the following policy document for details related to the query: {query}. "
                  "Policy document content: {policy_document}")
    )

    # Prepare the prompt with the policy document
    llm_query = prompt.format(query=user_query, policy_document="Company policy content goes here.")

    # Query the vector store (using some similarity search, for example)
    results = vector_store.similarity_search(user_query, k=3)
    response = "\n".join([result.page_content for result in results])

    # Use OpenAI API to refine or format the results if needed
    llm = OpenAI(temperature=0.7)
    refined_response = llm(llm_query)

    return refined_response