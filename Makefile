# Copyright 2025 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

-include scripts/base_env.sh

# Define Variables
ifndef project
    override project = $(PROJECT_ID)
endif

ifndef region
    override region = $(LOCATION)
endif


# Define Variables
VENV = venv
BUILD = build
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Define Timestamped Files
VENV_TIMESTAMP = ${BUILD}/.make.venv.done
INSTALL_TIMESTAMP = ${BUILD}/.make.install.done


TERRAFORM_FILES := $(wildcard infra/*.tf)
INIT_TIMESTAMP := infra/.terraform.initialized
DEPLOY_TIMESTAMP := infra/.terraform.deployed


# Default target
.PHONY: all
all: help


# Check the Active GCloud Login
.PHONY: gcloud-check
gcloud-check:
	@echo -n "Active GCP Login: "
	@gcloud config list account --format "value(core.account)"
	@echo -n "Active GCP Project: "
	@gcloud config get-value project 2>&1 | grep -v 'Your active configuration is: '
	@echo -n "Active Service Account: "
	@curl "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email" -H "Metadata-Flavor: Google" && echo ""


# Login and Configure GCloud Project
.PHONY: login
login:
	gcloud auth login --update-adc


# Configure GCloud Project
.PHONY: set-project
set-project:
ifndef project
	$(error project is not set!)
endif
	gcloud config set project $(project)
	gcloud auth application-default set-quota-project $(project)


# Fetch the Metadata Service Account
.PHONY: get-sa
get-sa:
	@curl "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email" -H "Metadata-Flavor: Google" && echo ""


# Update Remote Git Branches
.PHONY: update-branch
update-branch:
	git remote update origin --prune


# Clean Terraform Environment
.PHONY: clean
clean:
	rm -rf infra/.terraform infra/.terraform.lock.hcl infra/.terraform.initialized infra/.terraform.deployed ${BUILD} ${VENV_TIMESTAMP} ${INSTALL_TIMESTAMP}


# Initialize Terraform
$(INIT_TIMESTAMP): infra/*.tf
	terraform -chdir=infra init
	touch $(INIT_TIMESTAMP)

.PHONY: init
init: $(INIT_TIMESTAMP)


# Deploy Terraform infra
$(DEPLOY_TIMESTAMP): $(INIT_TIMESTAMP) infra/*.tf
ifndef project
	$(error project is not set!)
else
	terraform -chdir=infra apply -var="project_id=$(project)"
	touch $(DEPLOY_TIMESTAMP)
endif

.PHONY: deploy
deploy: $(DEPLOY_TIMESTAMP)


# Destroy Terraform infra
.PHONY: destroy
destroy: $(INIT_TIMESTAMP)
ifndef project
	$(error project is not set!)
else
	terraform -chdir=infra destroy -var="project_id=$(project)"
	make clean
endif


# Hydrate infra resources
.PHONY: hydrate
hydrate: deploy $(INSTALL_TIMESTAMP)
	scripts/run_hydrate_infra.sh


# Create virtual environment
${VENV_TIMESTAMP}:
	echo "🐍 Creating Python virtual environment in $(VENV)..."
	python3 -m venv $(VENV)
	mkdir -p ${BUILD}
	${PIP} install --upgrade pip
	touch ${VENV_TIMESTAMP}

.PHONY: venv
venv: ${VENV_TIMESTAMP}


# Install dependencies
${INSTALL_TIMESTAMP}: ${VENV_TIMESTAMP} pyproject.toml
	${PIP} install -e .
	touch ${INSTALL_TIMESTAMP}

.PHONY: install
install: ${INSTALL_TIMESTAMP}


# Run phase 1 demo
.PHONY: run-phase1
run-phase1: hydrate
	make -C labs/phase1 install
	scripts/run_phase1_demo.sh

# Run phase 2 demo
.PHONY: run-phase2
run-phase2: hydrate
	make -C labs/phase2 install
	scripts/run_phase2_demo.sh


# Help
.PHONY: help
help:
	@echo "$(service_slug) - $(service_desc)"
	@echo ""
	@echo "Usage:"
	@echo "  make init                 - Initialize Terraform"
	@echo "  make deploy               - Deploy Terraform infra"
	@echo "  make destroy              - Destroy Terraform infra"
	@echo "  make update-branch        - Refreshes remote Git branches into workspace"
	@echo "  make get-sa               - Fetch the service account associated with the environment"
	@echo "  make gcloud-check         - Check the active GCloud login and project"
	@echo "  make login                - Login to GCloud"
	@echo "  make set-project          - Configure GCloud project"
	@echo "  make clean                - Clean environment"
	@echo "  make help                 - Show help"
	@echo "  make venv                 - Create virtual environment"
	@echo "  make install              - Install runtime dependencies"
	@echo "  make hydrate              - Hydrate infrastructure resources"
	@echo "  make run-phase1           - Run phase 1 demo"
	@echo "  make run-phase2           - Run phase 2 demo"

