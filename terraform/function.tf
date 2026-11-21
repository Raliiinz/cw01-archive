
# Package the Python function without local caches or virtual environments.
data "archive_file" "function_source" {
  type        = "zip"
  output_path = "${path.module}/function.zip"

  source {
    content  = file("${path.module}/../function/handler.py")
    filename = "handler.py"
  }

  source {
    content  = file("${path.module}/../function/archiver.py")
    filename = "archiver.py"
  }

  source {
    content  = file("${path.module}/../function/storage.py")
    filename = "storage.py"
  }

  source {
    content  = file("${path.module}/../function/database.py")
    filename = "database.py"
  }

  source {
    content  = file("${path.module}/../function/requirements.txt")
    filename = "requirements.txt"
  }
}

# Cloud Function that processes archiving tasks from YMQ.
resource "yandex_function" "archiver" {
  folder_id   = var.folder_id
  name        = "${local.resource_prefix}archive-function"
  description = "Downloads files and saves ZIP archives"

  runtime           = "python312"
  entrypoint        = "handler.handler"
  memory            = 256
  execution_timeout = 600

  service_account_id = yandex_iam_service_account.worker.id

  # Redeploy automatically when the function source changes.
  user_hash = data.archive_file.function_source.output_base64sha256

  # Configuration is created from Terraform-managed resources.
  environment = {
    BUCKET_NAME           = yandex_storage_bucket.archives.bucket
    YDB_DOCUMENT_ENDPOINT = yandex_ydb_database_serverless.archives.document_api_endpoint

    AWS_ACCESS_KEY_ID     = yandex_iam_service_account_static_access_key.worker.access_key
    AWS_SECRET_ACCESS_KEY = yandex_iam_service_account_static_access_key.worker.secret_key
  }

  # Upload the generated ZIP archive.
  content {
    zip_filename = data.archive_file.function_source.output_path
  }

  # Ensure the database table exists before creating the function.
  depends_on = [
    terraform_data.archives_table
  ]
}
