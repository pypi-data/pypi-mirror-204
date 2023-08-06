#include <unistd.h>
#include <zmq.hpp>
#include <iostream>

#include "globals.hpp"
#include "Channel.hpp"


Channel::Channel(int socktype)
{
    CORE_LOGINFO("Try to create a socket of type " << socktype);
    socket = create_socket(socktype);
    CORE_LOGINFO("Channel initialization done");
}

zmq::socket_t Channel::create_socket(int socktype)
{
    auto s = zmq::socket_t{zmq_context, socktype};
    s.set(zmq::sockopt::linger, 0);

    CORE_LOGINFO("Creating socket done");

    return s;
}

void Channel::close()
{
    socket.close();

    CORE_LOGINFO("Channel destroyed");
}

void Channel::send_string(const char* data, zmq::send_flags flags, int timeout_ms)
{
    if(data == nullptr)
    {
        throw std::runtime_error("E: Client can't send a nullptr!");
    }
    CORE_LOGINFO("Sending data " + std::string(data));

    // If sending is not received by the other side within 1 second, then throw an exception.
    // This is the case when the virtuoso server is not responding (maybe because it is busy, or because it died)
    socket.set(zmq::sockopt::sndtimeo, timeout_ms);

    const auto dataSize = strlen(data); // Assuming your char* is NULL-terminated
    zmq::message_t message(dataSize);
    std::memcpy ((void *) message.data(), data, dataSize);

    const auto res = socket.send(message, flags);

    if (!res)
    {
        throw ChannelTimeoutReceive("Socket can't send data to the other endpoint");
    }
    if (res.value() != dataSize)
    {
        throw std::runtime_error("Client can't send all data, only " +std::to_string(res.value()) + "are send. Maybe a timeout has been triggered?") ;
    }
    CORE_LOGINFO("Sending data done");
}

std::string Channel::recv_string(int timeout_ms, zmq::recv_flags flags)
{
    zmq::message_t message;

    socket.set(zmq::sockopt::rcvtimeo, timeout_ms); // https://stackoverflow.com/questions/7538988/zeromq-how-to-prevent-infinite-wait

    const auto result = socket.recv(message, flags); // blocking
    if (!result)
    {
        throw ChannelTimeoutReceive(
            std::string("Socket can't receive data of the other endpoint. Probably because of timeout. Error ID:") 
            + zmq_strerror(errno)
        );
    }
    CORE_LOGINFO("Has received a message..." + message.to_string());
    return message.to_string();
}

/**
 * Get Hostname of this machine by calling gethostname()
 */
std::string Channel::get_hostname() const
{
    char hostname[DFIIBRIDGE_HOST_NAME_MAX];
    int result = gethostname(hostname, DFIIBRIDGE_HOST_NAME_MAX);
    if (result!=0)
    {
        // In Docker containern gethostname will fail -> we need a fallback solution
        if(const char* hostname_env = std::getenv("HOSTNAME"))
            return hostname_env;

        throw std::runtime_error("Could not retrieve hostname!");
    }

    return hostname;
}

