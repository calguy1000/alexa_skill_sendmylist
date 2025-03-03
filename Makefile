shell:
	docker compose run -it --user worker alexa-skill-dev bash --login

root:
	docker compose run -it alexa-skill-dev bash --login

build:
	docker compose build

run:
	docker compose run -it --user worker alexa-skill-dev ask run

deploy:
	docker compose run -it --user worker alexa-skill-dev ask deploy

test:
	docker compose run -it --user worker alexa-skill-dev ask dialog --locale en-US

clean:
	docker compose down
	_list=`docker ps -a | grep alexa-skill-dev | grep Exited | cut -d ' ' -f1`
	if [ "$$_list" != "" ]; then docker rm $_list; fi



