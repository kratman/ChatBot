###########################
#                         #
#        GabbieBot        #
#                         #
#    A simple chat bot    #
#                         #
###########################

### Location of GabbieBot ###
GABBIEPATH="home/kratz/Dropbox/Repos/ChatBot"

### Standard compiler settings ###

CXX=g++
CXXFLAGS=-static -Ofast -fopenmp

### Libarary settings ###

LDFLAGS=

### Python settings ###

PYPATH=/usr/bin/python

### Sed commands ###

#In-place flag (GNU: -i, OSX: -i "")
SEDI=-i

### Advanced compiler settings for developers ###

DEVFLAGS=-g -Wall -std=c++14

#####################################################

### Compile rules for users and devs ###



#####################################################

