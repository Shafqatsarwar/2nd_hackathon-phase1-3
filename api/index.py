import sys
import os
from pathlib import Path

# Add the project root to sys.path
root = Path(__file__).parent.parent
sys.path.append(str(root))

from src.backend.main import app

# Vercel expects a module-level variable named 'app'
# This file bridges the Vercel Serverless Function to our existing FastAPI app.
