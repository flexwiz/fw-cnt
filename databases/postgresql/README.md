# PostgreSQL

## 📋 Prerequisites

Before starting, ensure you have installed all tools mentioned in the [main documentation](../../README.md#-prerequisites) of this repository.

## 🚀 Getting start

### Step 1: deploy the Sealed Secrets controller

## https://hub.docker.com/_/postgres

 https://artifacthub.io/packages/helm/bitnami/postgresql-ha/12.6.0

## How to create sealed secrets for PostgrSQL ?

Use this manifest (secrets.yaml) to create sealed secrets for each environment:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgresql-secrets
  namespace: databases
  labels:
    flexwiz.io/tier: middleware
    flexwiz.io/type: security
    flexwiz.io/app: postgresql
type: Opaque
data:
  username: cG9zdGdyZXM= # base64 encoded "postgres"
  password: cGFzc3dvcmQ= # base64 encoded "password"
```

```
kubeseal --controller-name sealed-secrets --controller-namespace kube-system -f secrets.yaml -w sealed-secrets.yaml
```


## Documentation

- [Sealed Secrets Github repository](https://github.com/bitnami-labs/sealed-secrets) 
- [Bitnami Helm Chart](https://artifacthub.io/packages/helm/bitnami/sealed-secrets)
