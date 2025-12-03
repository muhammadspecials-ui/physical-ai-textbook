"""
Quick test script to verify backend setup.
Run this to check if all services are configured correctly.
"""

import sys
from pathlib import Path

def test_imports():
    """Test if all required packages are installed."""
    print("Testing imports...")
    try:
        import fastapi
        import uvicorn
        import openai
        from qdrant_client import QdrantClient
        import sqlalchemy
        import bcrypt
        import jwt
        print("✅ All packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Run: pip install -r requirements.txt")
        return False


def test_env_file():
    """Test if .env file exists and has required variables."""
    print("\nTesting environment configuration...")
    
    if not Path('.env').exists():
        print("❌ .env file not found")
        print("Copy .env.example to .env and fill in your credentials")
        return False
    
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    required_vars = [
        'OPENAI_API_KEY',
        'QDRANT_URL',
        'DATABASE_URL',
        'AUTH_SECRET'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        return False
    
    print("✅ All environment variables configured")
    return True


def test_openai():
    """Test OpenAI API connection."""
    print("\nTesting OpenAI API...")
    try:
        from config import settings
        from openai import OpenAI
        
        client = OpenAI(api_key=settings.openai_api_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'test successful'"}],
            max_tokens=10
        )
        
        print(f"✅ OpenAI API working: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return False


def test_qdrant():
    """Test Qdrant connection."""
    print("\nTesting Qdrant connection...")
    try:
        from qdrant_service import qdrant_service
        
        # Try to create collection
        qdrant_service.create_collection()
        
        # Test adding a document
        test_doc = [{
            "text": "This is a test document",
            "metadata": {"source": "test"}
        }]
        qdrant_service.add_documents(test_doc)
        
        # Test search
        results = qdrant_service.search("test", limit=1)
        
        if results:
            print(f"✅ Qdrant working: Found {len(results)} results")
            return True
        else:
            print("⚠️ Qdrant connected but no results found")
            return True
    except Exception as e:
        print(f"❌ Qdrant error: {e}")
        return False


def test_database():
    """Test database connection."""
    print("\nTesting database connection...")
    try:
        from database import init_db, SessionLocal, User
        
        # Initialize database
        init_db()
        
        # Test connection
        db = SessionLocal()
        user_count = db.query(User).count()
        db.close()
        
        print(f"✅ Database working: {user_count} users in database")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("Physical AI Textbook - Backend Test Suite")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Environment Config", test_env_file),
        ("OpenAI API", test_openai),
        ("Qdrant Vector DB", test_qdrant),
        ("Database", test_database),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"❌ {name} failed with exception: {e}")
            results[name] = False
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! Backend is ready to run.")
        print("\nStart the server with: python main.py")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
