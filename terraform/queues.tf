
resource "yandex_message_queue" "dead_letter" {
  name = "${local.resource_prefix}archive-dlq"

  message_retention_seconds = 1209600

  access_key = yandex_iam_service_account_static_access_key.provisioner.access_key
  secret_key = yandex_iam_service_account_static_access_key.provisioner.secret_key
}

resource "yandex_message_queue" "tasks" {
  name = "${local.resource_prefix}archive-tasks"

  visibility_timeout_seconds = 900

  receive_wait_time_seconds = 20

  message_retention_seconds = 86400

  # Move failed tasks to the Dead Letter Queue.
  redrive_policy = jsonencode({
    deadLetterTargetArn = yandex_message_queue.dead_letter.arn
    maxReceiveCount     = 1
  })

  access_key = yandex_iam_service_account_static_access_key.provisioner.access_key
  secret_key = yandex_iam_service_account_static_access_key.provisioner.secret_key
}
