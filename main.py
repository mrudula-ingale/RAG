from rag_app.rag_chain import ask_rag

def main():
    print("RAG Assistant")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("Ask a question: ")

        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        response = ask_rag(question)

        print("\nAnswer:")
        print(response["answer"])

        print("\nSources:")
        for i, source in enumerate(response["sources"], start=1):
            print(f"{i}. {source['source']} | page {source['page']}")

        print("-" * 80)


if __name__ == "__main__":
    main()