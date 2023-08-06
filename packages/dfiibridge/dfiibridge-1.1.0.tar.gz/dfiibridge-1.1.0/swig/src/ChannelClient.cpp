#include <iostream>
#include <unistd.h>

#include "ChannelClient.hpp"


/////// Client related methods ///////
ChannelClient::ChannelClient()
: Channel(ZMQ_REQ), connected(false)
{
    CORE_LOGINFO("Setting relaxed zmq socket option for client channel");
    socket.set(zmq::sockopt::req_relaxed, true);  // https://stackoverflow.com/questions/26915347/zeromq-reset-req-rep-socket-state
    CORE_LOGINFO("Setting correlated zmq socket option for client channel");
    socket.set(zmq::sockopt::req_correlate, true); // http://api.zeromq.org/master:zmq-setsockopt
}

ChannelClient::ChannelClient(const Session& session)
: ChannelClient()
{
    target_session = session;
}

ChannelClient::ChannelClient(const nlohmann::json& json)
: ChannelClient()
{
    target_session = Session(json);
}

ChannelClient::~ChannelClient()
{
    close();
}

void ChannelClient::connect()
{
    if(!target_session.is_valid())
        throw std::runtime_error("No valid target_session given");

    std::string conn_str = "tcp://" + target_session.hostname + ":" + std::to_string(target_session.port);
    connect(conn_str);
}

void ChannelClient::connect(const std::string& conn_str, const int maxConnectionsAttempts)
{
    if(!connected){
        // create listening socket for monitoring
        zmq::monitor_t monitor;
        monitor.init(socket, "inproc://monitor", ZMQ_EVENT_CONNECTED);

        int connectionAttempt = 0;
        // Attempt to connect.
        while(!connected){
            try{
                CORE_LOGINFO("Connecting to: " << conn_str);    // Notify user of attempt to connect
                connectionAttempt++;                               // increment attempt count
                socket.connect(conn_str);                          // Connect to the ip address

                if(monitor.check_event(1000))
                {                                                  // Wait at most 1000 msec for the connection
                    connected = true;                              // Set the connection bool
                    CORE_LOGINFO("Connecting to: " << conn_str + " is successful");
                    endpoint = conn_str;
                    break;                                         // continue past the while loop
                }
            }
            catch(zmq::error_t &err)
            {                                // Catch any error
                CORE_LOGERROR(err.what()) // Output error
            }
            CORE_LOGINFO("Connecting to: " << conn_str << " not successful, trying again...");

            // The default value are 3 attempts
            // The client waits at most 3*1000 msec per default until he throws an exception that
            // the connection failed.
            if(connectionAttempt == maxConnectionsAttempts)
            {
                CORE_LOGINFO("Max Connection Attempts Exceded. No session found.");
                throw std::runtime_error("Failed to connect to the given connection string: " + conn_str);
            }
        }
    }
}

void ChannelClient::reconnect()
{
    close();
    connect(endpoint);
}

void ChannelClient::send_string(const char* data, zmq::send_flags flags, int timeout_ms)
{
    if(!connected)
        throw std::runtime_error("E: Client should be connected first!");

    Channel::send_string(data, flags, timeout_ms);
}

std::string ChannelClient::recv_string(int timeout, zmq::recv_flags flags)
{
    if(!connected)
        throw std::runtime_error("E: Client should be connected first!");
    return Channel::recv_string(timeout, flags);
}

const Session& ChannelClient::get_target_session() const
{
    return target_session;
}

void ChannelClient::set_target_session(Session session)
{
    target_session = session;
}

std::string ChannelClient::get_target_hostname() const
{
    return target_session.hostname;
}

int ChannelClient::get_target_port() const
{
    return target_session.port;
}

std::string ChannelClient::get_target_key() const
{
    return target_session.key;
}
