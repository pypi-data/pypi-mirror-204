#include <iostream>
#include <algorithm>
#include "DfiiBridgeCore.hpp"
#include "Channel.hpp"


DfiiBridgeCore::DfiiBridgeCore(const CoreSessionManager& csm):
    session_manager(csm)
{
    CORE_LOGINFO("Initialize DfiiBridgeCore with a core session manager");
}

CoreSessionManager* DfiiBridgeCore::get_session_manager()
{
    return &this->session_manager;
}


void DfiiBridgeCore::register_logging_function(LoggingCallback_t instance)
{
    loggerCallbacks.insert(instance);
}

void DfiiBridgeCore::unregister_logging_function(LoggingCallback_t instance)
{
    const auto iter = std::find(begin(loggerCallbacks), end(loggerCallbacks), instance);
    if (iter != loggerCallbacks.end())
    {
       loggerCallbacks.erase(iter);
    }
}


void DfiiBridgeCore::logMessage(const LogLevel level, const std::string &message)
{
    if (!message.empty())
    {
        // the client decides what to do with the message and leog level
        for (const auto& cb : loggerCallbacks)
        {
            try
            {
                cb->log(level, message);
            }
            catch(const std::exception& e)
            {
                CORE_LOGINFO("Found invalid log handler. Maybe we are just closing the program.");
                continue;
            }
        }
        CORE_LOGINFO("Log message (" << level << "): " << message);
    }
}