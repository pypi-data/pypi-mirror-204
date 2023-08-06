// DfiiBridge.i
%module(directors="1") dfiibridge_core
%{
#include "LoggingCallback.hpp"
#include "DfiiBridgeClient.hpp"
#include "DfiiBridgeServer.hpp"
#include "CoreSessionManager.hpp"
#include "globals.hpp"
#include "ChannelClient.hpp"
#include "Channel.hpp"
#include "ChannelServer.hpp"
#include "ChannelClient.hpp"
#include <nlohmann/json.hpp>
%}

%include <std_string.i>
%include <std_vector.i>
%include <std_pair.i>
%include <std_map.i>
%include <exception.i>

%exception {
  try {
    $action
  }catch(const std::invalid_argument& e){
    SWIG_exception(SWIG_TypeError, (std::string("$name: ")+e.what()).c_str());
  } catch(const std::exception& e) {
    SWIG_exception(SWIG_RuntimeError, (std::string("$name: ")+e.what()).c_str());
  } catch(...) {
    SWIG_exception(SWIG_UnknownError, "Unknown exception when $name was called");
  }
}

%template(Svector) std::vector<std::string>;
%template(SSmap) std::map<std::string, std::string>;
%template(SSpair) std::pair<std::string, std::string>;
%template(SessionVector) std::vector<Session>;
%template(Ivector) std::vector<int>;

%feature("director", assumeoverride=1) RemoteCallback;
%feature("director", assumeoverride=1) LoggingCallback;
%feature("docstring");

%include "LoggingCallback.hpp"
%include "RemoteCallback.hpp"
%include "DfiiBridgeCore.hpp"
%include "DfiiBridgeServer.hpp"
%include "DfiiBridgeClient.hpp"
%include "Session.hpp"
%include "CoreSessionManager.hpp"
%include "globals.hpp"
%include "Channel.hpp"
%include "ChannelServer.hpp"
%include "ChannelClient.hpp"