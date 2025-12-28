# Platform as a Service - Infrastructure

Ce projet contient tous les fichiers nécessaires pour déployer la plateforme sur Minikube.

## Structure du projet

```
platform_as_service/
├── app/                    # Code de l'application
│   ├── backend/           # API Backend (Flask)
│   └── frontend/          # Frontend (Nginx + HTML/JS)
├── docker/                # Fichiers Docker
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── docker-compose.yml
│   └── nginx.conf
├── k8s/                   # Manifests Kubernetes
│   ├── namespace.yaml
│   ├── secret.yaml
│   ├── configmap-nginx.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   └── ingress.yaml
├── terraform/             # Infrastructure as Code (Terraform)
│   ├── providers.tf
│   ├── variables.tf
│   ├── main.tf
│   ├── outputs.tf
│   └── README.md
└── ansible/              # Configuration Management (Ansible)
    ├── inventory.ini
    ├── playbook.yml
    ├── ansible.cfg
    ├── group_vars/
    │   └── all.yml
    ├── tasks/
    │   ├── minikube-setup.yml
    │   ├── docker-build.yml
    │   ├── k8s-deploy.yml
    │   └── verify.yml
    └── README.md
```

## Méthodes de déploiement

### 1. Déploiement avec kubectl (Manuel)

```bash
# 1. Construire les images Docker
docker build -t platform-backend:latest -f docker/Dockerfile.backend .
docker build -t platform-frontend:latest -f docker/Dockerfile.frontend .

# 2. Charger les images dans Minikube
minikube image load platform-backend:latest
minikube image load platform-frontend:latest

# 3. Déployer avec kubectl
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/configmap-nginx.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
kubectl apply -f k8s/ingress.yaml

# 4. Vérifier le déploiement
kubectl get all -n platform-as-service

# 5. Accéder à l'application
minikube service frontend-service -n platform-as-service
```

### 2. Déploiement avec Terraform (IaC)

```bash
cd terraform

# Initialiser Terraform
terraform init

# Voir le plan
terraform plan

# Appliquer
terraform apply

# Obtenir l'URL
terraform output frontend_url

# Nettoyer
terraform destroy
```

Voir [terraform/README.md](terraform/README.md) pour plus de détails.

### 3. Déploiement avec Ansible (Automatisé)

```bash
cd ansible

# Déploiement complet
ansible-playbook -i inventory.ini playbook.yml

# Ou par étapes
ansible-playbook -i inventory.ini playbook.yml --tags minikube
ansible-playbook -i inventory.ini playbook.yml --tags docker
ansible-playbook -i inventory.ini playbook.yml --tags k8s
ansible-playbook -i inventory.ini playbook.yml --tags verify
```

Voir [ansible/README.md](ansible/README.md) pour plus de détails.

## Prérequis

- **Minikube**: `curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && sudo install minikube-linux-amd64 /usr/local/bin/minikube`
- **kubectl**: `curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && sudo install kubectl /usr/local/bin/`
- **Docker**: `sudo apt install docker.io -y`
- **Terraform** (optionnel): `wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip && unzip terraform_1.6.0_linux_amd64.zip && sudo mv terraform /usr/local/bin/`
- **Ansible** (optionnel): `sudo apt install ansible -y` ou `pip install ansible`

## Démarrage rapide

```bash
# 1. Démarrer Minikube
minikube start --cpus=2 --memory=4096 --driver=docker

# 2. Activer les addons
minikube addons enable ingress
minikube addons enable dashboard
minikube addons enable metrics-server

# 3. Choisir une méthode de déploiement (voir ci-dessus)

# 4. Accéder à l'application
minikube ip
# Accéder à http://<minikube-ip>:30080
```

## Architecture

### Backend (Python/Flask)
- Port: 5000
- 2 réplicas par défaut
- Health checks configurés
- Variables d'environnement via secrets

### Frontend (Nginx)
- Port: 8080
- 2 réplicas par défaut
- Proxy vers backend pour /api et /socket.io
- Configuration via ConfigMap

### Services
- **backend-service**: ClusterIP (interne uniquement)
- **frontend-service**: NodePort 30080 (accès externe)

### Ingress (optionnel)
- Hostname: platform.local
- Nécessite l'addon ingress de Minikube

## Commandes utiles

```bash
# Voir les pods
kubectl get pods -n platform-as-service

# Voir les logs
kubectl logs -f <pod-name> -n platform-as-service

# Voir les services
kubectl get services -n platform-as-service

# Accéder au dashboard
minikube dashboard

# Obtenir l'IP de Minikube
minikube ip

# Ouvrir le service dans le navigateur
minikube service frontend-service -n platform-as-service

# Redémarrer un deployment
kubectl rollout restart deployment/backend -n platform-as-service
kubectl rollout restart deployment/frontend -n platform-as-service

# Supprimer tous les ressources
kubectl delete namespace platform-as-service
```

## Configuration

### Variables Kubernetes
Les variables sont configurées via:
- **Secrets**: [k8s/secret.yaml](k8s/secret.yaml)
- **ConfigMaps**: [k8s/configmap-nginx.yaml](k8s/configmap-nginx.yaml)

### Variables Terraform
Créer un fichier `terraform/terraform.tfvars`:
```hcl
namespace = "platform-as-service"
backend_replicas = 2
frontend_replicas = 2
secret_key = "votre-cle-secrete"
```

### Variables Ansible
Modifier [ansible/group_vars/all.yml](ansible/group_vars/all.yml):
```yaml
minikube_cpus: 2
minikube_memory: 4096
backend_replicas: 2
frontend_replicas: 2
```

## Monitoring

```bash
# Métriques des ressources
kubectl top pods -n platform-as-service
kubectl top nodes

# Events
kubectl get events -n platform-as-service --sort-by='.lastTimestamp'

# Dashboard Kubernetes
minikube dashboard
```

## Troubleshooting

### Les images ne se chargent pas
```bash
# Vérifier que les images sont dans Minikube
minikube image ls | grep platform

# Recharger les images
eval $(minikube docker-env)
docker build -t platform-backend:latest -f docker/Dockerfile.backend .
docker build -t platform-frontend:latest -f docker/Dockerfile.frontend .
```

### Les pods ne démarrent pas
```bash
# Voir les détails du pod
kubectl describe pod <pod-name> -n platform-as-service

# Voir les logs
kubectl logs <pod-name> -n platform-as-service
```

### Le service n'est pas accessible
```bash
# Vérifier que Minikube tourne
minikube status

# Obtenir l'URL du service
minikube service frontend-service -n platform-as-service --url

# Vérifier le port forwarding
kubectl port-forward service/frontend-service 8080:8080 -n platform-as-service
```

## Nettoyage

```bash
# Supprimer le namespace (supprime toutes les ressources)
kubectl delete namespace platform-as-service

# Avec Terraform
cd terraform && terraform destroy

# Arrêter Minikube
minikube stop

# Supprimer Minikube
minikube delete
```

