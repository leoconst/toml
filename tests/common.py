import sys
from pathlib import Path


def augment_path():
    sys.path.insert(0, str(Path(__file__).parent.parent))
