provider "google" {
  project = "your-gcp-project-id"
  region  = "asia-northeast3"
}

resource "google_cloud_run_v2_service" "atlas_api" {
  name     = "atlas-api-service"
  location = "asia-northeast3"

  template {
    containers {
      image = "gcr.io/your-gcp-project-id/atlas-api:latest"
      ports {
        container_port = 8000
      }
    }
  }
}

resource "google_project_iam_member" "run_invoker" {
  project = google_cloud_run_v2_service.atlas_api.project
  role    = "roles/run.invoker"
  member  = "allUsers"
}
