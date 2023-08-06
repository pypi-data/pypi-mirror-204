#pragma once

#include <string>

#include "Channel.hpp"
#include "Session.hpp"


/**
 * @brief   The class implements the client channel to send and receive string messages from a server.
 * @details The class has a \ref Session instance to communicate with the server session. This session
 *          This session can be specified directly when instantiating the classes or at a later point in time.
 *          The method \ref set_target_session for this is provided.
 *          After creating an instance of this class, it is not immediately able to send or receive messages.
 *          The instance must be explicitly connected to your respective server session. To do this
 *          the method \ref connect must be called. Otherwise a runtime exception is thrown.
 *
 *          This class uses a ZMQ socket of type ZMQ_REQ to send requests.
 */
class ChannelClient : public Channel
{
private:
    Session target_session;
public:
    std::string endpoint;  // tcp://127.0.0.1:9999
    bool connected;
public:

    /**
     * @brief   The default constructor
     * @details An instance created with this constructor cannot send or receive any messages.
     *          The corresponding server connection is missing. All these attempts lead to a std::run_time exception.
     */
    ChannelClient();

    /**
     * @brief   Construct a new Channel Client instance and set the target session to the passed session.
     * @details An instance created with this constructor cannot send or receive any messages.
     *          The corresponding server connection is missing. All these attempts lead to a std::run_time exception.
     *
     * @param session
     */
    ChannelClient(const Session& session);

    /**
     * @brief   Construct a new Channel Client instance.
     * @details The associated server session is described by the JSON data structure and must contain
     *          the mandatory session parameters. These are described in \ref Session.
     *          Otherwise an exception is thrown.
     *          An instance created with this constructor cannot send or receive any messages.
     *          The corresponding server connection is missing. All these attempts lead to a std::run_time exception.
     */
    ChannelClient(const nlohmann::json&);


    ChannelClient(const ChannelClient&) = delete;
    ChannelClient& operator=(const ChannelClient& rhs) = delete;

    /**
     * @brief Close the connection to the server session and destroy the instance.
     */
    ~ChannelClient();

    /**
     * @brief Connect to the server session
     */
    void connect();

    /**
     * @brief   Connect to the passed endpoint.
     * @details The method tries to establish a connection until it succeeds or
     *          the maximum number of attempts is exceeded. The endpoint to connect to
     *          is specified by a string of the format format of tcp://0.0.0.0:<port_number>.
     *          If the current instance is allready connected, no new connection attempt is made.
     *          This also happens, if the connection string should be change. In the use case,
     *          the current connection must be closed before (call \ref close before).
     *
     * @throws std::runtime_error if the maximum number of connection attempts is reached
     * @throws std::runtime_error if an invalid connection string is used
     * @param conn_str The connection address string
     * @param maxConnectionsAttempts
     */
    void connect(const std::string& conn_str, const int maxConnectionsAttempts = 3);

    /**
     * @brief Close the current connection and connect to the last connected endpoint.
     */
    void reconnect();

    /**
     * @brief   Try to receive data from the connected session socket.
     * @details The method verify, if the current instance is connected and calls the base class method.
     *          \see Channel::recv_string
     *
     * @throws std::runtime_error if the current instance isn't connected
     * @param timeout The timeout value in milli seconds
     * @param flags flag how ZeroMQ should treat the receiving
     * @return std::string The null terminated response string
     */
    std::string recv_string(int timeout = -1, zmq::recv_flags flags = zmq::recv_flags::none) override;

    /**
     * @brief   Send the passed data to the connected session socket.
     * @details The method verify, if the current instance is connected and calls the base class method.
     *          The string data to be send must be null terminated otherwise an exception is thrown.
     *          \see Channel::send_string
     *
     * @throws std::runtime_error if a null pointer or empty data is passed
     * @throws std::runtime_error if the current instance isn't connected
     * @param data The datw which should be send.
     * @param flags flag how ZeroMQ should treat the request when sending
     * @param timeout_ms Timeout in ms for sending (default: -1 (infinite))
     */
    void send_string(const char *data, zmq::send_flags flags = zmq::send_flags::none, int timeout_ms=-1);

    /**
     * @brief Set the target session.
     *
     * @param session
     */
    void set_target_session(Session session);

    /**
     * @brief Get the target session.
     *
     * @return const Session&
     */
    const Session& get_target_session() const;

    /**
     * @brief Get the hostname of the target session.
     *
     * @return std::string The target session hostname
     */
    std::string get_target_hostname() const;

    /**
     * @brief Get the port number of the target session.
     *
     * @return int Thet target session port number
     */
    int get_target_port() const ;

    /**
     * @brief Get the key of the target session.
     *
     * @return std::string The target session key value
     */
    std::string get_target_key() const ;
};
