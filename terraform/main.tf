# Namespace
resource "kubernetes_namespace" "platform" {
  metadata { name = var.namespace }
}

# Secrets pour Flask
resource "kubernetes_secret" "backend_secret" {
  metadata {
    name      = "backend-secret"
    namespace = kubernetes_namespace.platform.metadata[0].name
  }
  string_data = {
    SECRET_KEY = var.secret_key
    FLASK_ENV  = var.flask_env
  }
  type = "Opaque"
}

# Deployment backend (simple)
resource "kubernetes_deployment" "backend" {
  metadata {
    name      = "backend"
    namespace = kubernetes_namespace.platform.metadata[0].name
    labels    = { app = "backend" }
  }
  spec {
    replicas = 1
    selector { match_labels = { app = "backend" } }
    template {
      metadata { labels = { app = "backend" } }
      spec {
        container {
          name  = "backend"
          image = "${var.backend_image}:${var.backend_tag}"
          image_pull_policy = "IfNotPresent"
          port { container_port = 5000 }
          env { name = "FLASK_ENV"  value_from { secret_key_ref { name = kubernetes_secret.backend_secret.metadata[0].name key = "FLASK_ENV" } } }
          env { name = "SECRET_KEY" value_from { secret_key_ref { name = kubernetes_secret.backend_secret.metadata[0].name key = "SECRET_KEY" } } }
        }
      }
    }
  }
}

# Service backend
resource "kubernetes_service" "backend" {
  metadata {
    name      = "backend-service"
    namespace = kubernetes_namespace.platform.metadata[0].name
    labels    = { app = "backend" }
  }
  spec {
    selector = { app = "backend" }
    port { port = 5000 target_port = 5000 }
    type = "ClusterIP"
  }
}

# Deployment frontend (Nginx)
resource "kubernetes_deployment" "frontend" {
  metadata {
    name      = "frontend"
    namespace = kubernetes_namespace.platform.metadata[0].name
    labels    = { app = "frontend" }
  }
  spec {
    replicas = 1
    selector { match_labels = { app = "frontend" } }
    template {
      metadata { labels = { app = "frontend" } }
      spec {
        container {
          name  = "frontend"
          image = "${var.frontend_image}:${var.frontend_tag}"
          image_pull_policy = "IfNotPresent"
          port { container_port = 8080 }
          env { name = "BACKEND_SERVICE_URL" value = "http://backend-service:5000" }
        }
      }
    }
  }
}

# Service frontend (NodePort pour accès simple)
resource "kubernetes_service" "frontend" {
  metadata {
    name      = "frontend-service"
    namespace = kubernetes_namespace.platform.metadata[0].name
    labels    = { app = "frontend" }
  }
  spec {
    selector = { app = "frontend" }
    port { port = 80 target_port = 8080 }
    type = "NodePort"
  }
}
