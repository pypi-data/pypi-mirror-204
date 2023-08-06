import os
os.environ["PYTHON_JULIAPKG_PROJECT"] = os.path.join(os.path.dirname(__file__), 'julia')
import juliapkg
juliapkg.resolve()

import juliacall
