#!/bin/bash
./pyLoadCore.py -v
./pyLoadCore.py --daemon -c -d
until [ "`./pyLoadCli.py status`" == "No downloads running." ]
do
	sleep 1
done
./pyLoadCli.py add Test http://proof.ovh.net/files/10Mio.dat
echo "Added download test"
sleep 5
until [ "`./pyLoadCli.py status`" == "No downloads running." ]
do
	./pyLoadCli.py status
	sleep 5
done
echo "Download test completed"
./pyLoadCli.py queue
if [[ "`./pyLoadCli.py queue`" == *failed* ]]
then
	echo "Download failed"
	./pyLoadCore.py --quit
	exit 1
fi
./pyLoadCore.py --quit
