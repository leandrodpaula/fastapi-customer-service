# terraform/main.tf
provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# Enable necessary APIs
resource "google_project_service" "artifactregistry" {
  project = var.gcp_project_id
  service = "artifactregistry.googleapis.com"
  disable_on_destroy = false # Keep it enabled
}

resource "google_project_service" "run" {
  project = var.gcp_project_id
  service = "run.googleapis.com"
  disable_on_destroy = false # Keep it enabled
}

# Artifact Registry for Docker images
resource "google_artifact_registry_repository" "default" {
  project       = var.gcp_project_id
  location      = var.gcp_region
  repository_id = var.service_name # Using service_name as repo name for simplicity
  description   = "Docker repository for ${var.service_name}"
  format        = "DOCKER"
  depends_on    = [google_project_service.artifactregistry]
}

# Cloud Run Service
resource "google_cloud_run_v2_service" "default" {
  project    = var.gcp_project_id
  location   = var.gcp_region
  name       = var.service_name
  depends_on = [google_project_service.run]

  template {
    containers {
      image = var.container_image # This needs to be the full image path in Artifact Registry
      ports {
        container_port = 80 # Default FastAPI port with Uvicorn
      }
      env {
        name  = "MONGO_URI"
        value = var.mongo_uri # Injected as environment variable
      }
      env {
        name  = "MONGO_DB_NAME"
        value = var.mongo_db_name
      }
      # Add other necessary env vars here, e.g., PORT if your app needs it
      # env {
      #   name = "PORT"
      #   value = "80"
      # }
    }
    # Adjust scaling, CPU, memory as needed
    scaling {
      min_instance_count = 0 # Can scale to 0 for cost savings
      max_instance_count = 2 # Example max
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# IAM policy to allow unauthenticated access to the Cloud Run service
data "google_iam_policy" "noauth" {
  binding {
    role    = "roles/run.invoker"
    members = ["allUsers"]
  }
}

resource "google_cloud_run_v2_service_iam_policy" "noauth_policy" {
  project  = google_cloud_run_v2_service.default.project
  location = google_cloud_run_v2_service.default.location
  name     = google_cloud_run_v2_service.default.name
  policy_data = data.google_iam_policy.noauth.policy_data
}
