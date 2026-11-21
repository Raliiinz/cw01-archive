
# Static access key for Terraform-managed AWS-compatible resources.
resource "yandex_iam_service_account_static_access_key" "provisioner" {
  service_account_id = yandex_iam_service_account.provisioner.id
  description        = "Static access key for infrastructure provisioning"

  # Create the key after IAM roles have been assigned.
  depends_on = [
    yandex_resourcemanager_folder_iam_member.service_roles
  ]
}
