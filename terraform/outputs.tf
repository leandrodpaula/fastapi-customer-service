# terraform/outputs.tf
output "cloud_run_service_url" {
  description = "URL of the deployed Cloud Run service."
  value       = google_cloud_run_v2_service.default.uri
}

output "artifact_registry_repository_url" {
  description = "URL of the Artifact Registry repository."
  value       = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.default.repository_id}"
}
