#!/bin/bash
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

# Configuration
API_PORT=8080
API_HOST="127.0.0.1"
PHASE_DIR="../labs/phase1"
VENV_DIR="$PHASE_DIR/.venv"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Load load environment
. base_env.sh

API_PORT=8080
API_HOST="127.0.0.1"

cd ../assets/mock_api
pip install -r requirements.txt
uvicorn main:app --host $API_HOST --port $API_PORT