#include <iostream>

#include "DfiiBridgeClient.hpp"


namespace fs = std::filesystem;

DfiiBridgeClient::DfiiBridgeClient()
: DfiiBridgeCore(), origin_session(false)
{
    CORE_LOGINFO("Initialize DfiiBridgeClient without a core session manager");
}

DfiiBridgeClient::DfiiBridgeClient(const std::string& root_path) : DfiiBridgeCore(CoreSessionManager{root_path})
{
    CORE_LOGINFO("Initialize DfiiBridgeClient with a root path: " << root_path);
}

DfiiBridgeClient::DfiiBridgeClient(const CoreSessionManager& csm) : DfiiBridgeCore(csm)
{
    CORE_LOGINFO("Initialize DfiiBridgeClient with a core session manager");
}

DfiiBridgeClient::~DfiiBridgeClient()
{
    CORE_LOGINFO("DfiiBridgeClient destroyed. All endpoint instances will be destroyed too!");
    clear_endpoints();
}

void DfiiBridgeClient::clear_endpoints()
{
    for(auto ch : client_channels)
        delete ch;

    client_channels.clear();
}

void DfiiBridgeClient::connect_to_endpoint(const nlohmann::json& session)
{
    connect_to_endpoint(Session(session));
}

void DfiiBridgeClient::connect_to_endpoint(const Session& session)
{
    logDebug("Connect to endpoint: " + session.hostname + " port " + std::to_string(session.port));
    ChannelClient* ch = new ChannelClient();
    try
    {
        ch->set_target_session(session);
        ch->connect();
    }
    catch(const std::exception& e)
    {
        delete ch;
        this->session_manager.delete_session_file(session);
        throw std::runtime_error(std::string("Cannot connect... giving up (")+e.what()+"). Deleting session file.");
    }
    logDebug("Connect to endpoint done");
    client_channels.push_back(ch);
}

void DfiiBridgeClient::connect_to_endpoints(const SessionVector& sessions)
{
    for(const auto& session : sessions)
    {
        connect_to_endpoint(session);
    }
}

void DfiiBridgeClient::set_origin_session(const Session& session)
{
    origin_session = session;
}

const Session& DfiiBridgeClient::get_origin_session() const
{
    return origin_session;
}

std::vector<Session> DfiiBridgeClient::get_connected_sessions() const
{
    std::vector<Session> session_list;
    for(const auto& t_channel : client_channels)
        session_list.push_back(t_channel->get_target_session());

    return session_list;
}


/**
 * Send a request to a virtuoso session
 */
ExecResultVector DfiiBridgeClient::execute(const std::string &function_name,
                                                const ExecArgumentVector &args,
                                                bool request_reply,
                                                int timeout)
{
    logDebug("Execute function \"" + function_name + "\"");

    if(client_channels.empty())
    {
        throw std::runtime_error("No endpoints attached.");
    }

    if (function_name.empty())
    {
       throw std::runtime_error("Function name can't be empty.");
    }

    ExecResultVector results;

    for(const auto& t_channel : client_channels)
    {
        nlohmann::json payload = {
            {"key", t_channel->get_target_key()}, // used for authentication and responding
            {"func", function_name},
            {"args", args},
            {"request_reply", request_reply}
        };

        if(origin_session.is_valid())
        {
            payload["origin_hostname"] = origin_session.hostname;
            payload["origin_port"] = origin_session.port;
        }

        logDebug("Sending payload:\n" + payload.dump(1));
        logDebug("Target: " + t_channel->get_target_hostname() + ":" + std::to_string(t_channel->get_target_port()));

        t_channel->send_string(payload.dump().c_str(), zmq::send_flags::none, timeout);

        logDebug("Sending payload done. Now start waiting for an answer from the server.");

        // append the response to the results.
        const auto answ = t_channel->recv_string(timeout);
        logDebug("Receiving:\n" + answ);
        results.push_back(answ);
    }
    logDebug("Execute function \"" + function_name + "\" done");

    return results;
}
