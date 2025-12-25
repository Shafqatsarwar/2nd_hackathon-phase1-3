import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlmodel import Session, select, create_engine, SQLModel

# Add project root to path
root = Path(__file__).parent.parent.parent
sys.path.append(str(root))

from src.backend.models import User, Task
from src.backend.database import engine

def diagnostic():
    load_dotenv()
    print("--- BACKEND DIAGNOSTIC START ---")
    print(f"DATABASE_URL ends with: ...{os.getenv('DATABASE_URL')[-20:] if os.getenv('DATABASE_URL') else 'None'}")
    
    with Session(engine) as session:
        try:
            # 1. Test User Operation
            test_id = "diag-user-123"
            print(f"Checking for user {test_id}...")
            user = session.get(User, test_id)
            if not user:
                print(f"User not found. Creating...")
                user = User(id=test_id, email=f"{test_id}@example.com")
                session.add(user)
                session.commit()
                session.refresh(user)
                print(f"✅ User created: {user.id}")
            else:
                print(f"✅ User found: {user.id}")
            
            # 2. Test Task Operation
            print("Creating test task...")
            task = Task(title="Diagnostic Task", description="Testing DB", user_id=test_id)
            session.add(task)
            session.commit()
            session.refresh(task)
            print(f"✅ Task created: #{task.id}")
            
            # 3. Clean up
            print("Cleaning up...")
            session.delete(task)
            # session.delete(user) # Keep user for consistency
            session.commit()
            print("✅ Cleanup finished.")
            
        except Exception as e:
            print(f"❌ ERROR DURING DIAGNOSTIC: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    diagnostic()
