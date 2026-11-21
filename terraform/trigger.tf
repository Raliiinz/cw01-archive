
resource "yandex_function_trigger" "archive_tasks" {
  folder_id   = var.folder_id
  name        = "${local.resource_prefix}archive-trigger"
  description = "Invoke archive function for YMQ tasks"

  message_queue {
    queue_id           = yandex_message_queue.tasks.arn
    service_account_id = yandex_iam_service_account.trigger.id

    batch_size   = "1"
    batch_cutoff = "0"

    visibility_timeout = "900"
  }

  function {
    id                 = yandex_function.archiver.id
    tag                = "$latest"
    service_account_id = yandex_iam_service_account.trigger.id
  }

  depends_on = [
    yandex_resourcemanager_folder_iam_member.service_roles
  ]
}
