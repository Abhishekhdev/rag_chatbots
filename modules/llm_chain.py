import google.generativeai as genai  # pip install google-generativeai
from modules.embeddings_store import create_or_load_faiss
from modules.config import GEMINI_API_KEY
from langchain_core.prompts import PromptTemplate

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
llm = genai.GenerativeModel("gemini-pro-latest")  # <-- Updated model name

# Prompt template for Gemini
template = """
You are a helpful assistant. Use the following context to answer the question.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}
Answer:
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

def ask_question(question: str) -> str:
    """
    Retrieve relevant documents from FAISS and ask the Gemini LLM
    """
    db = create_or_load_faiss()
    if not db:
        return "No documents found. Please upload and ingest files first."

    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    docs = retriever.invoke(question)
    context = "\n".join([doc.page_content for doc in docs])

    full_prompt = template.format(context=context, question=question)
    response = llm.generate_content(full_prompt)
    return getattr(response, "text", str(response))
