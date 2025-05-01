# Sealed Secrets

## 📋 Prerequisites

Before starting, ensure you have installed all tools mentioned in the [main documentation](../../README.md#-prerequisites) of this repository.

## 🚀 Getting start

### 1. deploy the Sealed Secrets controller

```bash
# Deploy to local environnement development
skaffold run -p local -m sealed-secrets

# Deploy to development environnement
skaffold run -p development -m sealed-secrets

# Deploy to staging
skaffold run -p staging -m sealed-secrets

# Deploy to production
skaffold run -p production -m sealed-secrets
``` 

It will deploy Sealed Secrets to your Kubernetes cluster in the `fw-security` namespace.

### 2. Encrypt your Kubernetes secrets with the [Kubeseal](https://github.com/bitnami-labs/sealed-secrets) tools

Use the following command to generate a sealed secrets file (`my-sealed-secret.yaml`) from an existing secret file (e.g: `my-secret.yaml`):

```bash
# With existing secrets template (mysecret.yaml)
kubeseal --controller-name sealed-secrets --controller-namespace fw-security -f mysecret.yaml -w my-sealed-secrets.yaml

# or without template
kubectl create secret generic my-secrets \
  --from-literal=username=YOUR_USERNAME \
  --from-literal=password=YOUR_PASSWORD \
  --dry-run=client -o yaml | \
  kubeseal --controller-name sealed-secrets --controller-namespace fw-security --format yaml > my-sealed-secrets.yaml
```

For example, to generate a sealed secrets file for my postgresql-secrets.yaml file:

```yaml
# postgresql-secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgresql-secrets
  namespace: fw-data
  labels:
    flexwiz.io/tier: storage
    flexwiz.io/type: database
    flexwiz.io/app: postgresql
    flexwiz.io/env: development
data:
  username: cG9zdGdyZXM=
  password: cGFzc3dvcmQ=
type: Opaque
```

```bash
kubeseal --controller-name sealed-secrets --controller-namespace fw-security -f postgres-secrets.yaml -w sealed-secrets.yaml

```

The result look like that:

```yaml
# sealed-secret.yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  creationTimestamp: null
  name: postgresql-secrets
  namespace: fw-data
spec:
  encryptedData:
    password: AgAJoIZN1Q6PJfh+61M8FFkzNdLEt9SWBPRuCBJI8jLuV2rbj+Nk2YEPK15SVxqsuqf/O7Jzy4OgNDm0WJxrCkyPHbvfoLsjC7KZzqgrh0Gh0IiQlg+skfb24vCPM/L7wM8pPIOQwNRSWSrtmPnKm1fJ/fTmBq23KQeBmKjWmtPKXmBN32PLaRvDSrCI+4yGFn4PlvPjcg61crbId3p6dvS6LGzDYcm1hYoi51wPoz1tPD9q19+RV5ARb11z1Yjl8h0JJI5vANVqaIZPYT+eD4nKVNE/dgaGktlX/8BbTFqD0s/5P2FJ71kemliE+1QZyzmjV7PbPhz5VOxHh2TrSnKKz6h8FDz0dXbn+apph90rkulJgjkN5xnufCdpoLXuIkjFVQCqUCnfEPAN/rMLk7OHZ7jkZbPptEiOM0DgBHzyI2qX+jDsCFIa3yQwyADNzIIJhfr4blb3Syd8958qzLVDhPWGAU6vtMDKiZjl2CK3QGhiwlrp2RrT40BngUyLnYCpXXtOcdkRSEaViv33NOmaaK50TNbkF1PHaBPcuFefpFaH1ITgNzakO67M+5kh62eyEc97wvLfZi56s7hInxf59MdpRAuoQEBbU+mTA8Hp6aIbBdr5KzUO3guZXT+ZPBUzdOhM0euQ5lkQ7y7QPjEjSxyAbiPIkDUX41Yqod78zG0CR8ZX2JAFjanZg5Wao+kBo24H74Y6TQ==
    username: AgA75KYHTXa88QenrIgGC+iuDPmnyMdbP6OQqmiEKZD7i9EL2uZK06kBEibYlh8gMIKH4dce087kXqSLCMaLUxvDxJaDCw2RBZKCE5ehxbN6VHReYFHLk1igH3y6AInAyvEvrnh+27RoZJeTnwfXluO83fNPJKVYw7lPiSIs2ubwXuhfIV2k3K14pyUj5sJ3uAaa+OoXvQP/QRi0P/2itFqIKILKj4l1eLcPhiecL5kBulJT/+b6b38A2uVO0qJI7Qx9S4T4MwQAj77zqHiA6p/PPrtaAaSSWaqd8+twf5A8WrsBz2MxfuSG/AZKYwp0jOl715XM9Pydv9WQ0NUej2nJWXwwoGdhtjqAuzwLhx/Gh+a0xHJJAX7jRdLbDvX5Lh3TBobZ//hQb3lgO0xylOvuc3PEgZIY81w4P1BcGL0tUa4SB9lxKIfd6SN3QVprXD8tFcxC9xhMsS6Bac8Q/zAlk4tquj/k3S3u2mhhXPnnCmcN7hIxbzglfRwindIquwCX3GDJDsxSPLG41nE5ZxwRaY9cn8QZoWEKo/KK0+r6i9PJxicrSEB68fgCb46+dajcLM9mogx7IBRpk2P8+rBRppWacWO7t+4qZBFiGrN3k1Kh7eugNFR4wU0XG7yZBncccVTy9oWV4YTXzrqWEO+O6DNwBKF1iYYWRTe9Xey8t8NgBY7+qFOnNkLPpqFYDOy+vWPeYwO29w==
  template:
    metadata:
      creationTimestamp: null
      labels:
        flexwiz.io/tier: storage
        flexwiz.io/type: database
        flexwiz.io/app: postgresql
        flexwiz.io/env: development
      name: postgresql-secrets
      namespace: fw-data
    type: Opaque
```

## Documentation

- [Sealed Secrets Github repository](https://github.com/bitnami-labs/sealed-secrets) 
- [Bitnami Helm Chart](https://artifacthub.io/packages/helm/bitnami/sealed-secrets)
