.. Auxiliary doc for laying out the attribute inheritance cascades

Attribute Inheritance
=====================

stdio_mgr.StdioManager
----------------------

.. runblock:: pycon

    >>> from runpy import run_path  # ignore
    >>> attr_origins = run_path("attr_origins.py")['attr_origins']  # ignore
    >>> from stdio_mgr.stdio_mgr import StdioManager
    >>> attr_origins(StdioManager)
