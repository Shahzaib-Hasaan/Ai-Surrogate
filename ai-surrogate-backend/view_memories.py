"""
View ChromaDB Memories - Standalone Script

Run this to see what's stored in the vector database.
"""

import chromadb
from chromadb import PersistentClient

# Connect to ChromaDB
client = PersistentClient(path="./chroma_db")

# Get the conversations collection
try:
    collection = client.get_collection(name="conversations")
    
    # Get all stored memories
    results = collection.get()
    
    print(f"\n{'='*70}")
    print(f"📊 CHROMADB MEMORY DATABASE")
    print(f"{'='*70}")
    print(f"\n✅ Total memories stored: {len(results['ids'])}\n")
    
    if results['metadatas']:
        for i, metadata in enumerate(results['metadatas'], 1):
            print(f"{'─'*70}")
            print(f"🧠 Memory #{i}")
            print(f"{'─'*70}")
            print(f"👤 User ID: {metadata.get('user_id', 'N/A')}")
            print(f"💬 Conversation ID: {metadata.get('conversation_id', 'N/A')[:20]}...")
            print(f"🕐 Timestamp: {metadata.get('timestamp', 'N/A')}")
            print(f"\n📝 User Message:")
            print(f"   {metadata.get('user_message', 'N/A')}")
            print(f"\n🤖 AI Response:")
            ai_response = metadata.get('ai_response', 'N/A')
            print(f"   {ai_response[:150]}{'...' if len(ai_response) > 150 else ''}")
            print()
    else:
        print("❌ No memories found yet.")
        print("💡 Send some messages through the chat to create memories!")
    
    print(f"\n{'='*70}")
    print(f"💾 Database location: ./chroma_db/")
    print(f"📊 Collection: conversations")
    print(f"{'='*70}\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("💡 Make sure ChromaDB is initialized (send a message first)")
