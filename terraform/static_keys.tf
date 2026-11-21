
resource "yandex_iam_service_account_static_access_key" "provisioner" {
  service_account_id = yandex_iam_service_account.provisioner.id
  description        = "Static access key for infrastructure provisioning"

  depends_on = [
    yandex_resourcemanager_folder_iam_member.service_roles
  ]
}

resource "yandex_iam_service_account_static_access_key" "worker" {
  service_account_id = yandex_iam_service_account.worker.id
  description        = "Static access key for archive worker"

  depends_on = [
    yandex_resourcemanager_folder_iam_member.service_roles
  ]
}
