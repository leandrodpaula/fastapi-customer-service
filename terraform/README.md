# Terraform Configuration for Customer API on Google Cloud Run

This directory contains Terraform scripts to provision the Customer API on Google Cloud Run.

## Prerequisites

1.  **Google Cloud SDK (gcloud)**: [Install and initialize](https://cloud.google.com/sdk/docs/install).
2.  **Terraform**: [Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli).
3.  **Permissions**: Ensure the authenticated GCP user/service account has necessary permissions (e.g., Project Owner, or specific roles like Artifact Registry Admin, Cloud Run Admin, Service Account User, Project IAM Admin).
4.  **APIs Enabled**: The script attempts to enable Artifact Registry and Cloud Run APIs. If this fails due to permissions, enable them manually in the GCP console for your project.

## Setup

1.  **Authenticate with GCP**:
    ```bash
    gcloud auth application-default login
    gcloud config set project YOUR_GCP_PROJECT_ID
    ```

2.  **Create `terraform.tfvars`**:
    Create a file named `terraform.tfvars` in this directory and populate it with your specific values:
    ```tfvars
    gcp_project_id = "your-gcp-project-id"
    gcp_region     = "us-central1" # Or your preferred region
    service_name   = "customer-api"
    mongo_uri      = "your-mongodb-connection-string" # e.g., "mongodb+srv://user:pass@cluster.mongodb.net/yourdbname?retryWrites=true&w=majority"
    mongo_db_name  = "clean_arch_db" # Ensure this matches your application's expected DB name
    container_image = "us-central1-docker.pkg.dev/your-gcp-project-id/customer-api/customer-api-image:latest" # Replace with your actual image path after building and pushing
    ```
    **Important**: `mongo_uri` is sensitive. Do not commit `terraform.tfvars` if it contains real secrets. Use environment variables or a secret manager for production. The `container_image` variable will be the full path to your Docker image in Artifact Registry. You'll typically build and push this image first, then provide its path here.

## Usage

1.  **Initialize Terraform**:
    Navigate to the `terraform` directory in your terminal.
    ```bash
    terraform init
    ```

2.  **Plan**:
    (Optional but recommended) Review the changes Terraform will make.
    ```bash
    terraform plan
    ```

3.  **Apply**:
    Provision the resources.
    ```bash
    terraform apply
    ```
    Type `yes` when prompted.

## Outputs

After a successful apply, Terraform will output:
-   `cloud_run_service_url`: The URL of your deployed service.
-   `artifact_registry_repository_url`: The URL for your Docker image repository in Artifact Registry. You'll use this to tag and push your Docker image.

## Cleanup

To remove all resources created by this configuration:
```bash
terraform destroy
```
Type `yes` when prompted.

## Notes
- The `container_image` variable in `terraform.tfvars` must be updated to point to the image you build and push to Google Artifact Registry. The typical format is `REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME/IMAGE_NAME:TAG`. The `artifact_registry_repository_url` output can help you construct this.
- This configuration sets up the Cloud Run service to be publicly accessible. Adjust IAM policies in `main.tf` if you need restricted access.
- The MongoDB URI is passed as an environment variable. For production, consider using Google Secret Manager and referencing secrets in Cloud Run.
