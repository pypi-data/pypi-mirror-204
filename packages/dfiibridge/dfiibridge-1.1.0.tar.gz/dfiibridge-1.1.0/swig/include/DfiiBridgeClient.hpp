#pragma once

#include <string>
#include <map>
#include <vector>
#include <thread>
#include <atomic>

#include "globals.hpp"
#include "RemoteCallback.hpp"
#include "ChannelServer.hpp"
#include "ChannelClient.hpp"
#include "CoreSessionManager.hpp"
#include "DfiiBridgeCore.hpp"

/**
 * @brief   Implements client behavior
 * @details One client instance can connect to different DfiiBridgeServer instances at the same time.
 *          to achive the connection with the server, the method \ref connect_to_endpoint is provided.
 *          The method requires information about the respective server session.
 *          After the connection the client can execute remote functions, which are registered at the
 *          server instances. The method \ref execute is provided for this.
 *          When the client instance is destroyed, the connections to all server instances are closed.
 *          All connections can be closed at any time using the methode \ref clear_endpoints.
 *
 *          The activities of these classes can be logged using a separate logging callback.
 *          To do this, a suitable class instance of the interface \ref LoggingCallback must
 *          be registered: call the function \ref register_logging_function. The same instance
 *          can be registered once, but different instances with different implementation can be
 *          used. A call of \ref unregister_logging_function removes the instance.
 */
class DfiiBridgeClient : public DfiiBridgeCore
{
private:

    /**
     * @brief The origin seession is the server session from which the client expects a response to requests.
     *
     */
    Session origin_session;

    /**
     * @brief List of all connected server instances or channels
     */
    std::vector<ChannelClient*> client_channels;

public:

    /**
     * @brief   Construct a new DfiiBridgeClient object.
     */
    DfiiBridgeClient();

    /**
     * @brief   Construct a new DfiiBridgeClient object and assigns the specified \ref CoreSessionManager instance.
     *
     * @param csm The core sessions manager used
     */
    DfiiBridgeClient(const CoreSessionManager& csm);

    /**
     * @brief   Construct a new DfiiBridgeClient object and creates a \ref CoreSessionManager instance with the specified root path.
     *
     * @param root_path Root path of all session files (default: ~/.dfiiBridge)
     */
    DfiiBridgeClient(const std::string& root_path);

    /**
     * @brief Destroy the Dfii Bridge Client object
     */
    ~DfiiBridgeClient();

    /**
     * @brief Disconnect all DfiiBridgeServer instances.
     */
    void clear_endpoints();

    /**
     * @brief   Connect the client to the passed sessions.
     * @details The method tries to connect the client to each session in the session list.
     *          If the connection setup fails for one session, the associated session file is automatically deleted
     *          and an appropriate error message is logged.
     *          The method tries to connect the next session in list.
     *
     * @param sessions The session list
     */
    void connect_to_endpoints(const SessionVector& sessions);


    /**
     * @brief   Connect the client to the session.
     * @details The associated session is described by the JSON data structure and must contain
     *          the mandatory session parameters. These are described in \ref Session.
     *          Otherwise an exception is thrown.
     *
     *          If the connection to this session cannot be established, the associated session file
     *          is automatically deleted and an appropriate error message is logged.
     *
     * @throws std::runtime_error if one the of the mandatory JSON parameter is missing
     * @param session The JSON session parameters
     */
    void connect_to_endpoint(const nlohmann::json& session);


    /**
     * @brief   Connect the client to the passed session.
     * @details If the connection to this session cannot be established, the associated session file
     *          is automatically deleted and an appropriate error message is logged.
     *
     * @param session The sessionto connect to
     */
    void connect_to_endpoint(const Session& session);

    /**
     * @brief Set the origin session
     * @details Every client can also host its own server that offers a set of functions to the endpoint.
     *          Call this function and set the session to the client's server.
     *          If set, the endpoint can connect back to the client to execute some remote function.
     *
     * @param server
     */
    void set_origin_session(const Session& server);

    /**
     * @brief   Get the origin session
     * @details Every client can also host its own server that offers a set of functions to the endpoint.
     *          This function gets the session file of that server.
     *
     * @return const Session&
     */
    const Session& get_origin_session() const;

    /**
     * @brief Get a vector of all connected sesssions.
     *
     * @return std::vector<Session>
     */
    std::vector<Session> get_connected_sessions() const;

    /**
     * @brief   Send a execution request for a remote callback (see \ref RemoteCallback) to
     *          all connected DfiiBridgeServer instances.
     * @details The remote callback, which should be executed, is specified by the registed name.
     *          The function arguments args are optional and depend on the specific RemoteCallback.
     *          If the flag request_reply is set to true, caller waits until the remote callback
     *          has been fully executed and has returned his result. The caller is therefore blocked.
     *          If the flag request_reply is set to false, the method doesnot wait for the response.
     *
     *
     * @param function_name  The registered name of the callback to be executed.
     * @param args           The optional arguments as a vector of strings
     * @param request_reply  Should wait for the server response
     * @param timeout        Timeout value in milliseconds to wait, until the server response must arrive.
     *                       The value -1 means 'no timeout'.
     * @return ExecResultVector
     */
    ExecResultVector execute(
        const std::string& function_name,
        const ExecArgumentVector& args = {},
        bool request_reply = true,
        int timeout = -1);
};
