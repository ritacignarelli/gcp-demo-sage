# Bucket Cloud Storage che contiene il file di istruzioni aggiuntive (istruzioni.md)
# letto da Sage a ogni richiesta per guidare le risposte del modello.
resource "google_storage_bucket" "sage_instructions" {
  name     = "${var.resource_prefix}-instructions"
  project  = var.project_id
  location = var.region

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  force_destroy = true
}

# Il service account di Cloud Run deve poter leggere il file di istruzioni.
resource "google_storage_bucket_iam_member" "sage_run_instructions_viewer" {
  bucket = google_storage_bucket.sage_instructions.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.sage_run.email}"
}