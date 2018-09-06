synthraw
========

Synthesizes camera raw files (`DNG <https://helpx.adobe.com/photoshop/digital-negative.html>`_ format) using Python. Requires `libtiff <http://www.libtiff.org>`_.

Installation
------------

.. code-block:: bash

   pip3 install numpy pillow
   python3 setup.py install

Usage
-----

From the command line:

.. code-block:: bash

   synthraw in.png out.dng

From Python:

.. code-block:: python

   import numpy as np
   from synthraw import DNG

   # Create a 32x32 pixel array
   data = np.zeros((32, 32), dtype=np.uint16)
   # Set one pixel to white
   data[1, 1] = 65535
   dng = DNG('out.dng')
   dng.write_data(data)
   dng.close()
