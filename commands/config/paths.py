
# commands/config/paths.py
import sys
from pathlib import Path

# =============== PATH SETUP

# Current directory: commands/config/
current_dir = Path(__file__).resolve().parent
# Project root directory
parent_dir = current_dir.parent
# Add root to import path
sys.path.insert(0, (parent_dir))
