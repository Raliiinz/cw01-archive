
# IAM roles required by the system's service accounts.
locals {
  service_account_roles = {
    # API Gateway: send tasks, read metadata and download ZIP files.
    gateway_ymq = {
      account_id = yandex_iam_service_account.gateway.id
      role       = "ymq.writer"
    }

    gateway_ydb = {
      account_id = yandex_iam_service_account.gateway.id
      role       = "ydb.viewer"
    }

    gateway_storage = {
      account_id = yandex_iam_service_account.gateway.id
      role       = "storage.viewer"
    }

    # Archive function: upload ZIP files and save metadata.
    worker_storage = {
      account_id = yandex_iam_service_account.worker.id
      role       = "storage.uploader"
    }

    worker_ydb = {
      account_id = yandex_iam_service_account.worker.id
      role       = "ydb.editor"
    }

    # Trigger: read queue messages and invoke the function.
    trigger_ymq = {
      account_id = yandex_iam_service_account.trigger.id
      role       = "ymq.reader"
    }

    trigger_function = {
      account_id = yandex_iam_service_account.trigger.id
      role       = "functions.functionInvoker"
    }

    # Provisioner: manage resources through Terraform.
    provisioner_ymq = {
      account_id = yandex_iam_service_account.provisioner.id
      role       = "ymq.admin"
    }

    provisioner_storage = {
      account_id = yandex_iam_service_account.provisioner.id
      role       = "storage.admin"
    }

    provisioner_ydb = {
      account_id = yandex_iam_service_account.provisioner.id
      role       = "ydb.editor"
    }
  }
}

# Assign each IAM role within the target folder.
resource "yandex_resourcemanager_folder_iam_member" "service_roles" {
  for_each = local.service_account_roles

  folder_id = var.folder_id
  role      = each.value.role
  member    = "serviceAccount:${each.value.account_id}"
}
