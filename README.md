# home-server
Very modularized/customizable home server

If you require sudo to run docker commands please run 'sudo chmod o=rwx /var/run/docker.sock'

To add docker containers they should either not have network ports or only expose the containers 80 port
There is currently no volume support
