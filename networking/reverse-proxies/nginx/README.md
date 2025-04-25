# Nginx Ingress Controller

This directory contains Kubernetes manifests for deploying the Nginx Ingress Controller across multiple environments (development, staging, production) using Skaffold, Kustomize, and Sealed Secrets.

## Project Structure

```
.
├── k8s
│   ├── base
│   │   ├── configmap.yaml
│   │   ├── deployment.yaml
│   │   ├── kustomization.yaml
│   │   ├── namespace.yaml
│   │   ├── rbac.yaml
│   │   └── service.yaml
│   └── overlays
│       ├── development
│       │   ├── kustomization.yaml
│       │   └── patches
│       │       ├── deployment.yaml
│       │       └── service.yaml
│       ├── production
│       │   ├── hpa.yaml
│       │   ├── kustomization.yaml
│       │   └── patches
│       │       └── deployment.yaml
│       └── staging
│           ├── kustomization.yaml
│           └── patches
│               └── deployment.yaml
├── README.md
├── secrets
└── skaffold.yml
```

## Prerequisites

Before starting, ensure you have installed all tools mentioned in the [main documentation](../../README.md#-prerequisites) of this repository.

## 🚀 Getting start

## Setup Instructions

### 1. Initial Setup

1. Read the setup step from the [main documentation](../../../README.md#setup-environment-variables) of this repository
2. [Setup Sealed Secrets controller](../../../security/sealed-secrets/README.md#-getting-start) in your cluster (if not already installed)

### 2. Creating Sealed Secrets

To create a sealed secret for TLS certificates:

1. Create a regular Kubernetes Secret:
   ```bash
   kubectl create secret tls traefik-tls --cert=path/to/tls.crt --key=path/to/tls.key --dry-run=client -o yaml > secrets/.secret.yaml
   ```

2. Seal the secret using kubeseal:
   ```bash
   kubeseal --controller-name=sealed-secrets --controller-namespace=kube-system -o yaml < secrets/.secret.yaml > sealed-tls-cert.yaml
   ```

3. Place the generated `sealed-tls-cert.yaml` in the appropriate environment directory under `overlays/`.

### 3. Deploying with Skaffold

To deploy to a specific environment:

```bash
skaffold run -p development  # Or staging, production
```

To develop with continuous deployment:

```bash
skaffold dev -p development
```

## Environment configurations

### Development environment
- Single replica deployment
- Resource limits set low
- Debug logging enabled

### Staging environment
- Two replicas deployment
- Moderate resource limits
- Standard logging

### Production environment
- Auto-scaling with HPA (3-10 replicas)
- High resource limits and requests
- Strict security settings
- Higher connection limits

## Maintenance

### Upgrading Nginx Ingress

To upgrade the Nginx ingress controller:

1. Update the image version in `base/deployment.yaml`
2. Apply changes using Skaffold or Kustomize

## Troubleshooting

### Common Issues

1. **TLS Certificate Issues**: Check sealed secrets and certificate validity
2. **Resource Constraints**: Verify resource requests and limits
3. **Connection Issues**: Check Nginx configuration in ConfigMap

## Security Best Practices

- All sensitive information is managed via Sealed Secrets
- RBAC strictly limits permissions
- Network policies restrict traffic
- Regular updates to container images
