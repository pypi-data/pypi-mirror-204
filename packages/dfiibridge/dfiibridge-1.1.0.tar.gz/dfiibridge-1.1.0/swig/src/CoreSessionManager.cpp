#include <filesystem>
#include <fstream>
#include <iostream>

#include "DfiiBridgeClient.hpp"
#include "CoreSessionManager.hpp"
#include "ChannelClient.hpp"
#include "globals.hpp"

namespace fs = std::filesystem;

// Session Manager related methods
CoreSessionManager::CoreSessionManager()
{
    CORE_LOGINFO("Initialize core session manager without root path: default_root_directory() = " << default_root_directory());
    set_root_directory(default_root_directory());
}

CoreSessionManager::CoreSessionManager(const std::string& root_path)
{
    CORE_LOGINFO("Initialize core session manager with root path: " << root_path);
    set_root_directory(root_path);
}

std::string CoreSessionManager::default_root_directory()
{
    auto user_home = std::getenv("HOME");
    if(!user_home)
    {
        throw std::runtime_error("$HOME is not defined!");
    }
    return (std::string)user_home + "/.dfiiBridge";
}

void CoreSessionManager::set_root_directory(const std::string& path)
{
    if(path.empty())
    {
        throw std::runtime_error("E: An empty name for root directory is not allowed!");
    }

    // Create the session directory if it is not there
    if(!fs::exists(path))
    {
        CORE_LOGINFO("Trying to create root_directory because it does not exist: " << path);
        std::error_code err;
        if(!fs::create_directories(path, err))
        {
            throw std::runtime_error(err.message());
        }
    }

    ROOT = path;
}

std::string CoreSessionManager::get_root_directory() const
{
    return ROOT;
}

void CoreSessionManager::write_as_json(const Session& session)
{
    nlohmann::json json_string = session.get_json();

    auto path = get_session_file_path(json_string);

    CORE_LOGINFO("Writing dfiibridge session file to " << path);
    std::ofstream out(path);
    out.exceptions(~std::ofstream::goodbit);
    out << json_string << std::endl << std::flush;
    out.flush();
    out.close();
}

std::string CoreSessionManager::get_session_file_path(const Session& session, bool check) const
{
    return get_session_file_path(session.hostname, session.port, check);
}

std::string CoreSessionManager::get_session_file_path(const std::string& hostname, int port, bool check) const
{
    std::string filename = hostname + "_" + std::to_string(port) + ".json";
    auto path = (fs::path)ROOT / (fs::path)filename;

    if(check && !fs::exists(path))
        throw std::runtime_error(path.string() + " does not exists!");

    return path;
}


std::string CoreSessionManager::get_log_file_path(const Session& session, bool check) const
{
    return get_log_file_path(session.hostname, session.port, check);
}

std::string CoreSessionManager::get_log_file_path(const std::string& hostname, int port, bool check) const
{
    std::string filename = hostname + "_" + std::to_string(port) + ".log";
    auto path = (fs::path)ROOT / (fs::path)filename;

    if(check && !fs::exists(path))
        throw std::runtime_error(path.string() + " does not exists!");

    return path;
}


Session CoreSessionManager::get_session(const std::string& path, bool connection_check)
{
    if(!fs::exists(path))
        throw std::runtime_error(std::string("Path (")+path+") to the session does not exist!");

    CORE_LOGINFO("Reading: " << path);

    nlohmann::json session;
    std::ifstream in(path);
    in >> session;

    if(!session.contains("hostname"))
    {
        throw std::runtime_error("Hostname is not defined in "+path);
    }
    if(!session.contains("port"))
    {
        throw std::runtime_error("Port is not defined in "+path);
    }
    if(!session.contains("version"))
    {
        throw std::runtime_error("Version is not defined in "+path);
    }
    if(!session.contains("key"))
    {
        throw std::runtime_error("Key is not defined in "+path);
    }

    if(connection_check && !ping_session(session["hostname"], session["port"]))
    {
        throw std::runtime_error("The session (" + std::string(session["hostname"]) + ", " + session["port"].dump() + ") is dead. Ping was unsuccessful.");
    }

    std::string version = session["version"];
    if(version[0] == DFIIBRIDGE_VERSION[0])
    {
        try
        {
            return Session(session);
        }
        catch(const nlohmann::detail::type_error& e)
        {
            throw std::runtime_error("The session (" + std::string(session["hostname"]) + ", " + session["port"].dump() + ") is not compatible: "+e.what());
        }
    }
    else
    {
        throw std::runtime_error("Version of the session: " + version + " did not match with DFIIBRIDGE version: " + DFIIBRIDGE_VERSION);
    }
    // session could not be found.
    throw std::runtime_error("There is no such a session (" + std::string(session["hostname"]) + ", " + session["port"].dump() + ")");
}

Session CoreSessionManager::get_session(const std::string& hostname, int port, bool connection_check)
{
    const std::string path = get_session_file_path(hostname, port);
    return get_session(path, connection_check);
}

SessionVector CoreSessionManager::find_sessions(bool check_connection) noexcept
{
    SessionVector sessions;
    nlohmann::json current_session;

    for (const auto& entry : fs::directory_iterator(CoreSessionManager::ROOT))
    {
        if(entry.path().extension() != ".json")
            continue;

        try
        {

            //CORE_LOGINFO("Reading: " << entry.path());
            std::ifstream in(entry.path());
            in >> current_session;

            auto s = Session(current_session);  // Exception can be thrown if session is incompatible
            //CORE_LOGINFO("checking version: " << s.version);
            if(s.version[0] != DFIIBRIDGE_VERSION[0])
                continue;

            //CORE_LOGINFO("pinging session " << s.hostname);
            if(check_connection && !ping_session(s))
                continue;

            //CORE_LOGINFO("is okay");
            sessions.push_back(s);

        }
        catch(const std::exception &e){
            CORE_LOGINFO("Session file " << entry << " could not been read. Trying to delete"
                << "the session file. Exception was: " << e.what());
            fs::remove(entry);
            continue;
        }
   }
    return sessions;
}

SessionVector CoreSessionManager::find_sessions(const UserDataMap& search_criteria,
                                                  bool check_connection) noexcept
{
    //CORE_LOGINFO("Going through all available sessions...");
    auto sessions = find_sessions(check_connection);

    //CORE_LOGINFO("Apply filter...");

    SessionVector result;

    for(auto& s : sessions)
    {
        bool matching = true;
        for (const auto& [key, value] : search_criteria)
        {
            if(s.userdata.find(key) == s.userdata.end())
            {
                // If the key is not present, then this is NOT a match!
                matching = false;
                break;
            }
            // the key is present
            if(s.userdata[key] != value)
            {
                // If the value is incorrect, then this is NOT a match!
                matching = false;
                break;
            }
        }
        if(matching)
            result.push_back(s);
    }
    return result;
}

bool CoreSessionManager::contains(const Session& session) noexcept
{
    return contains(session.hostname, session.port);
}

bool CoreSessionManager::contains(const std::string& hostname, int port) noexcept
{
    for(const auto& s : find_sessions())
    {
        if(s.hostname == hostname && s.port == port)
                return true;
    }
    return false;
}

bool CoreSessionManager::ping_session(const std::string& hostname, int port) noexcept
{
    Session s;
    try{
        s = get_session(hostname, port);
    }
    catch(...){
        return false;
    }
    return ping_session(s);
}

bool CoreSessionManager::ping_session(const Session& session) noexcept
{
    //CORE_LOGINFO("Trying to ping the session: (" << s.hostname << ", " << s.port << ")");
    try{
        ChannelClient channel{session};
        channel.connect();
    }
    catch(const std::exception &e){
        CORE_LOGWARNING("Server is not responding. Removing dead session file. Exception:\n" << e.what());
        delete_session_file(session);
        return false;
    }
    return true;
}

bool CoreSessionManager::delete_session_file(const Session& session)
{
    return delete_session_file(session.hostname, session.port);
}

bool CoreSessionManager::delete_session_file(const std::string& hostname, int port)
{
    // Invalid sessions do not need to be deleted
    if(hostname.empty() || port==-1)
        return true;

    CORE_LOGINFO("Try to delete the session file of " << hostname << ":" << port);

    std::error_code errorCode;
    std::string path;
    try{
        path = get_session_file_path(hostname, port);
    }catch(const std::exception &e){
        CORE_LOGERROR("Session file " << path << " can't be deleted! Exception " << e.what());
        return false;
    }

    CORE_LOGINFO("Found session file here: " << path);

    const auto ret = fs::remove(path.c_str(), errorCode);
    if (errorCode.value() != 0)
    {
        CORE_LOGERROR("Session file " << path << " can't be deleted! Error " << errorCode.message());
    }
    return ret && (errorCode.value() == 0);
}

bool CoreSessionManager::delete_session_files(const SessionVector& sessions)
{
    bool allFilesRemoved = true;
    for (const auto& s : sessions)
    {
        if(!delete_session_file(s.hostname, s.port))
        {
            allFilesRemoved = false;
        }
    }
    return allFilesRemoved;
}

std::string CoreSessionManager::kill_session(const Session& session)
{
    DfiiBridgeClient client;
    client.connect_to_endpoint(session);
    return client.execute(EXIT_CALLBACK_NAME, {}, true, 1000)[0];
}

std::string CoreSessionManager::get_info(const Session& session)
{
    DfiiBridgeClient client;
    client.connect_to_endpoint(session);
    return client.execute(INFO_CALLBACK_NAME, {}, true, 1000)[0];
}
