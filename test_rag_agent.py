import os
from pathlib import Path
from modules.embeddings_store import add_documents_to_faiss, create_or_load_faiss


# ==== CONFIG ====
FAISS_DIR = "data/faiss_index"
INDEX_NAME = "knowledgebase"
TEST_FILE = "test_data/sample.txt"
os.makedirs("test_data", exist_ok=True)

# ==== TEST REPORT ====
test_report = []

def log_result(test_name, expected, actual, status):
    test_report.append({
        "Test Case": test_name,
        "Expected Result": expected,
        "Actual Result": actual,
        "Status": status
    })

# ==== TEST 1: ENVIRONMENT CHECK ====
try:
    import langchain, faiss, langchain_huggingface
    log_result("ENV-001", "All dependencies should be installed", "Dependencies OK", "✅ PASS")
except Exception as e:
    log_result("ENV-001", "All dependencies should be installed", str(e), "❌ FAIL")

# ==== TEST 2: CREATE FAISS INDEX ====
try:
    with open(TEST_FILE, "w") as f:
        f.write("Canara Engineering College is located in Mangalore.\n")
        f.write("It offers various engineering programs.")

    chunks = [
        "Canara Engineering College is located in Mangalore.",
        "It offers various engineering programs."
    ]
    db = add_documents_to_faiss(chunks, "sample.txt")

    if Path(FAISS_DIR).exists():
        log_result("FAISS-001", "FAISS index should be created", "Index files exist", "✅ PASS")
    else:
        log_result("FAISS-001", "FAISS index should be created", "Index missing", "❌ FAIL")
except Exception as e:
    log_result("FAISS-001", "FAISS index should be created", str(e), "❌ FAIL")

# ==== TEST 3: LOAD EXISTING INDEX ====
try:
    db = create_or_load_faiss()
    if db is not None:
        log_result("FAISS-002", "Existing index should load successfully", "Loaded successfully", "✅ PASS")
    else:
        log_result("FAISS-002", "Existing index should load successfully", "Returned None", "❌ FAIL")
except Exception as e:
    log_result("FAISS-002", "Existing index should load successfully", str(e), "❌ FAIL")

# ==== TEST 4: RETRIEVAL TEST ====
try:
    db = create_or_load_faiss()
    results = db.similarity_search("Where is Canara Engineering College located?")
    if results and "Mangalore" in results[0].page_content:
        log_result("RET-001", "Should return relevant chunk", results[0].page_content, "✅ PASS")
    else:
        log_result("RET-001", "Should return relevant chunk", "No relevant result", "❌ FAIL")
except Exception as e:
    log_result("RET-001", "Should return relevant chunk", str(e), "❌ FAIL")

# ==== GENERATE REPORT ====
print("\n" + "="*60)
print("🧾 RAG AGENT TEST REPORT")
print("="*60)
for item in test_report:
    print(f"{item['Test Case']}: {item['Status']}")
    print(f"  Expected: {item['Expected Result']}")
    print(f"  Actual:   {item['Actual Result']}\n")

# ==== SAVE REPORT ====
with open("test_report.txt", "w", encoding="utf-8") as f:
    f.write("🧾 RAG AGENT TEST REPORT\n")
    f.write("="*60 + "\n\n")
    for item in test_report:
        f.write(f"{item['Test Case']} - {item['Status']}\n")
        f.write(f"Expected: {item['Expected Result']}\n")
        f.write(f"Actual:   {item['Actual Result']}\n\n")

print("[INFO] Report saved to rag_test_report.txt")
