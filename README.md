# Common Tools

[![Keycloak CI](https://github.com/ntdtfr/tools/actions/workflows/keycloak-ci.yml/badge.svg)](https://github.com/ntdtfr/tools/actions/workflows/keycloak-ci.yml)
[![Superset CI](https://github.com/ntdtfr/tools/actions/workflows/superset-ci.yml/badge.svg)](https://github.com/ntdtfr/tools/actions/workflows/superset-ci.yml)
[![Security Scanning](https://github.com/ntdtfr/tools/actions/workflows/security-scan.yml/badge.svg)](https://github.com/ntdtfr/tools/actions/workflows/security-scan.yml)

## Prerequisites

To be able to use these common `tools` with minikube, k3d, kind or another Kubernetes tools, you need to install the following tools:

- [kubectl]()
- [minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)
- [skaffold](https://skaffold.dev/docs/install/)
- [helm](https://helm.sh/docs/intro/install/)
- [kustomize](https://kubectl.docs.kubernetes.io/installation/kustomize/)

## How to use skaffold ?

### First you will need to start `minikube`:

```bash
# Basic kubernetes cluster to to start
minikube start

# Recommended: if you want to deploy many stacks (monitoring, logging, ...)
minikube start --cpus=8 --memory=16
```

### Clone the repository and deploy your favorite middleware tools stack

```bash
# Clone with HTTPS
git clone https://github.com/ntdtfr/tools.git && cd tools

# or 

# Clone with SSH
git clone git@github.com:ntdtfr/tools.git && cd tools

# Deploy PostgreSQL tool
skaffold run -p minikube -m postgres

# Deploy PostgreSQL and Redis tools
skaffold run -p minikube -m postgres,redis
```

### How to deploy these tools into your custom projects ?

For example, you would like to include Redis in your project. You need to include this sample code into your `skaffold.yaml`:
```yaml
  - configs: ["redis"]
    git:
      repo: https://github.com/ntdtfr/tools.git
      path: databases/redis/skaffold.yaml
      ref: main
      sync: true
    activeProfiles:
      - name: minikube
        activatedBy: [minikube]
```

## Port forward mapping

**Reserved ports:**

- `8080`: Ingress controler web UI
- `8180`: API Gateway
- `8280`: Authentication/authorization provider (Keycloak)
- `8380`: Service mesh web UI

**No specific port used for other tools**
