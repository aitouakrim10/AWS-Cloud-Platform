# Ansible Configuration for Platform as a Service

This directory contains Ansible playbooks and tasks to automate the deployment of the platform on Minikube.

## Prerequisites

- Ansible >= 2.9
- Minikube
- kubectl
- Docker

Install Ansible:
```bash
sudo apt update
sudo apt install ansible -y
# or
pip install ansible
```

## Structure

```
ansible/
├── inventory.ini           # Inventory file
├── playbook.yml           # Main playbook
├── group_vars/
│   └── all.yml           # Variables
├── tasks/
│   ├── minikube-setup.yml  # Minikube setup tasks
│   ├── docker-build.yml    # Docker build tasks
│   ├── k8s-deploy.yml      # Kubernetes deployment tasks
│   └── verify.yml          # Verification tasks
└── README.md
```

## Usage

### Run the complete deployment

```bash
ansible-playbook -i inventory.ini playbook.yml
```

### Run specific tasks with tags

Setup Minikube only:
```bash
ansible-playbook -i inventory.ini playbook.yml --tags minikube
```

Build Docker images only:
```bash
ansible-playbook -i inventory.ini playbook.yml --tags docker
```

Deploy to Kubernetes only:
```bash
ansible-playbook -i inventory.ini playbook.yml --tags k8s
```

Verify deployment:
```bash
ansible-playbook -i inventory.ini playbook.yml --tags verify
```

### Run specific combinations

Setup and build:
```bash
ansible-playbook -i inventory.ini playbook.yml --tags setup,build
```

Build and deploy:
```bash
ansible-playbook -i inventory.ini playbook.yml --tags build,deploy
```

## Configuration

Edit `group_vars/all.yml` to customize:

```yaml
# Minikube settings
minikube_cpus: 2
minikube_memory: 4096
minikube_disk_size: 20g

# Application settings
backend_replicas: 2
frontend_replicas: 2
secret_key: "your-secret-key"
```

## Tasks Description

### minikube-setup.yml
- Checks if Minikube is installed
- Starts Minikube if not running
- Enables required addons (ingress, dashboard, metrics-server)
- Configures kubectl context

### docker-build.yml
- Builds backend Docker image
- Builds frontend Docker image
- Loads images into Minikube

### k8s-deploy.yml
- Creates Kubernetes namespace
- Applies secrets and ConfigMaps
- Deploys backend and frontend
- Creates services
- Applies ingress (if enabled)
- Waits for deployments to be ready

### verify.yml
- Checks pods status
- Checks services status
- Displays access URLs
- Shows useful kubectl commands

## Cleanup

To delete all resources:
```bash
kubectl delete namespace platform-as-service
```

To stop Minikube:
```bash
minikube stop
```

To delete Minikube:
```bash
minikube delete
```

## Troubleshooting

Check Ansible syntax:
```bash
ansible-playbook playbook.yml --syntax-check
```

Dry run (check mode):
```bash
ansible-playbook -i inventory.ini playbook.yml --check
```

Verbose output:
```bash
ansible-playbook -i inventory.ini playbook.yml -v
# or -vv, -vvv for more verbosity
```

## Access the Application

After successful deployment:

1. Get Minikube IP:
```bash
minikube ip
```

2. Access via NodePort:
```
http://<minikube-ip>:30080
```

3. Or use service URL:
```bash
minikube service frontend-service -n platform-as-service
```

4. With Ingress (add to /etc/hosts):
```
<minikube-ip> platform.local
```
Then access: http://platform.local
