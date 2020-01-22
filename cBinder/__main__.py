import os
import sys

# allow imports from cBinder
if __package__ == '':
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

from cBinder.main import main   # noqa: E402

if __name__ == '__main__':
    main()
