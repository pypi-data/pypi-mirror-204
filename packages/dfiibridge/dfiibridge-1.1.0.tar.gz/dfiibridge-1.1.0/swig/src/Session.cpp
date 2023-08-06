#include "Session.hpp"

Session::Session()
: port(-1), hostname(), key(), version(DFIIBRIDGE_VERSION), userdata({}), valid(false) // not valid since port is not set
{}

Session::Session(bool invalid): valid(false) {};

Session::Session(const std::string& hostname,
                int port,
                const std::string& key,
                const std::string& version,
                UserDataMap userdata)
: port(port),hostname(hostname), key(key), version(version), userdata(userdata), valid(true)
{}

Session::Session(const nlohmann::json& json) : valid(true)
{
    if(json.contains("hostname"))
        hostname = json["hostname"];
    else
        throw std::runtime_error("Hostname is not given.");
    if(json.contains("key"))
        key = json["key"];
    else
        throw std::runtime_error("Key is not given.");
    if(json.contains("userdata"))
        userdata = json["userdata"];
    else
        throw std::runtime_error("userdata is not given.");
    if(json.contains("port"))
        port = json["port"];
    else
        throw std::runtime_error("port is not given.");
    if(json.contains("version"))
        version = json["version"];
    else
        throw std::runtime_error("version is not given.");
}

bool Session::operator==(const Session& rhs) const
{
    return rhs.hostname == hostname &&
        rhs.port == port &&
        rhs.key == key &&
        rhs.version == version;
}

bool Session::operator!=(const Session& rhs) const
{
    return !(*this == rhs);
}



Session Session::from_string(const std::string& json)
{
    nlohmann::json j = nlohmann::json::parse(json.c_str());

    std::string version = DFIIBRIDGE_VERSION;
    if(j.contains("version"))
        version = j["version"];

    if(!j.contains("hostname"))
        throw std::runtime_error("Hostname is not defined in json string.");

    if(!j.contains("port"))
        throw std::runtime_error("Port is not defined in json string.");

    if(!j.contains("key"))
        throw std::runtime_error("Key is not defined in json string.");

    Session new_session{j["hostname"], j["port"], j["key"], version};

    if(j.contains("userdata"))
        new_session.set_userdata(j["userdata"]);

    return new_session;
}

nlohmann::json Session::get_json() const
{
    return {
        {"version", version},
        {"port", port},
        {"hostname", hostname},
        {"key", key},
        {"userdata", userdata}
    };
}

void Session::set_userdata(const UserDataMap& userdata)
{
    this->userdata = userdata;
}

void Session::set_userdata(const nlohmann::json& userdata)
{
    set_userdata(userdata.get<UserDataMap>());
}