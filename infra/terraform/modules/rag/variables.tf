variable "project_id" {
  type        = string
  description = "The ID of the project to create the resources in"
}

variable "region" {
  type        = string
  description = "The region to create the resources in"
}

variable "embeddings_bucket_uri" {
  type        = string
  description = "The URI of the embeddings bucket"
}

variable "raw_docs_bucket_name" {
  type        = string
  description = "The name of the raw docs bucket"
}

variable "embeddings_bucket_name" {
  type        = string
  description = "The name of the embeddings bucket"
}

variable "rag_indexer_email" {
  type        = string
  description = "The email of the rag indexer service account"
}