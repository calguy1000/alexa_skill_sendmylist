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

dialog:
	docker compose run -it --user worker alexa-skill-dev ask dialog --locale en-US

clean:
	docker compose down
	_list=`docker ps -a | grep alexa-skill-dev | grep Exited | cut -d ' ' -f1`
	if [ "$$_list" != "" ]; then docker rm $_list; fi

help:
    @echo "shell: Run a shell in the container"
    @echo "root: Run a root shell in the container"
    @echo "build: Build the container" 
    @echo "run: Run the skill locally, for debugging"
    @echo "deploy: Deploy the skill"
    @echo "dialog: Test the skill using the interactive dialog tool"
    @echo "clean: Clean up the container"
    @echo "help: Show this help message"


