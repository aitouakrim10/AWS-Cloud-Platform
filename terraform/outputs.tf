output "namespace" {
  value       = kubernetes_namespace.platform.metadata[0].name
  description = "Namespace deploye"
}

output "frontend_service_type" {
  value       = kubernetes_service.frontend.spec[0].type
  description = "Type du service frontend deploye"
}
