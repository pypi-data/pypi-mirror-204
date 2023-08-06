#pragma once

#define DFIIBRIDGE_VERSION "1.0.0"
#define KEY_LENGTH 20
#define DFIIBRIDGE_HOST_NAME_MAX 40

#include <set>
#include <string>
#include <map>
#include <vector>

class Session;
class LoggingCallback;


using ExecResultVector = std::vector<std::string>;
using ExecArgumentVector = std::vector<std::string>;
using UserDataMap = std::map<std::string, std::string>;

using LoggingCallback_t = LoggingCallback*;
using LoggingCallbackList = std::set<LoggingCallback_t>;
using SessionVector = std::vector<Session>;


#define CORE_LOGINFO(i) if(0){}
// Uncomment to have more detailed debug information
//#define CORE_LOGINFO(i) std::cout << "[INFO] CORE-> " << i << std::endl;
#define CORE_LOGERROR(i) std::cout << "[ERROR] CORE-> " << i << std::endl;
#define CORE_LOGWARNING(i) std::cout << "[WARNING] CORE-> " << i << std::endl;



#define EXIT_CALLBACK_NAME "dfiibridge_exit"
#define INFO_CALLBACK_NAME "dfiibridge_info"