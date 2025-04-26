# Linkerd Kubernetes Deployment Project

This project provides a comprehensive setup for deploying Linkerd service mesh across multiple environments (production, staging, development) using Skaffold, Kustomize, and Sealed Secrets. It also includes sample implementations for integrating KrakenD API gateway and Keycloak authentication with Linkerd.

## Project Structure

```
├── README.md
├── skaffold.yaml
├── base
│   ├── kustomization.yaml
│   ├── linkerd-crds.yaml
│   ├── linkerd-control-plane.yaml
│   ├── linkerd-viz.yaml
│   └── sealed-secrets-controller.yaml
├── environments
│   ├── development
│   │   ├── kustomization.yaml
│   │   ├── patches
│   │   │   ├── linkerd-config-patch.yaml
│   │   │   ├── linkerd-resources-patch.yaml
│   │   │   └── linkerd-viz-patch.yaml
│   │   └── secrets
│   │       └── linkerd-trust-anchor.yaml
│   ├── staging
│   │   ├── kustomization.yaml
│   │   ├── patches
│   │   │   ├── linkerd-config-patch.yaml
│   │   │   ├── linkerd-resources-patch.yaml
│   │   │   └── linkerd-viz-patch.yaml
│   │   └── secrets
│   │       └── linkerd-trust-anchor.yaml
│   └── production
│       ├── kustomization.yaml
│       ├── patches
│       │   ├── linkerd-config-patch.yaml
│       │   ├── linkerd-resources-patch.yaml
│       │   └── linkerd-viz-patch.yaml
│       └── secrets
│           └── linkerd-trust-anchor.yaml
└── samples
    ├── krakend
    │   ├── kustomization.yaml
    │   ├── krakend-config.yaml
    │   └── krakend-deployment.yaml
    └── keycloak
        ├── kustomization.yaml
        ├── keycloak-deployment.yaml
        └── keycloak-config.yaml
```

## Prerequisites

- Kubernetes cluster (v1.25+)
- kubectl (v1.25+)
- Skaffold (v2.8.0+)
- Kustomize (v5.0.0+)
- kubeseal (v0.23.0+)
- helm (v3.12.0+)

## Linkerd Installation Overview

This project deploys Linkerd in a three-step process:

1. Install Linkerd CRDs
2. Deploy Linkerd control plane
3. Deploy Linkerd visualization components

### Core Components

- **Linkerd Control Plane**: Manages the service mesh, including proxies, identity, and traffic management
- **Linkerd Viz**: Provides observability features including dashboard, Prometheus, Grafana
- **Sealed Secrets**: Securely manages sensitive data like certificates

### Environment-Specific Configurations

Each environment (development, staging, production) has its own configuration:

- **Development**: Minimal resource requests, fewer replicas, debug enabled
- **Staging**: Moderate resources, standard replicas, some tracing
- **Production**: High-availability deployment, multiple replicas, optimized resources

## Setup Instructions

### 1. Generate Trust Anchor Certificates

The trust anchor is the root certificate for Linkerd's identity system. Create and seal it for each environment:

```bash
# Generate the trust anchor key and certificate
step certificate create root.linkerd.cluster.local ca.crt ca.key \
  --profile root-ca --no-password --insecure --not-after 87600h

# Create Kubernetes secret
kubectl create secret tls \
  linkerd-trust-anchor \
  --cert=ca.crt \
  --key=ca.key \
  --namespace=linkerd \
  --dry-run=client -o yaml > trust-anchor-secret.yaml

# Seal the secret for each environment
kubeseal --format=yaml < trust-anchor-secret.yaml > environments/development/secrets/linkerd-trust-anchor.yaml
kubeseal --format=yaml < trust-anchor-secret.yaml > environments/staging/secrets/linkerd-trust-anchor.yaml
kubeseal --format=yaml < trust-anchor-secret.yaml > environments/production/secrets/linkerd-trust-anchor.yaml
```

### 2. Deploy with Skaffold

```bash
# Development deployment
skaffold run -p dev

# Staging deployment
skaffold run -p staging

# Production deployment
skaffold run -p production
```

### 3. Verify the Installation

```bash
# Check control plane status
linkerd check

# Verify data plane
linkerd stat deployments -n linkerd
```

## Integrating with Sample Applications

### KrakenD API Gateway

The sample KrakenD deployment is configured to work with Linkerd by:

1. Including the necessary Linkerd annotations
2. Setting up proper service profiles for traffic management
3. Configuring health checking endpoints for Linkerd

To deploy:

```bash
kubectl apply -k samples/krakend
```

### Keycloak Authentication

The sample Keycloak deployment is configured to:

1. Work as an identity provider for applications in the mesh
2. Provide JWT token validation for service-to-service authentication
3. Integrate with Linkerd's mTLS for added security

To deploy:

```bash
kubectl apply -k samples/keycloak
```

## Key Files

### skaffold.yaml

```yaml
apiVersion: skaffold/v4beta5
kind: Config
metadata:
  name: linkerd-deployment
build: {}
profiles:
  - name: dev
    deploy:
      kubectl:
        manifests:
          - environments/development/kustomization.yaml
  - name: staging
    deploy:
      kubectl:
        manifests:
          - environments/staging/kustomization.yaml
  - name: production
    deploy:
      kubectl:
        manifests:
          - environments/production/kustomization.yaml
```

### base/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - linkerd-crds.yaml
  - linkerd-control-plane.yaml
  - linkerd-viz.yaml
  - sealed-secrets-controller.yaml

namespace: linkerd
```

## Best Practices Implemented

1. **Security**:
   - All sensitive data stored as Sealed Secrets
   - mTLS enabled by default
   - Proper RBAC configuration
   - Limited permissions for components

2. **Reliability**:
   - High-availability configurations for production
   - Readiness/liveness probes configured
   - Pod disruption budgets set
   - Resource requests and limits defined

3. **Scalability**:
   - Horizontal pod autoscaling enabled
   - Environment-specific resource configurations
   - Efficient resource usage in non-production environments

4. **Observability**:
   - Prometheus metrics collection
   - Grafana dashboards
   - Distributed tracing with OpenTelemetry
   - Linkerd dashboard deployed

5. **GitOps Ready**:
   - Kustomize based configuration
   - Clear separation of base and environment-specific configs
   - Compatible with CI/CD pipelines
   - Declarative approach

## Troubleshooting

### Common Issues

1. **Certificate Issues**:
   ```bash
   linkerd check --pre
   # Verify certificates are valid and not expired
   ```

2. **Resource Constraints**:
   ```bash
   kubectl describe pods -n linkerd
   # Look for resource-related failures
   ```

3. **Network Policies**:
   ```bash
   kubectl get networkpolicies -A
   # Ensure necessary communication is allowed
   ```

### Debugging Commands

```bash
# Get Linkerd proxy logs
kubectl logs deployment/linkerd-controller -n linkerd -c linkerd-proxy

# Check Linkerd components
linkerd check --proxy

# Debug traffic with tap
linkerd tap deployment/your-app -n your-namespace
```

## Maintenance

### Updating Linkerd

To update Linkerd to a newer version:

1. Update the image tags in the base configuration
2. Apply the changes with Skaffold
3. Monitor the rollout for any issues

```bash
# Monitor rollout
kubectl rollout status deployment/linkerd-controller -n linkerd
```

### Rotating Certificates

Trust anchor certificates should be rotated periodically:

1. Generate new certificates
2. Update the sealed secrets
3. Apply the changes
4. Verify the identity system is working correctly

```bash
linkerd check --identity
```

## References

- [Linkerd Documentation](https://linkerd.io/docs/)
- [Skaffold Documentation](https://skaffold.dev/docs/)
- [Kustomize Documentation](https://kubectl.docs.kubernetes.io/references/kustomize/)
- [Sealed Secrets Documentation](https://github.com/bitnami-labs/sealed-secrets)
