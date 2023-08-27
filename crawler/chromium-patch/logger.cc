#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>
#include <iostream>
#include <fstream>
#include <ctime>
#include <sstream>

std::string instrumentation_get_times(){
        std::time_t result = std::time(nullptr);
        std::stringstream ss;
        ss << result;
        return ss.str();
  }

std::string get_path(std::string output){
  const char *homedir;
  if ((homedir = getenv("HOME")) == NULL) {
    homedir = getpwuid(getuid())->pw_dir;
  }
  std::string name;
  if (output == "sw")
    name = "/sw_apicalls_output.log"; 
  else if (output == "script")
    name = "/sw_scripts_output.log";
  else if (output == "eventListener")
    name = "/sw_event_listener_output.log";
  else
    name = "/sw_error_output.log";       
  return homedir+name;
}

int instrumentation_log(std::string info, std::string output, std::string baseUrl) {
  
  std::string path = get_path(output);
  info = info+" "+baseUrl+" "+instrumentation_get_times();
  std::ofstream myfile;
  myfile.open (path, std::ios::out | std::ios::app );
  myfile << info +"\n";
  myfile.close();
  return 0;
}