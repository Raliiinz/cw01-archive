
# Trigger that processes messages from the archiving task queue.
resource "yandex_function_trigger" "archive_tasks" {
  folder_id   = var.folder_id
  name        = "${local.resource_prefix}archive-trigger"
  description = "Invoke archive function for YMQ tasks"

  # Source: main Message Queue.
  message_queue {
    queue_id           = yandex_message_queue.tasks.arn
    service_account_id = yandex_iam_service_account.trigger.id

    # Process exactly one task per invocation.
    batch_size   = "1"
    batch_cutoff = "0"

    # Keep message invisible during function execution.
    visibility_timeout = "900"
  }

  # Target: Python archiving function.
  function {
    id                 = yandex_function.archiver.id
    tag                = "$latest"
    service_account_id = yandex_iam_service_account.trigger.id
  }

  # Create only after the service account roles exist.
  depends_on = [
    yandex_resourcemanager_folder_iam_member.service_roles
  ]
}
