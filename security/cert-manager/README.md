# Cert-Manager

This module contains Kubernetes manifests for deploying cert-manager across multiple environments (development, staging, production) using Skaffold and Kustomize.

## Overview

[Cert-Manager](https://cert-manager.io/) is a Kubernetes add-on that automates the management and issuance of TLS certificates. This module uses the latest version and follows security best practices:

- Runs with restricted Pod Security Context
- Uses NetworkPolicies to limit traffic
- Resource limits and requests properly configured
- RBAC with least privilege principle

## Project Structure

```
.

```

## Prerequisites

Before starting, ensure you have installed all tools mentioned in the [main documentation](../../README.md#-prerequisites) of this repository.

## 🚀 Getting start

### Initial Setup

1. Read the setup step from the [main documentation](../../README.md#setup-environment-variables) of this repository
2. [Setup Sealed Secrets controller](../sealed-secrets/README.md#-getting-start) in your cluster (if not already installed)

### Deploy using Skaffold

To deploy Cert-Manager to the development environment:

```bash
skaffold run -p development
```

For staging:

```bash
skaffold run -p staging
```

For production:

```bash
skaffold run -p production
```

### Manual Deployment with Kustomize

To deploy each component manually using Kustomize:

```bash
# For development environment
kubectl apply -k overlays/development/

# For staging environment  
kubectl apply -k overlays/staging/

# For production environment
kubectl apply -k overlays/production/
```

## Customization

### Environment-Specific Configurations

Each environment (development, staging, production) has its own overlay with customized configurations:

- **Development**: Minimal resources, in-memory databases, debug mode enabled
- **Staging**: Moderate resources, persistent storage, similar to production but with non-critical monitoring
- **Production**: High availability, robust monitoring, auto-scaling, strict security policies

### Custom Certificate Issuers

To create a custom certificate issuer (e.g., for Let's Encrypt), create a ClusterIssuer or Issuer resource:

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

## Security Best Practices

This deployment follows these security best practices:

1. **Least Privilege Principle**: RBAC roles with minimal required permissions
2. **Network Policies**: Traffic limited to only necessary communications
3. **Pod Security**: Non-root users, read-only file systems, dropped capabilities
4. **Resource Quotas**: Prevents resource exhaustion attacks
5. **Secret Management**: Properly secured with appropriate RBAC
6. **mTLS**: All service-to-service communication is encrypted via Linkerd
7. **Regular Updates**: Using the latest stable versions of all components

## Maintenance

### Version Updates

To update cert-manager to a newer version:

1. Update the version in `base/deployment.yaml`
2. Run the appropriate Skaffold profile

### Troubleshooting

Common issues and solutions:

- **Certificate issuance failures**: Check cert-manager logs: `kubectl logs -n cert-manager -l app=cert-manager`
- **Authentication issues**: Check Keycloak logs: `kubectl logs -n keycloak -l app=keycloak`
- **API Gateway errors**: Check Krakend logs: `kubectl logs -n krakend -l app=krakend`

