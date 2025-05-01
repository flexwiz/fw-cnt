# PostgreSQL

## 📋 Prerequisites

Before starting, ensure you have installed all tools mentioned in the [main documentation](../../README.md#-prerequisites) of this repository.

## 🚀 Getting start

### Step 1: deploy the Sealed Secrets controller

## https://hub.docker.com/_/postgres

 https://artifacthub.io/packages/helm/bitnami/postgresql-ha/12.6.0

## How to create sealed secrets for PostgrSQL ?

Use this manifest (`secrets/.secrets.yaml.example`) to create the sealed secrets for each environment.


```bash
# Go to the secrets directory
cd secrets

# Create a `.secrets.yaml.<environment>` file for the environment (example: dev)
cp .secrets.yaml.example .secrets.yaml.dev

```
Configure the data secrets for the development environment:
```yaml
# .secrets.yaml.dev
apiVersion: v1
kind: Secret
metadata:
  name: postgresql-secrets
  namespace: fw-data
  labels:
    flexwiz.io/tier: storage
    flexwiz.io/type: database
    flexwiz.io/app: postgresql
type: Opaque
data:
  database: cG9zdGdyZXM= # base64 encoded "postgres"
  username: cG9zdGdyZXM= # base64 encoded "postgres"
  password: cGFzc3dvcmQ= # base64 encoded "password"
```

Generate the sealed secrets with [kubeseal](../../security/sealed-secrets/README.md#-getting-start):

```
# Generate sealed secrets for development environment
kubeseal --controller-name sealed-secrets --controller-namespace kube-system -f .secrets.yaml.dev -w sealed-secrets.yaml && mv sealed-secrets.yaml ../k8s/overlays/development
```


## Documentation

- [Sealed Secrets Github repository](https://github.com/bitnami-labs/sealed-secrets) 
- [Bitnami Helm Chart](https://artifacthub.io/packages/helm/bitnami/sealed-secrets)
