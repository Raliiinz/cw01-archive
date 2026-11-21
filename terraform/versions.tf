
terraform {
  required_version = ">= 1.6.0, < 2.0.0"

  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "= 0.243.0"
    }

    archive = {
      source  = "hashicorp/archive"
      version = "= 2.7.1"
    }
  }
}
