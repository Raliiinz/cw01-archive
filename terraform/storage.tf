
resource "yandex_storage_bucket" "archives" {
  folder_id = var.folder_id
  bucket    = var.bucket_name

  max_size = 10737418240

  # Remove objects together with the bucket during terraform destroy.
  force_destroy = true

  anonymous_access_flags {
    read        = false
    list        = false
    config_read = false
  }

  access_key = yandex_iam_service_account_static_access_key.provisioner.access_key
  secret_key = yandex_iam_service_account_static_access_key.provisioner.secret_key
}
