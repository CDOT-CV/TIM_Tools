import sys
import os

# Add the RoadConditions directory to the path so that relative imports work
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SCRIPT_DIR, '..', '..', '..', 'Translators', 'RoadConditions'))