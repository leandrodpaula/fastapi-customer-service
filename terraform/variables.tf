# terraform/variables.tf
variable "gcp_project_id" {
  description = "The GCP project ID to deploy resources into."
  type        = string
}

variable "gcp_region" {
  description = "The GCP region for the resources."
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Name for the Cloud Run service and Artifact Registry repository."
  type        = string
  default     = "customer-api"
}

variable "mongo_uri" {
  description = "MongoDB connection URI (including database name) for the Cloud Run service. Should be a secret."
  type        = string
  sensitive   = true
}

variable "mongo_db_name" {
  description = "MongoDB database name. This is appended to MONGO_URI if not already present by the app, but good to have for clarity."
  type        = string
  default     = "clean_arch_db" # Should match the one in .env or app config
}

variable "container_image" {
  description = "The Docker container image to deploy (e.g., REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY/IMAGE:TAG)."
  type        = string
  # This will be set dynamically after the image is built and pushed.
  # For initial setup, it might be a placeholder or left empty until build step.
  # For a full CI/CD, this would come from the build pipeline.
  # Example: default = "us-central1-docker.pkg.dev/my-project/customer-api/customer-api-image:latest"
}
