#pragma once

#include <atomic>
#include <map>
#include <string>
#include <thread>


#include "ChannelServer.hpp"
#include "Session.hpp"
#include "RemoteCallback.hpp"
#include "DfiiBridgeCore.hpp"

class DfiiBridgeServer;

/**
 * @brief   Callback function that gives back the pid information of the server.
 * @details It can be used to ping the server and to get some response.
 */
class InfoRemoteCallback : public RemoteCallback
{
public:
    InfoRemoteCallback() = default;
    std::string callback(DfiiBridgeClient* ws, ExecArgumentVector args);
};

/**
 * @brief   Callback function that exits the attached server if called.
 * @details The server.listen() function will stop if this callback is triggered.
 *          It will not lead to an exit of Virtuoso or whatever application
 *          is using this DfiiBridgeServer. It will only kill the server.
 */
class ExitRemoteCallback : public RemoteCallback
{
private:
    DfiiBridgeServer* server;
public:
    ExitRemoteCallback(DfiiBridgeServer* server);
    std::string callback(DfiiBridgeClient* ws, ExecArgumentVector args);
};

/**
 * @brief   Implements the endpoint (Receiver/Server) of a DfiiBridge network.
 * @details The server can listen for remote function calls.
 *          The remote functions must implement the interface \ref RemoteCall.
 *          These functions can be implemented as C++ classes as well as in Python.
 *          Instances of these implementations are registered with the method \ref register_function
 *          the and methods and removed with.
 *
 *          You have to start the listing explict with the methode \ref listen or \ref listen_async.
 *          There are two diffent modes available: the synchronous mode, where the thread
 *          in which the server instance was started blocks, and the asynchronous mode. In this mode,
 *          an internal thread is created for the listing, so that the thread in which the
 *          server was started is not blocked and is available for other tasks.
 *          The remote function calls are executed if a suitable callback has been registered.
 *          The asynchronous listing can be ended explicitly by calling the method \ref stop.
 *          After that method call you must recall \ref listen or \ref listen_async to enable
 *          the listening again.
 *
 *          The class uses a instance of the class \ref ChannelServer to establish and handle a
 *          socket for the client communications.
 *
 *          The activities of these classes can be logged using a separate logging callback.
 *          To do this, a suitable class instance of the interface \ref LoggingCallback must
 *          be registered: call the function \ref register_logging_function. The same instance
 *          can be registered once, but different instances with different implementation can be
 *          used. A call of \ref unregister_logging_function removes the instance.
 */
class DfiiBridgeServer : public DfiiBridgeCore
{
private:
    ChannelServer channel;

    /**
     * @brief The remote callback for exiting the dfiibridge server
     */
    ExitRemoteCallback exit_callback;

    /**
     * @brief The remote callback for getting information about the dfiibridge server
     */
    InfoRemoteCallback info_callback;

    /**
     * @brief The thread to execute the remote function class in an asynchronous manner.
     */
    std::thread* thread;
    Session host_session;

    /**
     * @brief Map of the registered callback instances
     */
    std::map<std::string, RemoteCallback*> known_functions;



    /**
     * @brief The internal thread safe flag to indicate, that the listen_async has been called.
     */
    std::atomic<bool> listening;

    void bind_free_port();

public:

    /**
     * @brief   Construct a new DfiiBridge Server object.
     * @details In this case, the server is not bound to any session or port and
     *          cannot listen to any clients. You must explicit call \ref listen
     *          or \ref listen_async to start listing of any client connections.
     *          At the same time, the instance is bound to a socket and a free port
     *          for communication with possible clients.
     *          A new instance of a \ref CoreSessionManager is created to manage
     *          the internal session.
     */
    DfiiBridgeServer();

    /**
     * @brief   Construct a new DfiiBridgeServer object.
     * @details This constructors calls the default constructor \ref DfiiBridgeServer()
     *          and adds the user data.
     *
     * @param userdata <key,value> pairs for the user data
     */
    DfiiBridgeServer(const UserDataMap& userdata);

    /**
     * @brief   Construct a new DfiiBridge Server object.
     * @details This constructors calls the default constructor \ref DfiiBridgeServer()
     *          and assigns the specified \ref CoreSessionManager instance.
     *          The optional user datas are also assigned.
     *
     * @param csm The core sessions manager used
     * @param userdata Optional <key,value> pairs for the user data
     */
    DfiiBridgeServer(const CoreSessionManager& csm,
                     const UserDataMap& userdata = {});

    /**
     * @brief   Destroy the DfiiBridge server instance.
     * @details The associated session file is deleted and waits until the internal thread
     *          for the remote function execution finishs its excution.
     */
    ~DfiiBridgeServer();

    /**
     * @brief   Update the userdata of the host_session
     * @details This will update the userdata on the host_session variable
     *
     * @param userdata Optional <key,value> pairs for the user data
     */
    void set_userdata(const UserDataMap& userdata);

    /**
     * @brief   Stops the listening
     * @details The method wait until the internal thread for the asynchronous function execution has finished.
     */
    void stop();

    /**
     * @brief   Start a server and listen from requests from client.
     * @details The method works synchronously in the thread that called it, the caller is blocked
     *          until the method exits.
     *
     * @throws std::runtime_error if no request receives during the timeout period
     */
    void listen();

    /**
     * @brief   Start the internal thread and listen from requests from client.
     * @details The method works asynchronously and does not block the thread  that called the method.
     *          The internal runs until it will be stop by calling \ref stop or until the
     *          DfiiBridgeServer is deleted.
     *          If this method is called several times in a row, the active internal thread is deleted beforehand.
     */
    void listen_async();

    /**
     * @brief Generate random key of the length \len for the session.
     *
     * @param len int the key length
     * @return std::string the generatd key
     */
    std::string gen_random_key(int len) const;

    /**
     * @brief Handle the payload data.
     * @details The method tries to pass the data from the payload to the registered callback instances.
     *          The method gets the name of the corresponding registered callback instance,
     *          checks the validity of the key and passes the parameters to the callback instance.
     *          The JSON string must have the mandatory structure:
     *          {
     *            'func' : name of the registered instance
     *            'key'  : a valid session key
     *            'args' : a vector with the payload values of type std::vector<std::string>
     *          }
     *
     * @throws std::runtime_error if the keywords 'func', 'key' and 'args' are missing in the JSON structure
     * @param payload a JSON string with the payload data
     * @return std::string Responsefrom the executed callback instance
     */
    std::string handle_one_request(const nlohmann::json& payload);

    /**
     * @brief Register a remote callback instance.
     *
     * @throws std::runtime_error if the name is empty or has been registered yet
     * @throws std::runtime_error if the instance pointer is a null pointer
     * @param name Unique registration name
     * @param func pointer of the callback instance
     */
    void register_function(const std::string& name, RemoteCallback* func);

    /**
     * @brief Get a const reference of the session object
     *
     * @return const Session&
     */
    const Session& get_session() const;

    /**
     * @brief Get the used hostname
     * @details The returned value must not be empty for a correctly initialized instance.
     *
     * @return The host name
     */
    std::string get_hostname() const;

    /**
     * @brief   Get the path name of the session file.
     *
     * @throws std::runtime_error if the session file does not exist.
     * @return std::string the absolute file name
     */
    std::string get_session_file_path() const;

    /**
     * @brief   Get the used port number
     * @details The returned value must be greater than 0 for a correctly initialized instance .
     *
     * @return  int the port number
     */
    int get_port() const;

    /**
     * @brief   Check if server is listening
     *
     * @return  bool, true if the server is currently listening
     */
    bool is_listening() const;
};
