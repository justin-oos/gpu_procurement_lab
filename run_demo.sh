#!/bin/bash

# Configuration
API_PORT=8080
API_HOST="127.0.0.1"
VENV_NAME="l400-env"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Vertex AI L400 Lab 2 Demo Initialization...${NC}"

# --- Step 1: Environment & Dependencies ---
echo -e "\n${BLUE}[1/5] Checking Environment...${NC}"

# Check if we are in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Error: pyproject.toml not found. Run this from the repo root.${NC}"
    exit 1
fi

# Install dependencies in editable mode
echo "📦 Installing package and dependencies..."
pip install -e .
pip install reportlab fastapi uvicorn # Ensure helper libs are present

# --- Step 2: World Building (Data) ---
echo -e "\n${BLUE}[2/5] Building the 'Opaque' Database...${NC}"
python assets/setup_db.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Database setup failed. Check credentials/permissions.${NC}"
    exit 1
fi

echo -e "\n${BLUE}[3/5] creating 'Conflicting' Legal Documents...${NC}"
python assets/setup_gcs.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ GCS setup failed. Check bucket permissions.${NC}"
    exit 1
fi

# --- Step 3: The External World (Mock API) ---
echo -e "\n${BLUE}[4/5] Launching Mock Spot Market API...${NC}"

# Kill any existing process on port 8080 to avoid conflicts
fuser -k $API_PORT/tcp > /dev/null 2>&1

# Start API in background
cd assets/mock_api
uvicorn main:app --host $API_HOST --port $API_PORT > ../../api_logs.txt 2>&1 &
API_PID=$!
cd ../..

echo "✅ API running in background (PID: $API_PID). Logs at ./api_logs.txt"
echo "   Waiting 5 seconds for API to warm up..."
sleep 5

# --- Step 4: The War Room (Agents) ---
echo -e "\n${BLUE}[5/5] 🛡️ INITIALIZING INCIDENT COMMAND WAR ROOM...${NC}"
echo "---------------------------------------------------------------"


# [Image of multi-agent system architecture]


# Run the main agent loop
python main.py

# --- Cleanup ---
echo -e "\n${BLUE}🧹 Cleaning up...${NC}"
kill $API_PID
echo "✅ Mock API stopped."
echo -e "${GREEN}🏁 Demo Complete.${NC}"