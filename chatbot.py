import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# LlamaIndex imports
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
    Document
)
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

import faiss

# Load environment variables
load_dotenv()


class CourseNoteChatbot:
    
    def __init__(self, notes_directory: str, groq_api_key: str = None):
        self.notes_directory = notes_directory
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        
        if not self.groq_api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable or pass it directly.")
        
        self.index = None
        self.query_engine = None
        
        # Configure LlamaIndex settings
        self._configure_settings()
        
    def _configure_settings(self):
        """Configure LlamaIndex global settings."""
        # Set up the LLM (Llama 3.3 via Groq) - Updated model
        Settings.llm = Groq(
            model="llama-3.3-70b-versatile",
            api_key=self.groq_api_key,
            temperature=0.3  # Slightly higher for more detailed responses
        )
        
        # Set up embeddings (using free HuggingFace embeddings)
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        
        # Set chunk size for better context
        Settings.chunk_size = 1024  # Increased for more context
        Settings.chunk_overlap = 128  # More overlap for continuity
        
    def load_notes(self, file_extensions: List[str] = None):
        
        if file_extensions is None:
            file_extensions = ['.txt', '.pdf', '.md', '.docx']
        
        print(f"Loading notes from: {self.notes_directory}")
        
        # Check if directory exists
        if not os.path.exists(self.notes_directory):
            raise FileNotFoundError(f"Directory not found: {self.notes_directory}")
        
        # Load documents
        try:
            reader = SimpleDirectoryReader(
                input_dir=self.notes_directory,
                required_exts=file_extensions,
                recursive=True
            )
            documents = reader.load_data()
            print(f"Loaded {len(documents)} documents")
            
            # Verify documents have content
            for i, doc in enumerate(documents):
                text_preview = doc.text[:200] if len(doc.text) > 200 else doc.text
                print(f"\nDocument {i+1} preview: {text_preview}...")
                if len(doc.text.strip()) < 50:
                    print(f"⚠️ Warning: Document {i+1} has very little content!")
            
            return documents
        except Exception as e:
            print(f"Error loading documents: {e}")
            return []
    
    def build_index(self, documents: List[Document] = None):
        """
        Build FAISS index from documents.
        
        Args:
            documents: List of Document objects. If None, loads from notes_directory
        """
        if documents is None:
            documents = self.load_notes()
        
        if not documents:
            raise ValueError("No documents to index. Please check your notes directory.")
        
        print("Building FAISS index...")
        
        # Create FAISS index
        # Dimension is 384 for BAAI/bge-small-en-v1.5 embeddings
        dimension = 384
        faiss_index = faiss.IndexFlatL2(dimension)
        
        # Create vector store
        vector_store = FaissVectorStore(faiss_index=faiss_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # Build index
        self.index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True
        )
        
        print("Index built successfully!")
        
    def create_query_engine(self, similarity_top_k: int = 5):
        """
        Create a query engine for answering questions.
        
        Args:
            similarity_top_k: Number of similar chunks to retrieve
        """
        if self.index is None:
            raise ValueError("Index not built. Call build_index() first.")
        
        # Use tree_summarize for better responses
        self.query_engine = self.index.as_query_engine(
            similarity_top_k=similarity_top_k,
            response_mode="tree_summarize",
            verbose=False
        )
        
    def ask(self, question: str) -> str:
        """
        Ask the chatbot a question.
        
        Args:
            question: The question to ask
            
        Returns:
            The chatbot's response
        """
        if self.query_engine is None:
            self.create_query_engine()
        
        print(f"\nQuestion: {question}")
        response = self.query_engine.query(question)
        return str(response)
    
    def chat(self):
        """Start an interactive chat session."""
        print("\n" + "="*60)
        print("Course Notes Chatbot")
        print("="*60)
        print("Ask questions about your course notes. Type 'quit' to exit.")
        print("="*60 + "\n")
        
        while True:
            try:
                question = input("You: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not question:
                    continue
                
                response = self.ask(question)
                print(f"\nChatbot: {response}\n")
                print("-"*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main function to run the chatbot."""
    
    # Setup example notes (comment this out if you have your own notes)
    notes_dir = "course_notes"
    if not os.path.exists(notes_dir):
        print("Creating example course notes...")
        setup_example_notes(notes_dir)
        print()
    
    # Get API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Please set your GROQ_API_KEY environment variable.")
        print("Get a free API key from: https://console.groq.com/")
        print("\nYou can set it by creating a .env file with:")
        print("GROQ_API_KEY=your_api_key_here")
        return
    
    try:
        # Initialize chatbot
        chatbot = CourseNoteChatbot(
            notes_directory=notes_dir,
            groq_api_key=api_key
        )
        
        # Load and index notes
        documents = chatbot.load_notes()
        chatbot.build_index(documents)
        
        # Start chat
        chatbot.chat()
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. Installed all required packages")
        print("2. Set your GROQ_API_KEY")
        print("3. Created course notes in the specified directory")


if __name__ == "__main__":
    main()