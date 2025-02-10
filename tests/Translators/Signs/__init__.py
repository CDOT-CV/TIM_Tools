import sys
import os

# Add the Signs directory to the path so that relative imports work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SCRIPT_DIR, '..', '..', '..', 'Translators', 'Signs'))
sys.path.append(os.path.join(SCRIPT_DIR, '..', '..', '..', 'Translators', 'Shared'))