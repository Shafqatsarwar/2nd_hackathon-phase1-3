import sys
import os
from pathlib import Path

# Add the backend directory to sys.path
root_dir = Path(__file__).parent.parent
backend_dir = str(root_dir / "src" / "backend")
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from main import app

# Vercel expects a module-level variable named 'app'
# This file bridges the Vercel Serverless Function to our existing FastAPI app.
