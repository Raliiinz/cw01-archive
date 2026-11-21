
# HTTP entry point for the archiving system.
resource "yandex_api_gateway" "archive" {
  folder_id   = var.folder_id
  name        = "${local.resource_prefix}archive-gateway"
  description = "HTTP API for asynchronous file archiving"

  # Render the OpenAPI specification using Terraform-managed resources.
  spec = templatefile("${path.module}/../openapi.yaml", {
    queue_url          = yandex_message_queue.tasks.id
    folder_id          = var.folder_id
    service_account_id = yandex_iam_service_account.gateway.id
    database_path      = yandex_ydb_database_serverless.archives.database_path
    bucket_name        = yandex_storage_bucket.archives.bucket
  })

  # Ensure IAM roles and the document table are ready.
  depends_on = [
    yandex_resourcemanager_folder_iam_member.service_roles,
    terraform_data.archives_table
  ]
}
