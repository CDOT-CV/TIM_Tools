import sys
import os

# Add both the WZDx and Shared directories to the path so that relative imports work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SCRIPT_DIR, '..', '..', '..', 'Translators', 'WZDx'))
sys.path.append(os.path.join(SCRIPT_DIR, '..', '..', '..', 'Translators', 'Shared'))