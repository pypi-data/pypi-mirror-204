import os
os.environ["PYTHON_JULIAPKG_PROJECT"] = os.path.dirname(__file__)
import juliapkg
juliapkg.resolve()

import juliacall
