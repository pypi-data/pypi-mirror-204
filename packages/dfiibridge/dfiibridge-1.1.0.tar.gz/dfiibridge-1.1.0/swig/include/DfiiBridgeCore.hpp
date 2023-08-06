#pragma once

#include "LoggingCallback.hpp"
#include "CoreSessionManager.hpp"

/**
 *  @brief  Abstract base class for DfiiBridge servers and clients.
 *  @details The class contains functions to register and unregister a logging callback instance and
 *           serval functions to log a string message.
 *           These functions forward the message to the registered callback instances, which actually
 *           do the logging.
 *           The class contains a reference of the used \ref CoreSessionManager.
 **/
class DfiiBridgeCore
{
protected:

    /**
     * @brief  The list of the  registered logging callback instances
     */
    LoggingCallbackList loggerCallbacks;

    /**
     * @brief The method logs for each registered callback instance the passed level and message.
     *        The callback is called, when the passed log level is higher than the current set level.
     *        An empty messge isn't logged.
     *
     * @param logLevel the log level
     * @param message the log message
     */
    void logMessage(const LogLevel logLevel, const std::string &message);


    CoreSessionManager session_manager;

    /**
     * @brief Log a message for log level DEBUG
     *
     * @param message the string message
     */
    void logDebug(const std::string &message) { logMessage(LogLevel::DEBUG, message); }

    /**
     * @brief Log a message for log level INFO
     *
     * @param message the string message
     */

    void logInfo(const std::string &message) { logMessage(LogLevel::INFO, message); }

    /**
     * @brief Log a message for log level ERROR
     *
     * @param message the string message
     */
    void logError(const std::string &message) { logMessage(LogLevel::ERROR, message); }

    /**
     * @brief Log a message for log level WARNING
     *
     * @param message the string message
     */
    void logWarning(const std::string &message) { logMessage(LogLevel::WARNING, message); }


    /**
     * @brief Constructor
     */
    DfiiBridgeCore() = default;

    /**
     * @brief Construct a new instance and set the internal reference to the passed core session manager
     *
     * @param csm
     */
    DfiiBridgeCore(const CoreSessionManager& csm);

    virtual ~DfiiBridgeCore(){}; // to make the class abstract

public:


    CoreSessionManager* get_session_manager();

    /**
     * @brief Register a new logging callback instance if the instance isn't stored in the list yet
     *
     * @param instance
     */
    void register_logging_function(LoggingCallback_t instance);


    /**
     * @brief Removes the passed instance from the list of registered logging callbacks.
     *
     * @param instance
     */
    void unregister_logging_function(LoggingCallback_t instance);


};
