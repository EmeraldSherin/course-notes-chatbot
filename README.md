AI-powered chatbot for answering questions from course notes using RAG

🧠 Tech Stack
Component	Technology
RAG Framework	LlamaIndex
Vector Store	FAISS
LLM	Groq — Llama 3.3
Embeddings	HuggingFace (BGE-small)
Document Parsing	txt, pdf, md, docx
🚀 Features

Multi-format document ingestion (TXT, PDF, MD, DOCX)

Semantic search with FAISS

Context-aware answers using Llama 3.3

Chat terminal interface

Free API usage via Groq

📂 Project Structure
Assignment1_YourName/
│── code/
│   ├── chatbot.py
│   ├── pdf_converter.py
│   └── test_queries.py
│── course_notes/
│── screenshots/
│── requirements.txt
│── .env.example
│── README.md

⚙️ Setup Instructions
✅ Create Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate


Mac/Linux

python3 -m venv venv
source venv/bin/activate

✅ Install Requirements
pip install -r requirements.txt

✅ Add Groq API Key
cp .env.example .env   # or copy on Windows


Edit .env:

GROQ_API_KEY=your_key_here

✅ Add Course Notes

Place files inside course_notes/

Supported formats:

.txt | .pdf | .md | .docx

▶️ Run the Chatbot
python code/chatbot.py

🎤 Example Chat
You: What is Big Data?

Bot: Big Data refers to extremely large datasets...

🧪 Testing
python code/test_queries.py

🔧 Troubleshooting
Issue	Fix
No module named llama_index	pip install --upgrade llama-index
GROQ_API_KEY missing	Create .env file
PDF content not loading	Run pdf_converter.py first
⚡ Performance Tips
Faster responses
model="llama-3.1-8b-instant"

Higher accuracy
similarity_top_k=7

📌 Limitations

No OCR for scanned PDFs

Requires internet for API

Limited to uploaded notes
