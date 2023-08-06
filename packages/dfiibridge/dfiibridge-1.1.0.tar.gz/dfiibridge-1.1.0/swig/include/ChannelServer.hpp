#pragma once

#include "Channel.hpp"

/**
 * @brief   The class implements the server channel to recieve requests and to send sponses from a client.
 * @details The class has a ZMQ socket to receive and send the data. After creating an instance of this class,
 *          it is not immediately able to receive messages, the socket is not binded to any address or port.
 *          This socket must be explicitly bound to an address and port in order for requests to be received.
 *          The class has the 2 methods  \ref bind_free_port \ref bind for this.
 *
 *          The class uses a ZMQ socket of type ZMQ_REP to send requests.
 */
class ChannelServer : public Channel
{

private:

    /**
     * @brief   Parse the port number from the IP4 address.
     * @details The passed address must have the format of tcp://0.0.0.0:<port_number>
     *
     * @param address The IP address and port number
     * @return int The port number
     */
    int parse_port_from_address(const std::string& address) const;

public:

    /**
     * @brief The address and port number of binded socket.
     *        The value looks like tcp://0.0.0.0:<port_number>.
     */
    std::string bind_address;

    /**
     * @brief  Construct a new Channel Server object
     */
    ChannelServer();
    ChannelServer(const ChannelServer&) = delete;
    ChannelServer& operator=(const ChannelServer& rhs) = delete;

    /**
     * @brief Close the binded socket and destroy the instance.
     */
    ~ChannelServer();

    /**
     * @brief   Bind the socket to the passed address.
     * @details The passed address string must have the format tcp://<IP4 address>:<port_number
     *
     * @param bind_address The address and port number to binded to
     */
    void bind(const std::string& bind_address);

    /**
     * @brief Bind the socket to the next free port
     *
     */
    void bind_free_port();

    /**
     * @brief Get the port number
     *
     * @return int the binded port number
     */
    int get_port() const;
};
