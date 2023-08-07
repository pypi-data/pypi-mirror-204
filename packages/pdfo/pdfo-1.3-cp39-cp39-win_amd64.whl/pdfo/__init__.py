# -*- coding: utf-8 -*-
"""Management of the importable functions of pdfo.

Authors
-------
Tom M. RAGONNEAU (tom.ragonneau@polyu.edu.hk)
and Zaikun ZHANG (zaikun.zhang@polyu.edu.hk)
Department of Applied Mathematics,
The Hong Kong Polytechnic University.

Dedicated to the late Professor M. J. D. Powell FRS (1936--2015).
"""


# start delvewheel patch
def _delvewheel_init_patch_1_3_6():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pdfo.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if not is_pyinstaller or os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-pdfo-1.3')
        if not is_pyinstaller or os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-pdfo-1.3')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if not is_pyinstaller or os.path.isfile(lib_path):
                    ctypes.WinDLL(lib_path)


_delvewheel_init_patch_1_3_6()
del _delvewheel_init_patch_1_3_6
# end delvewheel patch


from datetime import datetime

try:
    # Enable subpackage importing when binaries are not yet built.
    __PDFO_SETUP__  # noqa
except NameError:
    __PDFO_SETUP__ = False

# Definition of the metadata of PDFO for Python. It is accessible via:
# >>> import pdfo
# >>> print(pdfo.__author__)
# >>> ...
__author__ = 'Tom M. Ragonneau and Zaikun Zhang'
__copyright__ = f'Copyright 2020--{datetime.now().year}, ' \
                f'Tom M. Ragonneau and Zaikun Zhang'
__credits__ = ['Tom M. Ragonneau', 'Zaikun Zhang', 'Antoine Dechaume']
__license__ = '3-Clause BSD'
__version__ = '1.3'
__date__ = 'April, 2023'
__maintainer__ = 'Tom M. Ragonneau and Zaikun Zhang'
__email__ = 'tom.ragonneau@polyu.edu.hk and zaikun.zhang@polyu.edu.hk'
__status__ = 'Production'

if not __PDFO_SETUP__:

    from ._dependencies import OptimizeResult, Bounds, LinearConstraint, \
        NonlinearConstraint

    from ._bobyqa import bobyqa
    from ._cobyla import cobyla
    from ._lincoa import lincoa
    from ._newuoa import newuoa
    from ._uobyqa import uobyqa
    from ._pdfo import pdfo
    from . import tests
    from .tests import test_pdfo as testpdfo
    __all__ = ['OptimizeResult', 'Bounds', 'LinearConstraint',
               'NonlinearConstraint', 'bobyqa', 'cobyla', 'lincoa', 'newuoa',
               'uobyqa', 'pdfo', 'tests', 'testpdfo']