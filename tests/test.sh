#!/bin/bash
./pyLoadCore.py -v
./pyLoadCore.py --daemon -c -d
until [ "`./pyLoadCli.py -u pyload --pw=pyload status`" == "No downloads running." ]
do
	sleep 1
done
./pyLoadCli.py -u pyload --pw=pyload add Test http://proof.ovh.net/files/10Mio.dat
echo "Added download test"
sleep 5
until [ "`./pyLoadCli.py -u pyload --pw=pyload status`" == "No downloads running." ]
do
	./pyLoadCli.py -u pyload --pw=pyload status
	sleep 5
done
echo "Download test completed"
./pyLoadCli.py -u pyload --pw=pyload queue
if [[ "`./pyLoadCli.py -u pyload --pw=pyload queue`" == *failed* ]]
then
	echo "Download failed"
	./pyLoadCore.py --quit
	exit 1
fi
./pyLoadCore.py --quit
