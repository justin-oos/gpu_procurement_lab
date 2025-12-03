## 🛠️ Environment Setup

### Step 1: Terraform
1. Install Terraform.
2. Initialize and Apply:
   ```bash
   cd infra
   terraform init
   terraform apply -var="project_id=YOUR_PROJECT_ID"
   ```


### Step 2: Permit Vertex AI Service Account to Access your GCS Bucket

TODO: Automate this step:

Ensure service account `service-{project_number}@gcp-sa-aiplatform.iam.gserviceaccount.com` has objectViewer permissions on the GCS bucket for Legal.


### Step 3: Local Setup (For local development and testing)
1. Set up GCP authentication (For gdrive integration, please follow instructions from GDRIVE_SETUP.md file):
   ```bash
   gcloud auth login
   gcloud auth application default login
   ```
2. Create and activate a Python virtual environment (Python 3.12 recommended):
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```
3. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Phase 1 demo:
   ```bash
   bash run_phase1_demo.sh
   ```
5. Run the Phase 2 demo:
   ```bash
   bash run_phase2_demo.sh
   ```
