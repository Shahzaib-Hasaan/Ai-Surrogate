"""
Test script to verify database connection and create tables.

Run this script to:
1. Test database connection
2. Create all tables in Supabase
3. Verify models are working correctly
"""

from app.database import engine, Base, init_db
from app.models import User, Conversation, Message

def main():
    """Test database connection and create tables."""
    
    print("🔄 Testing database connection...")
    
    try:
        # Test connection
        with engine.connect() as connection:
            print("✅ Database connection successful!")
        
        # Create all tables
        print("\n🔄 Creating database tables...")
        init_db()
        
        # List all tables
        print("\n✅ Database tables created successfully!")
        print(f"\n📊 Tables created:")
        for table_name in Base.metadata.tables.keys():
            print(f"   - {table_name}")
        
        # Show model information
        print(f"\n📝 Models registered:")
        print(f"   - User: {User.__tablename__}")
        print(f"   - Conversation: {Conversation.__tablename__}")
        print(f"   - Message: {Message.__tablename__}")
        
        print("\n🎉 Database setup complete!")
        print("\n💡 Next steps:")
        print("   1. Check Supabase dashboard to see the tables")
        print("   2. Continue with Pydantic schemas creation")
        print("   3. Build authentication service")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔍 Troubleshooting:")
        print("   1. Check your .env file has correct DATABASE_URL")
        print("   2. Verify Supabase project is active")
        print("   3. Check internet connection")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
