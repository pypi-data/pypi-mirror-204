DfiiBridge
==========

This tool provides a Python based server that enables you to connect to your Virtuoso sessions and control it remotely using SKILL and Python commands.
It is based on the public SKILL bridge (https://github.com/unihd-cag/skillbridge).
But there has been some major changes:

- Authentication added
- Improved session management (multiple hosts, search and filtering options)
- Keep Cadence camel case naming
- Introduced c++ SWIG to support other languages than Python (currently only perl is available as well)
- Improved logging
- Added reverse communication channel (calling Python methods from Skill)

Installation
------------

Prerequisits:

- cmake 3.14
- gcc >=10.3
- libzmq
- swig

To run the component tests, just call:
```
tox
```

This command creates a new virtual python environment and installs the DfiiBdrige there.

Getting started
---------------

Start Virtuoso.
Load the `dfiiBridgeClient.il`, `dfiiBridgeServer.il` and `dfiiBridgeUtils.il` in the CIW.
To start the Virtuoso server call:
```
DfiiBridge_startServer()
```

To connect to the Virtuoso session and get the workspace object, open a terminal inside of Virtuoso
and call the following python commands:

```
from dfiibridge import VirtuosoSessionManager

vm = VirtuosoSessionManager()
ws = vm.get_workspace()
ws.skill.println("Hello World")
```
