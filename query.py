# query.py

from modules.llm_chain import ask_question

def main():
    print("RAG Chatbot CLI")
    print("Type 'exit' to quit.\n")
    
    while True:
        question = input("Your question: ")
        if question.lower() in ["exit", "quit"]:
            break
        
        answer = ask_question(question)
        print(f"Answer: {answer}\n")

if __name__ == "__main__":
    main()
