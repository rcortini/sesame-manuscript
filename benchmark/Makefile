SHELL := /bin/bash
DOCKER_NAME = test2
GENOMES_DOWNLOAD_LOG = data/1_download_genomes.log
GENOMES_INDEX_LOG = data/2_make_genomes_index.log

all: run-docker-analysis

benchmark : $(GENOMES_DOWNLOAD_LOG) $(GENOMES_INDEX_LOG)

run-docker-analysis:
	if [[ "$(shell which docker)" == "" ]]; then \
		echo "error: Docker is required to run this pipeline."; \
		exit 1; \
	fi
	docker build -t $(DOCKER_NAME) .
	docker run -v $(CURDIR):/benchmark $(DOCKER_NAME) make -C /benchmark benchmark

$(GENOMES_DOWNLOAD_LOG) :
	bash scripts/1_download_genomes.sh > $@

$(GENOMES_INDEX_LOG) : $(GENOMES_DOWNLOAD_LOG)
	bash scripts/2_make_genomes_index.sh > $@
