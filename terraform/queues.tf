
# Dead Letter Queue: stores tasks that could not be processed.
resource "yandex_message_queue" "dead_letter" {
  name = "${local.resource_prefix}archive-dlq"

  # Keep failed tasks for 14 days.
  message_retention_seconds = 1209600

  access_key = yandex_iam_service_account_static_access_key.provisioner.access_key
  secret_key = yandex_iam_service_account_static_access_key.provisioner.secret_key
}

# Main queue: receives archiving tasks from API Gateway.
resource "yandex_message_queue" "tasks" {
  name = "${local.resource_prefix}archive-tasks"

  # Message becomes visible again after 900 seconds.
  visibility_timeout_seconds = 900

  # Long polling: wait up to 20 seconds for messages.
  receive_wait_time_seconds = 20

  # Keep pending tasks for one day.
  message_retention_seconds = 86400

  # Move failed tasks to the Dead Letter Queue.
  redrive_policy = jsonencode({
    deadLetterTargetArn = yandex_message_queue.dead_letter.arn
    maxReceiveCount     = 1
  })

  access_key = yandex_iam_service_account_static_access_key.provisioner.access_key
  secret_key = yandex_iam_service_account_static_access_key.provisioner.secret_key
}
