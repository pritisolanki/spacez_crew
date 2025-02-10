# Local development
run:
	uv run uvicorn api:app --host 0.0.0.0 --port 8000

configure-gcloud:
	gcloud init
	gcloud auth configure-docker $(ARTIFACT_REGISTRY)

# Docker commands
DOCKER_IMAGE_NAME=spacez-crew
DOCKER_TAG=latest
GCP_PROJECT_ID=spacez-450415
GCP_REGION=us-central1
ARTIFACT_REGISTRY=us-central1-docker.pkg.dev

# pre-requisites

docker-build:
	docker build --platform linux/amd64 -t $(DOCKER_IMAGE_NAME):$(DOCKER_TAG) .

docker-run:
	docker run -p 8000:8000 $(DOCKER_IMAGE_NAME):$(DOCKER_TAG)

# GCP commands
gcp-configure:
	gcloud config set project $(GCP_PROJECT_ID)
	gcloud auth configure-docker $(ARTIFACT_REGISTRY)
	gcloud artifacts repositories create $(DOCKER_IMAGE_NAME) --repository-format=docker \
		--location=$(GCP_REGION) --description="Docker repository for SpaceZ Crew"

gcp-build:
	docker build --platform linux/amd64 -t $(ARTIFACT_REGISTRY)/$(GCP_PROJECT_ID)/$(DOCKER_IMAGE_NAME)/$(DOCKER_IMAGE_NAME):$(DOCKER_TAG) .

gcp-push:
	docker push $(ARTIFACT_REGISTRY)/$(GCP_PROJECT_ID)/$(DOCKER_IMAGE_NAME)/$(DOCKER_IMAGE_NAME):$(DOCKER_TAG)

gcp-deploy:
	gcloud run deploy $(DOCKER_IMAGE_NAME) \
		--image $(ARTIFACT_REGISTRY)/$(GCP_PROJECT_ID)/$(DOCKER_IMAGE_NAME)/$(DOCKER_IMAGE_NAME):$(DOCKER_TAG) \
		--platform managed \
		--region $(GCP_REGION) \
		--allow-unauthenticated

# Cleanup commands
gcp-cleanup:
	-gcloud run services delete $(DOCKER_IMAGE_NAME) --region=$(GCP_REGION) --quiet
	-gcloud artifacts repositories delete $(DOCKER_IMAGE_NAME) --location=$(GCP_REGION) --quiet
	-docker rmi $(ARTIFACT_REGISTRY)/$(GCP_PROJECT_ID)/$(DOCKER_IMAGE_NAME)/$(DOCKER_IMAGE_NAME):$(DOCKER_TAG)

# Combined deployment command
deploy-to-gcp: gcp-configure gcp-build gcp-push gcp-deploy

