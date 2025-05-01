# Metabase

## 📋 Prerequisites

Before starting, ensure you have installed all tools mentioned in the [main documentation](../../README.md#-prerequisites) of this repository.

## 🚀 Getting start

## Step 1: Create sealed secrets for all environments (development, staging and production) 

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
  name: metabase-secrets
  namespace: wf-analytics
  labels:
    flexwiz.io/tier: analytics
    flexwiz.io/type: business-intelligence
    flexwiz.io/app: metabase
type: Opaque
data:
  database: bWV0YWJhc2U= # base64 encoded "metabase"
  username: bWV0YWJhc2U= # base64 encoded "metabase"
  password: cGFzc3dvcmQ= # base64 encoded "password"
```

Generate the sealed secrets with [kubeseal](../../security/sealed-secrets/README.md#-getting-start):

```bash
# Generate sealed secrets for development environment
kubeseal --controller-name sealed-secrets --controller-namespace kube-system -f .secrets.yaml.dev -w sealed-secrets.yaml && mv sealed-secrets.yaml ../k8s/overlays/development
```

## Step 2: Deploy Metabase with Skaffold to a specific environment

Please refer to the [main documentation](../../README.md) for more details about deployment with Skaffold.

> Note: The `development` environment is used in this example.

Metabase use PostgreSQL as database, you need to deploy it first:
```bash
skaffold run -p development -m postgresql
```

Then you can deploy metabase:
```bash
skaffold run -p development -m metabase
```

## Documentation
- [Metabase offical website](https://www.metabase.com)
- [Metabase documentation](https://www.metabase.com/docs/latest)
