class Memory:
    def __init__(self):
        self.conversation_history = []  # List to store the conversation history

    def process_input(self, user_input):
        """
        Processes a new user input, and optionally, re-engineers it based on previous interactions.
        """
        # For simplicity, we'll just return the user input as is for now
        return user_input

    def store_response(self, user_input, agent_response):
        """
        Stores the user input and agent response in memory.
        """
        self.conversation_history.append({
            "query": user_input,
            "response": agent_response
        })

    def get_conversation(self):
        """
        Returns the entire conversation history.
        """
        return self.conversation_history

# Function to initialize memory
def initialize_memory():
    """
    Initializes the memory object.
    """
    return Memory()