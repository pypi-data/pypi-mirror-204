#pragma once


#include <string>


/**
 * @brief This class defines the interface for the remote logging function callback.
 *        The callback can be implemented as a plain C++ or python class.
 */
class LoggingCallback
{
public:

    /**
     * @brief Log the passed message string for the releated to the log level.
     *
     * @param log_level log level value
     * @param log_message  the message string
     */
    virtual void log(const int log_level, std::string log_message) = 0;

    /**
     * @brief The default generated destructor.
     */
    virtual ~LoggingCallback() = default;
};

/**
 * @brief This log levels defintion is copied from python and
 *        defines the same level values for C++.
 *
 */
enum LogLevel : int { CRITICAL = 50,
    FATAL = CRITICAL,
    ERROR = 40,
    WARNING = 30,
    WARN = WARNING,
    INFO = 20,
    DEBUG = 10,
    NOTSET = 0,
    };
