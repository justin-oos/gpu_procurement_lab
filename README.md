## 🛠️ Environment Setup

### Option 1: Terraform (Recommended for Production simulation)
1. Install Terraform.
2. Initialize and Apply:
   ```bash
   cd infra
   terraform init
   terraform apply -var="project_id=YOUR_PROJECT_ID"