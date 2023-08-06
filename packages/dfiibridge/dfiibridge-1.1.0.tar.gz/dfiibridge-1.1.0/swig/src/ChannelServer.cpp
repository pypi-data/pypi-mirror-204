#include <regex>
#include "ChannelServer.hpp"

ChannelServer::ChannelServer()
: Channel(ZMQ_REP)
{
    CORE_LOGINFO("Server channel created")
}

ChannelServer::~ChannelServer()
{
    close();
    CORE_LOGINFO("Server channel destroyed")
}

/**
 * Parse the port number from the bind adress. Bind adress is in
 * the format of tcp://0.0.0.0:00000
 */
int ChannelServer::parse_port_from_address(const std::string& address) const
{
    // parse the last 4 integer which is the port number.
    std::string s = address;
    std::regex rgx("(.*):(\\d+)");
    std::smatch matches;
    std::regex_search(s, matches, rgx);

    auto m = matches.end() - 1;
    return std::stoi(*m);
}

void ChannelServer::bind(const std::string& bind_address)
{
    CORE_LOGINFO("Bind to address: " << bind_address);
    socket.bind(bind_address);
    this->bind_address = bind_address;
    CORE_LOGINFO("Binding successfull");
}

void ChannelServer::bind_free_port()
{
    std::string conn_str = "tcp://*:*";

    std::string address_buf(1024, ' '); // make this sufficiently large,
                                        // otherwise an error will be thrown because of invalid argument.
    CORE_LOGINFO("Bind to address: " << conn_str);
    socket.bind(conn_str);

    auto size = socket.get(zmq::sockopt::last_endpoint, zmq::buffer(address_buf));
    address_buf.resize(size);
    CORE_LOGINFO("Binding successfull");

    bind_address = address_buf;
}

int ChannelServer::get_port() const
{
    return parse_port_from_address(bind_address);
}