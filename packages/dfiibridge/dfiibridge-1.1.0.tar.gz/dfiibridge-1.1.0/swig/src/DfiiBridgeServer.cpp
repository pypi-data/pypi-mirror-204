#include <iostream>
#include <thread>
#include <zmq.hpp>
#include <sys/types.h>
#include <unistd.h>

#include "globals.hpp"
#include "ChannelServer.hpp"
#include "DfiiBridgeClient.hpp"
#include "DfiiBridgeServer.hpp"


std::string InfoRemoteCallback::callback(DfiiBridgeClient* ws, ExecArgumentVector args)
{
    pid_t pid = getpid();
    return std::string("\"DfiiBridge Server running on pid ")+std::to_string(pid)+"\"";
}

ExitRemoteCallback::ExitRemoteCallback(DfiiBridgeServer* server) : server(server){};

std::string ExitRemoteCallback::callback(DfiiBridgeClient* ws, ExecArgumentVector args)
{
    server->stop();
    return "\"\""; // Empty string means success here -> can be evaluated in all languages
}


DfiiBridgeServer::DfiiBridgeServer()
: DfiiBridgeServer(CoreSessionManager{}, UserDataMap{})
{
    CORE_LOGINFO("Created Server instance general core session manager and empty user datamap");
}

DfiiBridgeServer::DfiiBridgeServer(const UserDataMap& userdata)
: DfiiBridgeServer(CoreSessionManager{}, userdata)
{
    CORE_LOGINFO("Created Server instance general core session manager but with userdata");
}

DfiiBridgeServer::DfiiBridgeServer(const CoreSessionManager& csm, const UserDataMap& userdata):
    DfiiBridgeCore(csm),
    channel(),
    thread(nullptr),
    host_session(),
    known_functions(),
    listening(false),
    exit_callback(this),
    info_callback()
{
    CORE_LOGINFO("Trying to bind to free port");
    bind_free_port();
    CORE_LOGINFO("Setting userdata");
    host_session.set_userdata(userdata);

    // Register two default callback functions
    register_function(EXIT_CALLBACK_NAME, &exit_callback); // exit the server
    register_function(INFO_CALLBACK_NAME, &info_callback); // print pid of server
}

DfiiBridgeServer::~DfiiBridgeServer()
{
    logDebug("Destruction of server started");
    stop();

    // destroy the json file
    if(!session_manager.delete_session_file(host_session))
        logDebug("Session file coult not be deleted.");

    logDebug("Server instance destroyed");
}

std::string DfiiBridgeServer::get_session_file_path() const
{
    return session_manager.get_session_file_path(channel.get_hostname(), channel.get_port(), false);
}

void DfiiBridgeServer::stop()
{
    if(!listening)
        return; // It is not running -> nothing to be done

    listening = false; // stop the server
    if(thread != nullptr)
    {
        thread->join();
        delete thread;
        thread = nullptr;
    }
}

void DfiiBridgeServer::set_userdata(const UserDataMap& userdata)
{
    host_session.set_userdata(userdata);
}

const Session& DfiiBridgeServer::get_session() const
{
    return host_session;
}


void DfiiBridgeServer::bind_free_port()
{
    channel.bind_free_port();
}

bool DfiiBridgeServer::is_listening() const
{
    return listening;
}

/**
 * Start a server and listen from requests from Virtuoso or other programs
 */
void DfiiBridgeServer::listen()
{
    if(listening)
    {
        throw std::runtime_error("Server is already running!");
    }
    listening = true;

    logDebug("Setting the host session configuration for server..");

    host_session.hostname = channel.get_hostname();
    host_session.port = channel.get_port();
    host_session.key = gen_random_key(KEY_LENGTH);
    host_session.valid = true;
    session_manager.write_as_json(host_session);

    while(listening)
    {
        // read the received message from host socket.
        //logDebug(std::string("Listening for a new request (")+host_session.hostname+":"+std::to_string(host_session.port)+")...");
        std::string msg = "";
        try
        {
            msg = channel.recv_string(1000);
        }catch(const ChannelTimeoutReceive& e)
        {
            continue; // just try again in case of a timeout
        }
        catch(const std::exception& e)
        {
            logError(e.what());
            break;
        }

        if(msg.empty())
        {
            logDebug("Received nothing (empty string)... try again...");
            channel.send_string("failure Received an empty string", zmq::send_flags::dontwait);
            continue;
        }

        logDebug("Handling the request: " + msg);
        // parse the payload
        const auto payload = nlohmann::json::parse(msg);

        // process the message and return back to result from the called function
        std::string answ = "";

        // If no reply requested, send empty answ. directly!
        if(!payload["request_reply"])
        {
            logDebug("Sending the response to the client: " + answ);
            channel.send_string(answ.c_str(), zmq::send_flags::dontwait);
        }

        try
        {
            answ = handle_one_request(payload);
        }
        catch (std::exception &exp)
        {
            logError("handle_one_request failed");
            logError(exp.what());
            channel.send_string((std::string("failure ")+exp.what()).c_str(), zmq::send_flags::dontwait);
            continue;
        }
        catch(...)
        {
            logError("handle_one_request failed with unknown expection!");
            channel.send_string("failure handle_one_request failed with unknown expection", zmq::send_flags::dontwait);
            continue;
        }

        logDebug("Callback executed");

        // send the result back if requested
        if(payload["request_reply"])
        {
            logDebug("Sending the response to the client: " + answ);
            channel.send_string(answ.c_str(), zmq::send_flags::dontwait);
        }
    }

    listening = false;
    logDebug("Listening stopped");
}

/**
 * Start a server asynchronously
 */
void DfiiBridgeServer::listen_async()
{
    stop();
    logDebug("Starting async server");
    thread = new std::thread(&DfiiBridgeServer::listen, this);
}

std::string DfiiBridgeServer::gen_random_key(int len) const
{
    std::string s;
    static const char alphanum[] =
        "0123456789#+-_.,/()[]!?^<>|~*%$&"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz";

    for (int i = 0; i < len; ++i) {
        s += alphanum[rand() % (sizeof(alphanum) - 1)];
    }
    return s;
}

std::string DfiiBridgeServer::handle_one_request(const nlohmann::json& payload)
{
    logInfo("Received:\n" + payload.dump(1));

    std::string function_name;

    if(payload.contains("func"))
        function_name = payload["func"];
    else
        throw std::runtime_error("Function name is not given.");

    if(!payload.contains("key"))
    {
        throw std::runtime_error("Key is not given.");
    }

    if(payload["key"] != host_session.key)
    {
        throw std::runtime_error("Key in the payload is wrong! Expected is the host session key: \"" + host_session.key +"\"");
    }

    if(!payload.contains("args"))
    {
        throw std::runtime_error("The keyword 'args' in the payload is missing!");
    }

    logInfo("Trying to call \"" + function_name + "\" callback...");
    if(known_functions.find(function_name) == known_functions.end())
    {
        throw std::runtime_error("Requested function \"" + function_name + "\" is not defined/registered!");
    }

    // There is no origin hostname -> no reverse communication
    if(payload.find("origin_hostname") == payload.end() || payload.find("origin_port") == payload.end())
    {
        logInfo("Function \"" + function_name + "\" is now called without origin session:" + payload["args"].dump());
        return known_functions[function_name]->callback(nullptr, payload["args"]);
    }

    logInfo("Function \"" + function_name + "\" is now called with origin session:" + payload["args"].dump());

    // initialize reverse communication
    DfiiBridgeClient client;

    // Copy loggers of server to client
    for (const auto& cb : loggerCallbacks)
    {
        client.register_logging_function(cb);
    }

    auto target_session = session_manager.get_session(payload["origin_hostname"], payload["origin_port"], false);
    client.connect_to_endpoint(target_session); // Add the sender as endpoint
    client.set_origin_session(host_session); // Host session as origin

    return known_functions[function_name]->callback(&client, payload["args"]);
}

/**
 * Register a function that can be called from skill
 **/
void DfiiBridgeServer::register_function(const std::string& name, RemoteCallback* func)
{
    if(func == nullptr)
    {
        throw std::runtime_error("Can't register a nullptr as a callback!");
    }

    if (name.empty())
    {
        throw std::runtime_error("A non empty register name is needed!");
    }

    if(known_functions.find(name) != known_functions.end())
    {
        throw std::runtime_error("The used name is already registered yet!");
    }
    known_functions[name] = func;

}

std::string DfiiBridgeServer::get_hostname() const
{
    return channel.get_hostname();
}

int DfiiBridgeServer::get_port() const
{
    return channel.get_port();
}
