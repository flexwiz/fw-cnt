# Traefik v3.3.5 (Ingress Controller)

This directory contains configurations to deploy Traefik as an ingress controller across production, staging, and development environments using Skaffold, Kustomize, and Sealed Secrets.

## Project Structure

```
.
├── k8s
│   ├── base
│   │   ├── configmap.yaml
│   │   ├── crds.yaml
│   │   ├── deployment.yaml
│   │   ├── kustomization.yaml
│   │   ├── namespace.yaml
│   │   ├── rbac.yaml
│   │   └── service.yaml
│   └── overlays
│       ├── development
│       │   ├── kustomization.yaml
│       │   └── patches
│       │       ├── configmap.yaml
│       │       └── deployment.yaml
│       ├── production
│       │   ├── kustomization.yaml
│       │   ├── network-policy.yaml
│       │   └── patches
│       │       ├── configmap.yaml
│       │       └── deployment.yaml
│       └── staging
│           ├── kustomization.yaml
│           └── patches
│               ├── configmap.yaml
│               └── deployment.yaml
├── README.md
├── secrets
└── skaffold.yml
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

## Environment configurations

### Base Configuration

The base configuration contains common elements shared across all environments:
- RBAC configurations for Traefik
- Core deployment settings
- Common CRDs
- Basic Traefik configuration

### Development environment

- Single replica
- Minimal resource requirements
- Simplified configuration
- Debug logging enabled
- No TLS enforcement

### Staging environment

- 2 replicas for redundancy
- Moderate resource allocations
- TLS enabled
- Test metrics
- Standard logging

### Production environment

- High availability with 3 replicas
- Resource limits optimized for production traffic
- Strict TLS settings
- Metrics enabled for monitoring
- Extended logging
- Rate limiting


## Monitoring and Maintenance

### Accessing Traefik Dashboard

The Traefik dashboard is available at:
- Production: https://traefik.flexwiz.io/dashboard/ (IP restricted)
- Staging: https://traefik.staging.flexwiz.io/dashboard/
- Development: http://traefik.dev.flexwiz.io/dashboard/

### Health Checks

Check Traefik health status:

```
kubectl get pods -n fw-middleware
kubectl logs -n fw-middleware -l flexwiz.io/app=traefik
```

### Updating Configurations

1. Modify the appropriate files in the base or overlay directories
2. Deploy using Skaffold:
   ```
   skaffold run -p <environment>
   ```

## Best Practices Implemented

1. **Security**:
   - RBAC with minimal permissions
   - Encrypted secrets using Sealed Secrets
   - Secure TLS configurations
   - Network policies to restrict traffic

2. **Scalability**:
   - Horizontal pod autoscaling
   - Environment-specific resource allocations
   - Configuration for high traffic in production

3. **Maintainability**:
   - Kustomize for DRY configurations
   - Clear separation of environment-specific settings
   - Skaffold for consistent deployments

4. **Reliability**:
   - Health checks and readiness probes
   - Multiple replicas in production and staging
   - Graceful shutdown configurations

5. **Observability**:
   - Prometheus metrics integration
   - Structured logging
   - Dashboard access for monitoring

## Troubleshooting

### Common Issues

1. **Certificate Issues**:
   - Check if the SealedSecret was properly created
   - Verify the Sealed Secrets controller is running
   - Ensure the certificate is valid for your domain

2. **Connection Refused**:
   - Check if Traefik pods are running
   - Verify service endpoints are correctly configured
   - Check network policies

3. **Resource Constraints**:
   - Monitor resource usage with `kubectl top pods -n fw-middleware`
   - Adjust resource limits in the respective environment overlays

4. **Configuration Errors**:
   - Check Traefik logs: `kubectl logs -n fw-middleware -l flexwiz.io/app=traefik`
   - Validate CRD configurations
   - Test configuration with `skaffold render -p <environment>`
