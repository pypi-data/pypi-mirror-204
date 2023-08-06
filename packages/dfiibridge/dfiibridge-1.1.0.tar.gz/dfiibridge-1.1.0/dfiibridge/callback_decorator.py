
from dfiibridge_core import DfiiBridgeClient, RemoteCallback, LoggingCallback
from .workspace import Workspace

def log_callback(func):
    """Decorator for LoggingCallbacks

    Args:
        func (Callable): Function that looks like: def my_func(log_level, log_message)->None

    Returns:
        LoggingCallback: Instance of the LoggingCallback
    """
    class DecoratorLoggingCallback(LoggingCallback):
        def log(self, log_level, log_message):
            try:
                func(log_level, log_message)
            except Exception as e:
                print(f"ERROR: {e}")
                raise
    return DecoratorLoggingCallback()

def callback(func):
    """Decorator for RemoteCallbacks

    Args:
        func (Callable): Function that looks like: def my_func(origin_client:DfiiBridgeClient, raw_args:list)->str

    Returns:
        RemoteCallback: Instance of the RemoteCallback
    """
    class DecoratorCallback(RemoteCallback):
        def callback(self, origin_client:DfiiBridgeClient, raw_args:list)->str:
            try:
                return func(origin_client, *raw_args)
            except Exception as e:
                return f"failure {e}"
    return DecoratorCallback()


def skill_callback(func):
    """Decorator for RemoteCallbacks that can be called from skill

    This decorator does the translation of the arguments and the translation of the return type
    for you.

    Args:
        func (Callable): Function that looks like: def my_func(origin_ws:Workspace, args:list)->str

    Returns:
        RemoteCallback: Instance of the RemoteCallback
    """
    class DecoratorCallback(RemoteCallback):
        def callback(self, origin_client:DfiiBridgeClient, raw_args:list)->str:

            try:
                if not origin_client:
                    return "failure No origin server found! Is it really listening?"

                origin_sessions = origin_client.get_connected_sessions()

                if len(origin_sessions)!=1:
                    return "failure No or multiple connected sessions on origin_client! This should not happen."

                origin_ws = Workspace(origin_sessions[0])

                func_args = []
                for arg in raw_args:
                    func_args.append(origin_ws._translator.decode(arg))

                answ = func(origin_ws, *func_args)
                return origin_ws._translator.encode(answ)

            except Exception as e:
                return f"failure {e}"

    return DecoratorCallback()
