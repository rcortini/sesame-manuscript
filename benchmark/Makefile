SHELL := /bin/bash
DOCKER_NAME = test2

all: run-docker-analysis

run-docker-analysis:
	if [[ "$(shell which docker)" == "" ]]; then \
		echo "error: Docker is required to run this pipeline."; \
		exit 1; \
	fi
	docker build -t $(DOCKER_NAME) .
	docker run -v $(CURDIR):/benchmark $(DOCKER_NAME) make -C /benchmark benchmark

benchmark :
	bash scripts/jobs_generate.sh; \
	  cd data/genomes; \
	  make -n
