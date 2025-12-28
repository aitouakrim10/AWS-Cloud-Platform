# Déploiement simple (niveau junior)

Prérequis: Minikube, kubectl, Terraform
Construire les images dans Minikube:
```
eval $(minikube docker-env)
docker compose -f docker/docker-compose.yml build
```
 Déployer:
```
cd terraform
terraform init
terraform apply
```
Accès: `minikube service -n platform frontend-service`
