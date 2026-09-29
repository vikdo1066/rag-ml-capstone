resource "google_vertex_ai_index" "rag_index" {
  display_name = "rag-index"
  region       = var.region

  metadata {
    contents_delta_uri = var.embeddings_bucket_uri

    config {
      shard_size                  = "SHARD_SIZE_SMALL"
      dimensions                  = 768
      approximate_neighbors_count = 20
      distance_measure_type       = "DOT_PRODUCT_DISTANCE"
      algorithm_config {
        tree_ah_config {
          leaf_node_embedding_count    = 1000
          leaf_nodes_to_search_percent = 10
        }
      }
    }
  }

  index_update_method = "STREAM_UPDATE"   # supports incremental upserts
}

resource "google_vertex_ai_index_endpoint" "rag_endpoint" {
  display_name            = "rag-index-endpoint"
  region                  = var.region
  public_endpoint_enabled = true
}

resource "google_vertex_ai_index_endpoint_deployed_index" "rag_deployed" {
  index_endpoint    = google_vertex_ai_index_endpoint.rag_endpoint.id
  index             = google_vertex_ai_index.rag_index.id
  deployed_index_id = "rag_deployed_v1"
  display_name      = "rag-deployed-v1"

  dedicated_resources {
    machine_spec { machine_type = "e2-standard-2" }

    min_replica_count = 1
    max_replica_count = 1
  }
}

resource "google_storage_bucket_iam_member" "indexer_raw_reader" {
  bucket = var.raw_docs_bucket_name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${var.rag_indexer_email}"
}

resource "google_storage_bucket_iam_member" "indexer_embeddings_writer" {
  bucket = var.embeddings_bucket_name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${var.rag_indexer_email}"
}

resource "google_project_iam_member" "indexer_aiplatform" {
  project = var.project_id
  role    = "roles/aiplatform.user"   # broader than predictionServiceUser; index update needs aiplatform.indexes.update
  member  = "serviceAccount:${var.rag_indexer_email}"
}
