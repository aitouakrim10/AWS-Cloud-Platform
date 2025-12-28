variable "namespace" {
  description = "Namespace Kubernetes"
  type        = string
  default     = "platform"
}

variable "secret_key" {
  description = "Secret Flask"
  type        = string
  default     = "+++++"
}

variable "flask_env" {
  description = "Environnement Flask"
  type        = string
  default     = "development"
}

variable "backend_image" {
  description = "Image backend"
  type        = string
  default     = "platform_backend"
}

variable "frontend_image" {
  description = "Image frontend"
  type        = string
  default     = "platform_frontend"
}

variable "backend_tag" {
  description = "Tag backend"
  type        = string
  default     = "latest"
}

variable "frontend_tag" {
  description = "Tag frontend"
  type        = string
  default     = "latest"
}
