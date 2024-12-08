# Define categories for context understanding
general_keywords = [
    "must-visit tourist spots", 
    "cost to fly", 
    "best time of year", 
    "budget hotels", 
    "popular activities", 
    "book a train ticket", 
    "public transport options", 
    "suggest an itinerary", 
    "weather like", 
    "travel insurance", 
    "visa processing time",  # Add visa-related general question
]

specific_keywords = [
    "visa", 
    "transit visa", 
    "passport holder", 
    "entry requirements", 
    "visa-on-arrival", 
    "documents required", 
    "yellow fever vaccination", 
    "visa processing time"
]

# Function to classify questions based on context
def classify_question(question):
    # Normalize the question
    question_lower = question.lower()

    # Check for specific keywords first
    if any(keyword in question_lower for keyword in specific_keywords):
        # Check if "visa" is mentioned and the query asks for general information
        if "visa" in question_lower:
            # Specific keywords that could be generic visa-related queries
            if "processing time" in question_lower or "timeline" in question_lower or "requirements" in question_lower:
                return "General"  # Visa processing time or rules can be a general query
            else:
                return "Specific"  # Other visa-related specific questions
        else:
            return "Specific"  # Non-visa specific queries
    # Check for general keywords (e.g., tourism, activities)
    elif any(keyword in question_lower for keyword in general_keywords):
        return "General"
    
    # Default to Unknown if the question doesn't match known patterns
    return "Unknown"

# Function to handle the classification and routing based on question
def handle_question(question):
    classification = classify_question(question)
    if classification == "Specific":
        print(f"Classified as: Specific")
        print(f"Suggested Action: Ask for missing details like nationality, travel dates, or purpose.")
        group = "Agent B (Specific Scenarios)"
    elif classification == "General":
        print(f"Classified as: General")
        print(f"Suggested Action: Proceed with general information lookup.")
        group = "Agent A (General Enquiries)"
    else:
        print(f"Classified as: Unknown")
        print(f"Suggested Action: Request clarification from the user.")
        group = "Manual Review"
    
    return group

# Example questions to test the classification
sample_questions = [
    "What are some must-visit tourist spots in London?",
    "How much does it cost to fly from India to New York?",
    "What is the best time of year to visit Japan?",
    "Can you recommend budget hotels in Paris?",
    "What are the popular activities for tourists in Thailand?",
    "How do I book a train ticket in Europe?",
    "What are the public transport options in Singapore?",
    "Can you suggest an itinerary for 7 days in Bali?",
    "What is the weather like in Australia during December?",
    "Do I need travel insurance for visiting Dubai?",
    "What visa do I need to transit through Canada as an Indian passport holder?",
    "How long does it take to process a Schengen visa for Indian citizens?",
    "Do US green card holders need a visa to visit the UK?",
    "Can a South African citizen get a visa-on-arrival in Thailand?",
    "What is the visa-free period for Singapore passport holders visiting Germany?",
    "Do I need a transit visa for a layover in Doha on my way to France?",
    "What documents are required for a business visa to Japan for a Nigerian passport holder?",
    "I want to travel to France; do I need a visa?",
    "What is the UK VISA processing timeline?",
    "Do Indian citizens need a transit visa for connecting flights in the UK?",
    "Can I travel to Canada with an expired US visa?",
    "Are there exemptions for diplomatic passport holders traveling to the EU?"
    "I need to travel to france on business for two weeks can you help in planning my trip."
    "I am planning for vacation in south asia can you suggest nice family tourist destination which is economical"
    "do we need ecnr stamp for travel to south asia?"
]

# Main program
def main():
    while True:
        print("\n--- Travel Query Classification ---")
        print("1. Enter a new travel question")
        print("2. Test with sample questions")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            user_question = input("\nEnter your travel-related question: ")
            print(f"\nQuestion: {user_question}")
            group = handle_question(user_question)
            print(f"Routed to: {group}\n")
        elif choice == "2":
            print("\nTesting with sample questions...")
            for question in sample_questions:
                print(f"\nQuestion: {question}")
                group = handle_question(question)
                print(f"Routed to: {group}\n")
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose again.")

# Run the program
if __name__ == "__main__":
    main()
