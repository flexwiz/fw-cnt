# MongoDB

This directory contains Kubernetes manifests for deploying MongoDB across multiple environments (production, staging, development) using Skaffold, Kustomize, and Sealed Secrets following best practices.

## Project Structure

```
.
├── k8s
│   ├── base
│   │   ├── configmap.yaml
│   │   ├── kustomization.yaml
│   │   ├── namespace.yaml
│   │   ├── pvc.yaml
│   │   ├── service-account.yaml
│   │   ├── service.yaml
│   │   └── statefulset.yaml
│   └── overlays
│       ├── development
│       │   ├── kustomization.yaml
│       │   ├── patches
│       │   │   ├── pvc.yaml
│       │   │   └── statefulset.yaml
│       │   └── sealed-secrets.yaml
│       ├── production
│       │   ├── kustomization.yaml
│       │   ├── patches
│       │   │   ├── pvc.yaml
│       │   │   └── statefulset.yaml
│       │   ├── pdb.yaml
│       │   └── sealed-secrets.yaml
│       └── staging
│           ├── kustomization.yaml
│           ├── patches
│           │   ├── pvc.yaml
│           │   └── statefulset.yaml
│           ├── pdb.yaml
│           └── sealed-secrets.yaml
├── README.md
├── secrets
└── skaffold.yaml
```

## Prerequisites

Before starting, ensure you have installed all tools mentioned in the [main documentation](../../README.md#-prerequisites) of this repository.

## 🚀 Getting start

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

### Manual Deployment

You can also deploy using kubectl and kustomize directly:

```bash
# Deploy to development
kubectl apply -k overlays/development/

# Deploy to staging
kubectl apply -k overlays/staging/

# Deploy to production
kubectl apply -k overlays/production/
```

## Security Considerations

- MongoDB runs with a non-root user
- Network policies limit access to the database
- Credentials are stored as Sealed Secrets
- RBAC policies restrict pod permissions

## Monitoring and Logging

- Resource requests and limits are defined for each environment
- Ready for integration with Prometheus monitoring
- Structured logging configured

## Best Practices Implemented

1. StatefulSet for stable network identities
2. Proper resource requests and limits
3. Environment-specific configurations
4. Encrypted secrets management
5. High availability in production
6. Pod disruption budgets for controlled maintenance
7. Readiness and liveness probes
8. Anti-affinity rules for high availability
