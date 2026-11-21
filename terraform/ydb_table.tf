
resource "terraform_data" "archives_table" {

  # Store credentials as sensitive values.
  # Terraform hides them from human-readable plans.
  store {
    input = {
      endpoint   = yandex_ydb_database_serverless.archives.document_api_endpoint
      access_key = yandex_iam_service_account_static_access_key.provisioner.access_key
      secret_key = yandex_iam_service_account_static_access_key.provisioner.secret_key
    }

    sensitive = true
  }

  triggers_replace = [
    yandex_ydb_database_serverless.archives.id
  ]

  provisioner "local-exec" {
    working_dir = "${path.module}/.."
    command     = "python scripts/ydb_table.py create"

    environment = {
      YDB_DOCUMENT_ENDPOINT = self.store.sensitive_output.endpoint
      AWS_ACCESS_KEY_ID     = self.store.sensitive_output.access_key
      AWS_SECRET_ACCESS_KEY = self.store.sensitive_output.secret_key
    }
  }

  provisioner "local-exec" {
    when        = destroy
    working_dir = "${path.module}/.."
    command     = "python scripts/ydb_table.py delete"

    environment = {
      YDB_DOCUMENT_ENDPOINT = self.store.sensitive_output.endpoint
      AWS_ACCESS_KEY_ID     = self.store.sensitive_output.access_key
      AWS_SECRET_ACCESS_KEY = self.store.sensitive_output.secret_key
    }
  }
}
