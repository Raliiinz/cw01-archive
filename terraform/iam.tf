
locals {
  service_account_roles = {
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

    worker_storage = {
      account_id = yandex_iam_service_account.worker.id
      role       = "storage.uploader"
    }

    worker_ydb = {
      account_id = yandex_iam_service_account.worker.id
      role       = "ydb.editor"
    }

    trigger_ymq = {
      account_id = yandex_iam_service_account.trigger.id
      role       = "ymq.reader"
    }

    trigger_function = {
      account_id = yandex_iam_service_account.trigger.id
      role       = "functions.functionInvoker"
    }

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

resource "yandex_resourcemanager_folder_iam_member" "service_roles" {
  for_each = local.service_account_roles

  folder_id = var.folder_id
  role      = each.value.role
  member    = "serviceAccount:${each.value.account_id}"
}
