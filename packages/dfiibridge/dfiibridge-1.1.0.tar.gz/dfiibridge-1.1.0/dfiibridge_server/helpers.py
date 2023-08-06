"""
This module provides functions to communicate between the server and virtuoso
"""

from sys import stdin, stderr


def execute_inside_skill(data: str) -> str:
    """
    Send skill code to Virtuoso and receive the reply
    """
    stderr.write(">"+data.replace("\n", "\u2764"))
    stderr.write("\n")
    stderr.flush()
    return stdin.readline()


