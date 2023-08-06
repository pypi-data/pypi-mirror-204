#pragma once

#include "globals.hpp"

class DfiiBridgeClient;

/**
 * @brief Functor for executing remote callback.
 *        The callback can be implemented as a plain C++ or python class.
 **/
class RemoteCallback
{
public:
    virtual std::string callback(DfiiBridgeClient* ws, ExecArgumentVector args) = 0;

    /**
     * @brief The default generated destructor.
     */
    virtual ~RemoteCallback(){};
};
