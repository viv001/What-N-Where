#!/usr/bin/python


#=====================================================================
# import libraries

import sys
# This is the python parsing module, with large variety of features
from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex

# This is the python datetime parser
from dateutil import parser
#=====================================================================



# Format of the linux sysfile
# =======================================================================
#   Month Data time hostname application[processid]: Message_text 
# =======================================================================
 
class Syslog_Parser(object):

  # This Function parses the syslog style line and converts into data dictionary

  def parse(self, line):
    parsed = self.__expression.parseString(line)
    data_dictionary = {}
    data_dictionary["timestamp"] = parser.parse(parsed[0]+" "+parsed[1]+" "+parsed[2])

    data_dictionary["hostname"]  = parsed[3]
    data_dictionary["application"]   = parsed[4]
    if len(parsed)==7:
        data_dictionary["pid"]       = parsed[5]
        data_dictionary["message"]   = parsed[6]
    else:
        data_dictionary["pid"] = ""
        data_dictionary["message"]   = parsed[5]
    return data_dictionary


  # This function converts the data dictionary into JSON format

  def to_json(self,data_dictionary):
    s = "{ "
    cnt=0
    for i in data_dictionary:
        s += '"'+str(i)+'"'+":"+'"'+str(data_dictionary[i])+'"'
        if cnt==len(data_dictionary)-1:
            s += " "
        else:
            s += ","
        cnt = cnt + 1
    s += "}"
    return s

  # This is the required regex work
  # required for the conversion
  def __init__(self):
    integers = Word(nums)
    month = Word(string.uppercase, string.lowercase, exact=3)
    day   = integers
    hour  = Combine(integers + ":" + integers + ":" + integers)
    timestamp = month + day + hour
    hostname = Word(alphas + nums + "_" + "-" + ".")
    application = Word(alphas + nums + "/" + "-" + "_" + ".") + Optional(Suppress("[") + integers + Suppress("]")) + Suppress(":")
    message = Regex(".*")
    self.__expression = timestamp + hostname + application + message


###########################################################
#       THIS IS THE MAIN FUNCTION
###########################################################

# It takes in input the log filename as command line arguments and prints
# the json data

def main():
  parser = Syslog_Parser()
  data = []
  filename = sys.argv[1]
  with open(filename) as syslogFile:
    for line in syslogFile:
      fields = parser.parse(line)
      data.append(parser.to_json(fields))
  print "[",
  for i in range(len(data)):
      if i==len(data)-1:
        print data[i],
      else:
        print data[i],
        print ","
  print "]",

if __name__ == "__main__":
    main()
