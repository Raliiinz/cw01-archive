
# Public HTTP endpoint of the API Gateway.
output "api_gateway_url" {
  description = "Base URL of the archiving API"
  value       = "https://${yandex_api_gateway.archive.domain}"
}

# Resource names for deployment verification.
output "archive_bucket_name" {
  description = "Object Storage bucket for ZIP archives"
  value       = yandex_storage_bucket.archives.bucket
}

output "ydb_database_name" {
  description = "YDB database name"
  value       = yandex_ydb_database_serverless.archives.name
}
