#!/usr/bin/env python3

"""
Handles the calls from SKILL:
- read origin, search_criteria, function and function arguments from stdin
- parse them and send them to each custom server that matches the criteria given

Stdin contains the following:
    srcHost:srcPort
    search_criteria
    function_name
    [arguments]\n * N
    <<<<END>>>>

"""

import sys
from dfiibridge_core import DfiiBridgeClient, CoreSessionManager, LoggingCallback
from argparse import ArgumentParser
import os
import io


class ClientLoggingCallback(LoggingCallback):

    def __init__(self, file_name, verbosity:int=0):
        super().__init__()

        self.file_name = file_name
        self.verbosity = verbosity

    def log(self, log_level, log_message):
        #with open(self.file_name,'a') as f:
        #    f.write(f"{datetime.datetime.now()} {log_level}: {log_message}\n")
        print(log_message)

def main(args):

    # read in all lines including the line break from stdin, until <END> marker hit
    raw_args = []

    while True:
        cur_line = sys.stdin.readline()
        if cur_line.strip() == "<<<<END>>>>":
            break
        raw_args += [cur_line.strip()]

    # find sessions for the criteria provided in the message
    csm = CoreSessionManager(args.session_dir)
    client = DfiiBridgeClient(csm)


    if args.hostname and args.port:
        sessions = [csm.get_session(args.hostname, args.port, False)]
    elif args.search_criteria:
        # extract userdata search from args.search_criteria
        userdata = {}
        if args.search_criteria:
            for var in args.search_criteria.split(","):
                k,v = var.split("=")
                userdata[k] = v
        sessions = list(csm.find_sessions(userdata))
    else:
        raise Exception("You need to define a search criteria or a hostname/port!")

    if not sessions:
        raise Exception(f"No sessions are currently running with the filter {userdata}!")

    origin_session = csm.get_session(args.origin_hostname, args.origin_port, False)

    for session in sessions:
        if session == origin_session:
            sessions.remove(session)
            break

    if not sessions:
        raise Exception(f"No session found with the userdata {userdata} (only one but this is the origin session!)")

    if not sessions:
        raise Exception("No session is left. Maybe you try to connect to the origin session? "
                        "This is not possible because it would end up in a self blocking loop.")

    client.set_origin_session(origin_session)

    # check if there is a session with these criteria available
    if not sessions:
        print(f"no sessions found for identifier '{userdata}'!")
        sys.exit(-1)

    # Enable logger if wished
    if args.verbosity<10:
        logger = ClientLoggingCallback("dfiibridge_logger.log")
        client.register_logging_function(logger)

    client.connect_to_endpoints( sessions )

    replies = client.execute(args.function_name, raw_args)

    for reply in replies:
        print("\u2764"+reply, file=sys.stderr, end="") # give reponse for each client

if __name__ == '__main__':

    argument_parser = ArgumentParser(sys.argv[0])
    argument_parser.add_argument('--session_dir',
                                type=str,
                                default=os.path.join(os.environ["HOME"], ".dfiiBridge"),
                                help='Directory to store the session file (default: ~/.dfiiBridge)')
    argument_parser.add_argument('--origin_hostname',
                                type=str,
                                required=True,
                                help='Hostname of the virtuoso_server')
    argument_parser.add_argument('--origin_port',
                                type=int,
                                required=True,
                                help='Port of the virtuoso_server')
    argument_parser.add_argument('--function_name',
                                type=str,
                                required=True,
                                help='Name of the function to call remotely')
    argument_parser.add_argument('-v', '--verbosity', default=30, type=int, help="Set the veribosity level")
    argument_parser.add_argument('--search_criteria',
                                type=str,
                                default="",
                                help="Search criteria ('key1=value1,key2=value2')")
    argument_parser.add_argument('--hostname',
                                type=str,
                                default=None,
                                help="Define the hostname of your target")
    argument_parser.add_argument('--port',
                                type=int,
                                default=None,
                                help="Define the port of your target")
    args = argument_parser.parse_args()

    try:
        main(args)
    except Exception as e:
        print(f"\u2764error(\"{e}\")", file=sys.stderr) # give reponse for each client
