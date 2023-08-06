#pragma once

#include <string>

#include "globals.hpp"
#include "Session.hpp"


/**
 * @brief The core session manager manages the virtuoso sessions.
 */
class CoreSessionManager
{
private:
    /**
     * @brief the name of the root directory
     *
     */
    std::string ROOT;

public:

    /**
     * @brief Construct a new Core Session Manager object
     * @details The root directory is the to the default value $HOME/.dfiiBridge.
     * @throws std::runtime_error if value of $HOME is empty.
     */
    CoreSessionManager();

    /**
     * @brief Construct a new Core Session Manager object
     * @details The root directory is set the passed value.
     *          If the directory will be created if it does not exist.
     * @throws std::runtime_error if \ref root_path is empty.
     *
     * @param root_path name of the used root directory
     */
    CoreSessionManager(const std::string& root_path);

    /**
     * @brief Get the the default DfiiBridge root directory name.
     *        This value is $HOME/.dfiiBridge.
     * @throws std::runtime_error if value of $HOME is empty.
     */
    static std::string default_root_directory();

    /**
     * @brief Set the root directory if the path value isn't empty.
     *        The path will be created, if it doesn't exists.
     *
     * @throws std::runtime_error if the path value is empty.
     *
     * @param path relative of absolute path name
     */

    void set_root_directory(const std::string& path);

    /**
     * @brief Get the root directory name
     */
    std::string get_root_directory() const;

    /**
     * @brief Kill the session via the 'dfiibridge_exit' remote function callback
     */
    std::string kill_session(const Session& session);

    /**
     * @brief Get information about the session via the 'dfiibridge_info' remote function callback
     */
    std::string get_info(const Session& session);

    /**
     * @brief    Save the passed session in the session file.
     * @details  The session is created in the current root directory.
     *           The file name is derived from the hostname and the port in the session.
     *
     * @param session the session
     */
    void write_as_json(const Session& session);

    /**
     * @brief   Get the path name of the session's log file.
     * @details The file name is derived from the hostname and the port in the session.
     *          If the flag check is true, the the existence of the session file is checked.
     *
     * @throws std::runtime_error if the session log does not exist.
     * @param session the session instance
     * @param check verify the existence of the log file
     * @return std::string the absolute file name
     */
    std::string get_log_file_path(const Session& session, bool check=false) const;

    /**
     * @brief Get the path name of the session's log file.
     * @details The file name is derived from the hostname and the port.
     *          If the flag check is true, the the existence of the session file is checked.
     *
     * @throws std::runtime_error if the session log does not exist.
     * @param hostname hostname of the session
     * @param port used port number
     * @param check verify the existence of the log file
     * @return std::string the absolute file name
     */
    std::string get_log_file_path(const std::string& hostname, int port, bool check=false) const;

    /**
     * @brief   Get the path name of the session file.
     * @details The file name is derived from the hostname and the port in the session.
     *          If the flag check is true, the the existence of the log file is checked.
     *          The creation of the log file is the responsibility of the user!
     *          The core will never create this file on its own. It just provides a common name.
     *
     * @throws std::runtime_error if the session file does not exist.
     * @param session the session instance
     * @param check verify the existence of the session file
     * @return std::string the absolute file name
     */
    std::string get_session_file_path(const Session& session, bool check=false) const;

    /**
     * @brief Get the path name of the session file.
     * @details The file name is derived from the hostname and the port.
     *          If the flag check is true, the the existence of the log file is checked.
     *          The creation of the log file is the responsibility of the user!
     *          The core will never create this file on its own. It just provides a common name.
     *
     * @throws std::runtime_error if the session file does not exist.
     * @param hostname hostname of the session
     * @param port used port number
     * @param check verify the existence of the session file
     * @return std::string the absolute file name
     */
    std::string get_session_file_path(const std::string& hostname, int port, bool check=false) const;

    /**
     * @brief Provide a vector of all available sessions.
     * @details The method iterates over the files in the root directory and returns a vector
     *          of sessions whose main Versioninfo value matches the current main version number.
     *          If connection_check is true, only those sessions are taken into account whose host can be connected to,
     *
     * @param connection_check Verify the connection to each session host
     * @return SessionVector The session vector
     */
    SessionVector find_sessions(bool connection_check=false) noexcept;

    /**
     * @brief Provide a vector of sessions whose userdata match the search criteria
     * @details The method only considers those sessions whose major version matches the current version number.
     *          In addition, all entries of the search criteria must be present in the userdata map.
     *          If connection_check is true, only those sessions are taken into account whose host can be connected to,
     *
     * @param search_criteria key,value pairs
     * @param connection_check Verify the connection to each session host
     * @return SessionVector The session vector
     */
    SessionVector find_sessions(const UserDataMap& search_criteria, bool connection_check=false) noexcept;

    /**
     * @brief Get the session to the specified session file.
     * @details The method tries to read the specified file, verifies that the file contains the required
     *          properties  like hostname, port, version.
     *          If connection_check is true, it is checked whether the specified session host can be reached
     *          under the specified port.
     *
     * @throws std::runtime_error if the session file does not exist or the the property verfication fails
     * @param path The session file name
     * @param connection_check Verify the connection to the session host
     * @return Session
     */
    Session get_session(const std::string& path, bool connection_check=false);

    /**
     * @brief Get the session to the specified hostname and port.
     * @details The method tries to read the associated session file, verifies that this file contains the
     *          required properties  like hostname, port, version.
     *          If connection_check is true, it is checked whether the specified session host can be reached
     *          under the specified port.
     *
     * @param hostname The session host
     * @param port The session port number
     * @param connection_check Verify the connection to the session host
     * @return Session
     */
    Session get_session(const std::string& hostname, int port, bool connection_check=false);

    /**
     * @brief   Check if a corresponding session file exists in the root directory.
     * @details The session hostname and the port number are used for the the check.
     *
     * @param session The session to check
     * @return true if an corresponding session exists, false otherwise
     */
    bool contains(const Session& session) noexcept;

    /**
     * @brief  Check if a corresponding session file exists in the root directory.
     *
     * @param hostname The hostname of the session to check
     * @param port The port number of the session to check
     * @return true if an corresponding session exists, false otherwise
     */
    bool contains(const std::string& hostname, int port) noexcept;

    /**
     * @brief Try to connect the host of the session.
     * @details The session host must be accessible under the session port.
     *          If not, the associated session file is also deleted.
     *
     * @param session
     * @return true if the session host and the session port are accessible
     * @return false if the session host and session port are not accessible
     */
    bool ping_session(const Session& session) noexcept;

    /**
     * @brief Try to connect the host under the port.
     * @details The session host must be accessible under the session port.
     *          If not, the associated session file is also deleted.
     *
     * @param hostname
     * @param port
     * @return true if the session host and the session port are accessible
     * @return false if the session host and session port are not accessible
     */
    bool ping_session(const std::string& hostname, int port) noexcept;

    /**
     * @brief Deletes the session file belonging to the session.
     *
     * @param session The session
     * @return true if the session file was successfully deleted
     * @return false in case of any error
     */
    bool delete_session_file(const Session& session);

    /**
     * @brief Deletes the session file belonging to the hostname and port.
     *
     * @param hostname  The session host
     * @param port  The session port
     * @return true if the session file was successfully deleted
     * @return false in case of any error
     */
    bool delete_session_file(const std::string& hostname, int port);

    /**
     * @brief Deletes all session files that belong to the transfered sessions.
     *
     * @param sessions The session list
     * @return true if the session file was successfully deleted
     * @return false in case of any error
     */
    bool delete_session_files(const SessionVector& sessions);
};
