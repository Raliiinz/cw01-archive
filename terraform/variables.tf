
variable "cloud_id" {
  description = "Идентификатор облака Yandex Cloud"
  type        = string
}

variable "folder_id" {
  description = "Идентификатор каталога Yandex Cloud"
  type        = string
}

variable "bucket_name" {
  description = "Имя бакета Object Storage"
  type        = string

  validation {
    condition     = can(regex("^vvot[0-9]{2}-", var.bucket_name))
    error_message = "Имя бакета должно начинаться с vvotNN-."
  }
}
