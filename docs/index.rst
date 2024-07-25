Welcome to the DT4Safeguards documentation!
=======================================


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Introduction
------------
DT4Safeguards (Digital Twin for Safeguards in Nuclear Waste Management) is a python framework modeling safeguards activities in nuclear facilities related to the process of the disposal of nuclear waste.

The project can be found in the following repository:
https://github.com/manuel-k2/DT4Safeguards

Requirements
------------
Make sure you have all required packages installed:

`pip install -r requirements.txt`

Results
-------
The results were visualized with Dash and can be displayed locally. Run the Dash app via:

`python3 project/app.py`

Results are then visible with a browser at http://127.0.0.1:8050/.

Modules
-------

.. automodule:: project.app
    :members:

.. automodule:: project.model.monitoringsystem
    :members:

.. automodule:: project.model.historyclass
    :members:

.. automodule:: project.model.facility
    :members:

.. automodule:: project.model.room
    :members:

.. automodule:: project.projecttypes.command
    :members:

.. automodule:: project.projecttypes.transportcmd
    :members:

.. automodule:: project.projecttypes.location
    :members:

.. automodule:: project.projecttypes.dimensions
    :members: