
# Private Object Storage bucket for ZIP archives.
resource "yandex_storage_bucket" "archives" {
  # Bucket name is provided by the user.
  # No hardcoded account-specific names.
  folder_id = var.folder_id
  bucket    = var.bucket_name

  # Maximum bucket size: 10 GiB.
  max_size = 10737418240

  # Remove objects together with the bucket during terraform destroy.
  force_destroy = true

  # Disable public access to archives and bucket configuration.
  anonymous_access_flags {
    read        = false
    list        = false
    config_read = false
  }

  # Credentials created automatically by Terraform.
  access_key = yandex_iam_service_account_static_access_key.provisioner.access_key
  secret_key = yandex_iam_service_account_static_access_key.provisioner.secret_key
}
