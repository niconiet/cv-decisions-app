# decisions_bot

* Build
		docker build --no-cache=true -t sr-docker-xp01.corp.cablevision.com.ar:5000/cv-decisions-bot:latest -t sr-docker-xp01.corp.cablevision.com.ar:5000/cv-decisions-bot:1.0 .

* Run: (El puerto del environment tiene que ser igual al puerto del host que está haciendo binding)
        docker run -d --restart=always -v architecture-decisions-app:/volume --name=cv-decisions-bot --dns=192.168.182.46 --dns=192.168.5.11 --dns-search=corp.cablevision.com.ar -h=sr-docker-xd02.corp.cablevision.com.ar -p 80:80 sr-docker-xp01.corp.cablevision.com.ar:5000/cv-decisions-bot:latest

* Stop
		docker stop cv-decisions-bot

* Remove
		docker rm cv-decisions-bot

* Logs
		docker logs -f

* Docker save
	    docker save nrnieto/cv-decisions-bot > /home/nico/Desktop/cv-decisions.tar

* Docker load
        docker load < cv-decisions.tar

* Remove stopped containers
        docker rm $(docker ps -q -f status=exited)

* Remove untagged images
        docker rmi -f $(docker images | grep "<none>" | awk "{print $3}")