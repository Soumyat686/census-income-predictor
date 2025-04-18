import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

#from income_predictor.config.core import PACKAGE_ROOT
#with open(PACKAGE_ROOT / "VERSION") as version_file:
__version__ = "0.0.1"
