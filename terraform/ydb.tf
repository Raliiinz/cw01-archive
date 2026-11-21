
resource "yandex_ydb_database_serverless" "archives" {
  folder_id = var.folder_id
  name      = "${local.resource_prefix}archives-db"

  deletion_protection = false

  serverless_database {
    provisioned_rcu_limit = 10

    storage_size_limit = 1
  }
}
