
# Manage the YDB document table within the Terraform lifecycle.
resource "terraform_data" "archives_table" {
  input = {
    endpoint   = yandex_ydb_database_serverless.archives.document_api_endpoint
    access_key = yandex_iam_service_account_static_access_key.provisioner.access_key
    secret_key = yandex_iam_service_account_static_access_key.provisioner.secret_key
  }

  # Recreate the table if the underlying database is replaced.
  triggers_replace = [
    yandex_ydb_database_serverless.archives.id
  ]

  # Create the document table after YDB and credentials exist.
  provisioner "local-exec" {
    working_dir = "${path.module}/.."
    command     = "python scripts/ydb_table.py create"

    environment = {
      YDB_DOCUMENT_ENDPOINT = self.input.endpoint
      AWS_ACCESS_KEY_ID     = self.input.access_key
      AWS_SECRET_ACCESS_KEY = self.input.secret_key
    }
  }

  # Delete the table when Terraform destroys the infrastructure.
  provisioner "local-exec" {
    when        = destroy
    working_dir = "${path.module}/.."
    command     = "python scripts/ydb_table.py delete"

    environment = {
      YDB_DOCUMENT_ENDPOINT = self.input.endpoint
      AWS_ACCESS_KEY_ID     = self.input.access_key
      AWS_SECRET_ACCESS_KEY = self.input.secret_key
    }
  }
}
