###########################
#                         #
#        GabbieBot        #
#                         #
#    A simple chat bot    #
#                         #
###########################

### Python settings ###

PYPATH=/usr/bin/python2

### Sed commands ###

#In-place flag (GNU: -i, OSX: -i "")
SEDI=-i

#####################################################

### Compile rules for users and devs ###

install:	title binary stats compdone

clean:	title delbin compdone

#####################################################

### Rules for building various parts of the code ###

binary:	
	@echo ""; \
	echo "### Building executables ###"; \
	echo ""; \
	mkdir -p bin
	@echo 'echo "#!$(PYPATH)" > ./bin/RunGabbie'; \
	echo "!!${PYPATH}" > ./bin/RunGabbie
	cat ./src/RunGabbie.py >> ./bin/RunGabbie
	@echo 'echo "#!$(PYPATH)" > ./bin/TrainGabbie'; \
	echo "!!${PYPATH}" > ./bin/TrainGabbie
	cat ./src/TrainGabbie.py >> ./bin/TrainGabbie
	@sed $(SEDI) 's/\#.*//g' ./bin/*; \
	sed $(SEDI) 's/[[:space:]]*$$//g' ./bin/*; \
	sed $(SEDI) '/^$$/d' ./bin/*; \
	sed $(SEDI) 's/\!\!/\#\!/g' ./bin/*
	echo "#!/bin/bash" > ./bin/GabbieForget
	cat ./src/Forget.bash >> ./bin/GabbieForget
	@chmod a+x ./bin/*

title:	
	@echo ""; \
	echo "###################################################"; \
	echo "#                                                 #"; \
	echo "#                    GabbieBot                    #"; \
	echo "#                                                 #"; \
	echo "#                A simple chat bot                #"; \
	echo "#                                                 #"; \
	echo "###################################################"

stats:	
	@echo ""; \
	echo "### Source code statistics ###"; \
	echo ""; \
	echo "Number of GabbieBot source code files:"; \
	ls -al src/* | wc -l; \
	echo "Total length of GabbieBot (lines):"; \
	cat src/* | wc -l

compdone:	
	@echo ""; \
	echo "Done."; \
	echo ""

delbin:	
	@echo ""; \
	echo '     ___'; \
	echo '    |_  |'; \
	echo '      \ \'; \
	echo '      |\ \'; \
	echo '      | \ \'; \
	echo '      \  \ \'; \
	echo '       \  \ \'; \
	echo '        \  \ \       <wrrr vroooom wrrr> '; \
	echo '         \__\ \________'; \
	echo '             |_________\'; \
	echo '             |__________|  ..,  ,.,. .,.,, ,..'; \
	echo ""; \
	echo ""; \
	echo "Removing binaries..."; \
	rm -rf ./bin
