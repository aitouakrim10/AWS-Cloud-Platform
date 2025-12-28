terraform {
  required_version = ">= 1.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}

# Utilise le contexte Minikube local
provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "minikube"
}
