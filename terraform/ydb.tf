
# Serverless YDB database for archive metadata.
resource "yandex_ydb_database_serverless" "archives" {
  folder_id = var.folder_id
  name      = "${local.resource_prefix}archives-db"

  # Allow Terraform to delete the database during cleanup.
  deletion_protection = false

  serverless_database {
    # Provisioned capacity: 10 RU per second.
    provisioned_rcu_limit = 10

    # Maximum database storage: 1 GB.
    storage_size_limit = 1
  }
}
