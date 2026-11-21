locals {
  resource_prefix = "${split("-", var.bucket_name)[0]}-"
}