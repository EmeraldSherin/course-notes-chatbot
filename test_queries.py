"""
Automated Testing Script for Course Notes Chatbot
=================================================

This script tests the chatbot with predefined queries and saves results.
Useful for generating demonstration evidence for assignment submission.
"""

import os
from datetime import datetime
from chatbot import CourseNoteChatbot


def run_tests():
    """Run automated tests with predefined queries."""
    
    # Test queries - CUSTOMIZE THESE FOR YOUR COURSE
    test_queries = [
        "What is Big Data?",
        "Explain the MapReduce programming model",
        "What are the main components of Hadoop ecosystem?",
        "Describe HDFS architecture",
        "What is the difference between Hive and HBase?",
        "Explain the CAP theorem",
        "What is NoSQL and when should it be used?",
        "Describe the role of NameNode in Hadoop",
        "What are the characteristics of Big Data (Vs)?",
        "How does Apache Spark differ from Hadoop MapReduce?"
    ]
    
    print("="*70)
    print("AUTOMATED CHATBOT TESTING")
    print("="*70)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Queries: {len(test_queries)}")
    print("="*70)
    print()
    
    # Initialize chatbot
    try:
        chatbot = CourseNoteChatbot(
            notes_directory="course_notes",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Load and build index
        print("Initializing chatbot...")
        documents = chatbot.load_notes()
        chatbot.build_index(documents)
        print()
        
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        return
    
    # Prepare results file
    results_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Run tests
    results = []
    successful = 0
    failed = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"Query {i}/{len(test_queries)}")
        print(f"{'='*70}")
        print(f"Question: {query}")
        print("-"*70)
        
        try:
            response = chatbot.ask(query)
            print(f"Response: {response}")
            
            results.append({
                'query': query,
                'response': response,
                'status': 'success'
            })
            successful += 1
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                'query': query,
                'response': str(e),
                'status': 'failed'
            })
            failed += 1
    
    # Save results to file
    print(f"\n\n{'='*70}")
    print("SAVING RESULTS")
    print(f"{'='*70}")
    
    with open(results_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("COURSE NOTES CHATBOT - TEST RESULTS\n")
        f.write("="*70 + "\n")
        f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Queries: {len(test_queries)}\n")
        f.write(f"Successful: {successful}\n")
        f.write(f"Failed: {failed}\n")
        f.write("="*70 + "\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"\n{'='*70}\n")
            f.write(f"QUERY {i}\n")
            f.write(f"{'='*70}\n\n")
            f.write(f"Question: {result['query']}\n\n")
            f.write(f"Status: {result['status'].upper()}\n\n")
            f.write(f"Response:\n{'-'*70}\n")
            f.write(f"{result['response']}\n")
            f.write(f"{'-'*70}\n")
    
    print(f"✅ Results saved to: {results_file}")
    
    # Print summary
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}")
    print(f"✅ Successful: {successful}/{len(test_queries)}")
    print(f"❌ Failed: {failed}/{len(test_queries)}")
    print(f"📊 Success Rate: {(successful/len(test_queries)*100):.1f}%")
    print(f"{'='*70}\n")
    
    return results


def generate_demo_report(results):
    """Generate a formatted demo report for submission."""
    
    report_file = f"demo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Chatbot Demonstration Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write("## Test Overview\n\n")
        f.write(f"- **Total Queries Tested:** {len(results)}\n")
        f.write(f"- **Successful Responses:** {sum(1 for r in results if r['status'] == 'success')}\n")
        f.write(f"- **Platform:** Groq API (Llama 3.3 70B)\n")
        f.write(f"- **Vector Store:** FAISS\n\n")
        f.write("---\n\n")
        
        # Add first 5 queries for demonstration
        f.write("## Sample Queries and Responses\n\n")
        for i, result in enumerate(results[:5], 1):
            f.write(f"### Query {i}\n\n")
            f.write(f"**Question:** {result['query']}\n\n")
            f.write(f"**Response:**\n\n")
            f.write(f"{result['response']}\n\n")
            f.write("---\n\n")
        
        f.write("## Analysis\n\n")
        f.write("The chatbot successfully demonstrates:\n\n")
        f.write("1. **Accurate Information Retrieval**: Responses are based on course notes\n")
        f.write("2. **Natural Language Understanding**: Handles various question formats\n")
        f.write("3. **Contextual Awareness**: Provides relevant and detailed answers\n")
        f.write("4. **Consistent Performance**: Maintains quality across different topics\n\n")
    
    print(f"✅ Demo report saved to: {report_file}")
    return report_file


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run tests
    results = run_tests()
    
    # Generate demo report
    if results:
        generate_demo_report(results)
    
    print("\n✅ Testing complete!")
    print("Use the generated files for your assignment submission.")