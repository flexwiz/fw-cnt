[![Keycloak CI](https://github.com/ntdtfr/tools/actions/workflows/keycloak-ci.yml/badge.svg)](https://github.com/ntdtfr/tools/actions/workflows/keycloak-ci.yml)
[![Superset CI](https://github.com/ntdtfr/tools/actions/workflows/superset-ci.yml/badge.svg)](https://github.com/ntdtfr/tools/actions/workflows/superset-ci.yml)
[![Security Scanning](https://github.com/ntdtfr/tools/actions/workflows/trivy.yml/badge.svg)](https://github.com/ntdtfr/tools/actions/workflows/trivy.yml)

# Cloud Native Tools (CNT)

This repository contains the infrastructure code and configuration for deploying open-source Cloud Native Tools like database, cache, message broker, gateway, monitoring, logging, and more to multiple environments (development, staging, and production) using Docker, Kubernetes, and Skaffold.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Setup](#environment-setup)
- [Development Workflow](#development-workflow)
- [Deployment](#deployment)
- [Maintenance](#maintenance)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🔍 Overview

This project provides a complete infrastructure setup for running any Cloud Native component (Redis, Keycloak, PostgreSQL, MongoDB, ...) across multiple environments with the following features:

- Containerized deployment using Docker
- Kubernetes orchestration
- Environment-specific configurations using Kustomize
- Developer-friendly workflow using Skaffold
- CI/CD integration for automated deployments

## 🏗️ Architecture

The deployment architecture follows this approach with isolation in dedicated namespace (e.g: Krakend, Keycloak, Metabase):

```
┌─────────────────────────────────────────────────────────┐
│                  Kubernetes Cluster                     │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │ Krakend     │    │  Keycloak   │    │ Metabase    │  │
│  │ Namespace   │    │  Namespace  │    │ Namespace   │  │
│  │             │    │             │    │             │  │
│  │ ┌─────────┐ │    │ ┌─────────┐ │    │ ┌─────────┐ │  │
│  │ |Krakend  │ │    │ |Keycloak │ │    │ │Metabase │ │  │
│  │ │  Pod    │ │    │ │  Pod    │ │    │ │  Pod    │ │  │
│  │ └─────────┘ │    │ └─────────┘ │    │ └─────────┘ │  │
│  │             │    │             │    │             │  │
│  │ ┌─────────┐ │    │ ┌─────────┐ │    │ ┌─────────┐ │  │
│  │ │Database │ │    │ │Database │ │    │ │Database │ │  │
│  │ │  Pod    │ │    │ │  Pod    │ │    │ │  Pod    │ │  │
│  │ └─────────┘ │    │ └─────────┘ │    │ └─────────┘ │  │
│  │             │    │             │    │             │  │
│  │ ┌─────────┐ │    │ ┌─────────┐ │    │ ┌─────────┐ │  │
│  │ │Ingress  │ │    │ │Ingress  │ │    │ │Ingress  │ │  │
│  │ │         │ │    │ │         │ │    │ │         │ │  │
│  │ └─────────┘ │    │ └─────────┘ │    │ └─────────┘ │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

Before starting, ensure you have the following tools installed:

- [Docker (20.10.x or later)](https://docs.docker.com/engine/install/)
- [kubectl (1.22.x or later)](https://kubernetes.io/docs/tasks/tools/#kubectl)
- [minikube (1.2.x or later)](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)
- [Skaffold (2.0.x or later)](https://skaffold.dev/)
- [Kustomize (4.5.x or later)](https://kustomize.io/)
- [helm (3.x or later)](https://helm.sh/docs/intro/install/)
- Git (2.30.x or later)
- Access to a Kubernetes cluster (local or remote)

## 📁 Project Structure

```
├── .github/                        # CI/CD workflows
|
├── api-gateway
│   ├── krakend
│   │   ├── k8s                     # Base Kubernetes manifests
|   |   |   ├── base/               # Base Kubernetes manifests
|   |   |   └── overlays/           # Environment-specific configurations
|   |   |       ├── development/
|   |   |       ├── staging/
|   |   |       └── production/
│   │   |── Dockerfile.yaml         # Docker configurations
|   |   ├── skaffold.yaml           # Skaffold configuration
│   │   └── README.md               # Documentation
│   ├── other
│   │   ├── k8s
│   │   ├── skaffold.yaml
|   |   ├── skaffold.yaml
│   │   └── README.md
│   └── skaffold.yaml
├── databases
│   ├── cassandra
│   │   ├── k8s
│   │   ├── Dockerfile
|   |   ├── skaffold.yaml
│   │   └── README.md
│   ├── other
│   │   ├── k8s
│   │   ├── Dockerfile
|   |   ├── skaffold.yaml
│   │   └── README.md
│   └── skaffold.yaml
├── other
│   └── skaffold.yaml
├── scripts                       # Utility scripts
├── .editorconfig
├── .gitignore
├── skaffold.yaml                 # Global Skaffold configuration
└── README.md                     # This file
```

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/flexwiz/fw-cnt.git
cd fw-cnt
```

### Setup Environment Variables

Create a `.env` file for each environment in the respective overlays directory of the component that you will run:

```bash
# Example for development environment
cd api-gateway/krakend
cp .env.example overlays/development/.env
# Edit the file with your environment-specific values
```

## 🌐 Environment Setup

### Create a Kubernetes cluster for development

* With `minikube`:

```bash
# Basic kubernetes cluster to to start
minikube start

# Recommended: if you want to deploy many stacks (monitoring, logging, ...)
minikube start --cpus=8 --memory=16
```

### Generate local hosts to use with ingress controller (optional)

Use the provided script to generate hosts to access to your applications from your local host:

```bash
./scripts/generate-hosts.sh <your-k8s-ip> k8s.local
```

This will create the required hosts in the `/etc/hosts`.

## 💻 Development Workflow

### Start Development Environment

Deploy Krakend API Gateway component to your local Kubernetes cluster:

```bash
skaffold dev -p development -m krakend
```

This command will:
- Build the Docker image for Krakend
- Deploy the application to the krakend namespace
- Skaffold port-forward the application port(s) to access from local
- Stream logs from all deployed components
- Watch for file changes and automatically redeploy

To set up port-forwarding with kubectl, you can use this command `kubectl port-forward -n <namespace> svc/<service-name> <local-port>:<target-port>`:

```bash
kubectl port-forward -n krakend svc/<krakend> 9000:8080
```

### Port forward mapping

**Reserved ports:**

- `8080`: Ingress controler web UI
- `8180`: API Gateway
- `8280`: Authentication/authorization provider (Keycloak)
- `8380`: Service mesh web UI

**No specific port used for other tools**

### How to use these components into your custom projects ?

For example, you would like to include Redis in your project. You need to include this sample code into your `skaffold.yaml`:
```yaml
requires:
  - configs: ["redis"]
    git:
      repo: https://github.com/flexwiz/fw-cnt.git
      path: databases/redis/skaffold.yaml
      ref: main
      sync: true
```

## 🚢 Deployment

### Manual Deployment

Deploy to a specific environment using Skaffold:

```bash
# Deploy to development environnement
skaffold run -p development -m [component1],[component2],...

# Deploy to staging
skaffold run -p staging -m [component1],[component2],...

# Deploy to production
skaffold run -p production -m [component1],[component2],...
```

### CI/CD Integration

This repository includes GitHub Actions workflows for automated deployments for each component:

- Push to `develop` branch → Deploy to development environment
- Push to `staging` branch → Deploy to staging environment
- Push to `main` branch → Deploy to production environment

### Scaling

Production environment is configured with Horizontal Pod Autoscaling (HPA) based on CPU and memory usage. You can modify the scaling parameters the dedicated component in `overlays/production/patches/hpa.yaml`.

## 🔒 Security

### Secret Management

- All sensitive information is stored in Kubernetes Secrets
- Secret files are not committed to the repository
- Secret generation scripts are provided for local development
- CI/CD pipelines use GitHub Secrets for deployment

### Network Security

- Network Policies are implemented to restrict pod-to-pod communication
- TLS is enforced for all services
- Proper ingress controllers with security headers are configured

### Container Security

- Containers run as non-root users
- Resource limits are implemented for all pods
- Regular vulnerability scanning is performed on container images

## 🔍 Troubleshooting

See the documentation of the dedicated component inside their directory.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Metabase](https://www.metabase.com/) - The open-source business intelligence tool
- [Kubernetes](https://kubernetes.io/) - Container orchestration
- [Skaffold](https://skaffold.dev/) - Local Kubernetes development
- [Kustomize](https://kustomize.io/) - Kubernetes configuration management
