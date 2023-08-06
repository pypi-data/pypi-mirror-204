#pragma once

#include <string>

#include <nlohmann/json.hpp>

#include "globals.hpp"

/**
 * @brief The virtuoso session class
 * @details A session contains the required attributes hostname, port, a session key and the protocol version.
 *         A list of user defined key value pairs can be used for the optional attributes.
 */
class Session
{
public:
    /**
     * @brief The virtuoso port number
     */
    int port;

    /**
     * @brief The virtuoso server name or IP address
     */
    std::string hostname;

    /**
     * @brief The session key
     *
     */
    std::string key;

    /**
     * @brief The DfiiBridge protocol version
     */
    std::string version;

    /**
     * @brief The <key,value> map for optional user data.
     * @brief key and value must be of type std::string
     */
    UserDataMap userdata;

    /**
     * @brief Indicator whether the current sessionb is valid
     */
    bool valid;

    /**
     * @brief Construct a new Session object
     */
    Session();
    Session(bool invalid);

    /**
     * @brief Instantiate a new session instance from the passed JSON string.
     * @details  The JSON properties are handled in the same way as in the method \ref from_string.
     *
     * @throws std::runtime_error as soon as a required value is missing.
     *         These are "hostname", "port", "key" and "version"
     * @param json  The JSON string with the usesd parameters.
     */
    Session(const nlohmann::json& json);

    /**
     * @brief Instantiate a new session instance from the passed values.
     *
     * @throws std::runtime_error as soon as a required value is missing
     * @param hostname The session host name or IP address
     * @param port The session port number
     * @param key  The session key
     * @param version The optional DfiiBridge protocol version
     * @param userdata The optional user data
     */
    Session(const std::string& hostname,
            int port,
            const std::string& key,
            const std::string& version=DFIIBRIDGE_VERSION,
            UserDataMap userdata={});

    /**
     * @brief Is the current session valid or not?
     */
    bool is_valid() const {return valid;};

    /**
     * @brief The equal to operator
     * @details Except for the user data and the valid flag, all class members are used for the comparison.
     * @param rhs The other session
     */
    bool operator==(const Session& rhs) const;

    /**
     * @brief The not equal to operator
     * @details Except for the user data and the valid flag, all class members are used for the comparison.
     * @param rhs The other session
     */
    bool operator!=(const Session& rhs) const;

    /**
     * @brief Create a new session instance from the passed JSON string.
     * @details The method tries to get the values for the required properties like hostname, port and key
     *          from the JSON string and creates a new session instance.
     *
     * @throws std::runtime_error as soon as a required property is missing
     * @param json  The JSON string with the usesd parameters.
     * @return Session
     */
    static Session from_string(const std::string& json);

    /**
     * @brief Get the json object
     *
     * @return nlohmann::json
     */
    nlohmann::json get_json() const;

    /**
     * @brief Set the optional user data
     *
     * @param userdata <key,value> pairs of the user data
     */
    void set_userdata(const UserDataMap& userdata);

    /**
     * @brief Set the optional user data from the passed JSON instance
     *
     * @param userdata
     */
    void set_userdata(const nlohmann::json& userdata);
};
