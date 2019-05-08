SHELL := /bin/bash
DOCKER_NAME = test2
GENOMES_DOWNLOAD_LOG = 1_download_genomes.log
GENOMES_INDEX_LOG = 2_make_genomes_index.log

all: run-docker-analysis

benchmark : genomes-index

run-docker-analysis:
	if [[ "$(shell which docker)" == "" ]]; then \
		echo "error: Docker is required to run this pipeline."; \
		exit 1; \
	fi
	docker build -t $(DOCKER_NAME) .
	docker run -v $(CURDIR):/benchmark $(DOCKER_NAME) make -C /benchmark benchmark

genomes-download :
	cd scripts; \
	bash 1_download_genomes.sh > $(GENOMES_DOWNLOAD_LOG)
  
$(GENOMES_DOWNLOAD_LOG) : genomes-download

genomes-index : $(GENOMES_DOWNLOAD_LOG)
	cd scripts; \
	bash 2_make_genomes_index.sh > $(GENOMES_INDEX_LOG)
