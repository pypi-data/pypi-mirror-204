#pragma once

#include <zmq.hpp>
#include <string>
#include <iostream>
#include "globals.hpp"

class ChannelTimeoutReceive : public std::runtime_error {
    public:
        ChannelTimeoutReceive(const std::string& msg)
            : std::runtime_error(msg)
        {
        };
};

/**
 * @brief   Base class to implement the sendinng and the receiving of text messages.
 * @details The class uses a socket for sending.
 *          The C++ library cppzmq is used to abstract the socket access and to implement
 *          the sending and receiving of the text message. More infos about the library offers
 *          the page:  https://github.com/zeromq/cppzmq
 */
class Channel
{
protected:

    /**
     * @brief The used ZeroMQ context.
     *
     */
    zmq::context_t zmq_context;

    /**
     * @brief The used ZeroMQ socket
     *
     */
    zmq::socket_t socket;

protected:
    Channel(int socktype);

    /**
     * @brief Create a socket object for specified type.
     *
     * @param socktype  The socket type
     * @return zmq::socket_t
     */
    zmq::socket_t create_socket(int socktype);

public:

    /**
     * @brief Destroy the Channel object
     */
    virtual ~Channel(){};

    /**
     * @brief Close the socket.
     */
    void close();

    /**
     * @brief   Send the passed data to the connected session socket.
     * @details The string data to be send must be null terminated otherwise an exception is thrown.
     *          The method checks that all bytes of the request could be sent, i.e. that the request
     *          could be completely forwarded to the server session.
     *
     * @throws std::run_time_error if not all bytes of the request could be sent
     * @throws std::runtime_error if a null pointer or empty data is passed
     * @param data The datw which should be send.
     * @param flags flag how ZeroMQ should treat the request when sending
     * @param timeout Timeout in ms (default: -1 (infinite))
     */
    virtual void send_string(const char* data, zmq::send_flags flags = zmq::send_flags::none, int timeout_ms = -1);

    /**
     * @brief   Receive data from the connected session socket in blocking mode.
     * @details The method tries to receive a response from the server session and waits, if no timeout
     *          value is specified, until the server has completely transmitted its request. This wait
     *          can be very long.
     *          IUf a timeout value was specified, this is the maximum time that is waited until the
     *          complete request has to be received. If this time elapses, an exception is thrown and
     *          no response is returned.
     *          This happens also, if the complete request could not be received.
     *
     * @throws std::runtime_error if not all bytes of the response could be received
     * @param timeout_ms The timeout value in milli seconds (default: -1 (infinite))
     * @param flags flag how ZeroMQ should treat the receiving
     * @return std::string The null terminated response string
     */
    virtual std::string recv_string(int timeout_ms = -1, zmq::recv_flags flags = zmq::recv_flags::none);

    /**
     * @brief   Get the hostname
     * @details The method tries to get the hostname hostname by either calling the function gethostname or
     *          reading the environment variable HOSTNAME.
     *
     * @throws std::runtime_error if no hostname could be determined
     * @return std::string The hostname
     */
    std::string get_hostname() const;
};
