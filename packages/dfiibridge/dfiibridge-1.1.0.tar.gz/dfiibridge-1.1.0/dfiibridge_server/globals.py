import re

import importlib.resources

COMMAND_VIRTUOSO = lambda gui, init, path_to_skill_server: ["virtuoso", gui, init, "-replay", path_to_skill_server]

# Session creation pattern to find DfiiBridge information in Virtuoso stdout
DFII_LABEL_PATTERN = r"^\[INFO\]\s+DfiiBridge\s+running\s+on\s+(.*?):(\d+)\s+status:(\w+)"

DFII_LABEL_PATTERN = re.compile(DFII_LABEL_PATTERN, re.VERBOSE)

DFII_CLIENT_SKILL = str(importlib.resources.files(__package__) / "dfiiBridgeClient.il")
DFII_SERVER_SKILL = str(importlib.resources.files(__package__) / "dfiiBridgeServer.il")
DFII_UTILS_SKILL =  str(importlib.resources.files(__package__) / "dfiiBridgeUtils.il")
DFII_SERVER_PY =    str(importlib.resources.files(__package__) / "virtuoso_server.py")
DFII_CLIENT_PY =    str(importlib.resources.files(__package__) / "virtuoso_client.py")
