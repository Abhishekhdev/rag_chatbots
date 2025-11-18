"""
Modules package initialization.

This makes 'modules' a proper Python package
so other scripts can import from it (e.g., test_rag_agent.py).
"""

import os
import sys

# Ensure the project root is in sys.path (helps avoid import errors)
PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(PACKAGE_ROOT, os.pardir))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
