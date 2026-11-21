
resource "yandex_iam_service_account" "gateway" {
  folder_id   = var.folder_id
  name        = "${local.resource_prefix}gateway-sa"
  description = "Service account for API Gateway"
}

resource "yandex_iam_service_account" "worker" {
  folder_id   = var.folder_id
  name        = "${local.resource_prefix}worker-sa"
  description = "Service account for archive processing"
}

resource "yandex_iam_service_account" "trigger" {
  folder_id   = var.folder_id
  name        = "${local.resource_prefix}trigger-sa"
  description = "Service account for the YMQ trigger"
}

resource "yandex_iam_service_account" "provisioner" {
  folder_id   = var.folder_id
  name        = "${local.resource_prefix}provisioner-sa"
  description = "Service account for infrastructure provisioning"
}
