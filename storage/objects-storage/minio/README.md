# Minio

## Key features

### Bucket initialization job

- Created a separate Kubernetes Job that runs after MinIO deployment
- Uses minio/mc (MinIO Client) container to create and configure buckets
- Waits for MinIO service to be available before attempting bucket creation

For each bucket:

- Creates the bucket if it doesn't exist (mc mb ...)
- Sets appropriate bucket policies (mc policy set ...)
- Avoids recreating buckets that already exist

Environment-specific configuration:

- Added the ability to have environment-specific bucket settings
- Production environment includes lifecycle policies and an additional "backups" bucket
- Uses Kustomize patches to apply environment-specific settings


### Backup implementation

CronJobs will automatically back up all MinIO buckets to both AWS S3 and Google Cloud Storage. Here's what these configurations provide:

Dual cloud provider backup strategy:

- AWS S3 backup runs at 1:00 AM
- Google Cloud Storage backup runs at 3:00 AM
- Both use the MinIO Client (mc) for efficient synchronization

Environment-specific backup frequencies:

- **Development**: Weekly backups on Mondays
- **Staging**: Twice weekly backups (Monday and Thursday)
- **Production**: Daily backups with versioning preservation


## Environment configuration

### Development:

- Smaller storage (5Gi)
- NGINX ingress controller
- Staging TLS certificates
- Local port forwarding

### Staging:

- Medium storage (50Gi)
- Traefik ingress controller
- Production TLS certificates
- SSD storage class

### Production:

- Large storage (500Gi)
- Increased resource limits
- Node affinity for dedicated storage nodes
- Security context configuration
- SSD redundant storage class

## 📋 Prerequisites

Before starting, ensure you have installed all tools mentioned in the [main documentation](../../README.md#-prerequisites) of this repository.

## 🚀 Getting start

### 1. Create sealed secrets for all environments (development, staging and production) 

Use this manifest (`secrets/.secrets.yaml.example`) to create the sealed secrets for each environment:

- Minio credentials
- AWS credentials
- GCS credentials


```bash
# Go to the secrets directory
cd secrets

# Create a `.secrets.yaml.<environment>` file for the environment (example: dev)
cp .secrets.yaml.example .secrets.yaml.dev

```
Configure the data secrets for the development environment:
```yaml
# .secrets.yaml.dev
# This is a template, will be replaced by sealed-secrets in each environment
apiVersion: v1
kind: Secret
metadata:
  name: minio-secrets
  namespace: fw-middleware
  labels:
    flexwiz.io/tier: storage
    flexwiz.io/type: object-storage
    flexwiz.io/app: minio
    flexwiz.io/env: local
type: Opaque
data:
  username: YWRtaW4=      # base64 encoded admin
  password: cGFzc3dvcmQ=  # base64 encoded password
```

Generate the sealed secrets with [kubeseal](../../security/sealed-secrets/README.md#-getting-start):

```bash
# Generate sealed secrets for development environment
kubeseal --controller-name sealed-secrets --controller-namespace kube-system -f .secrets.yaml.dev -w sealed-secrets.yaml && mv sealed-secrets.yaml ../k8s/overlays/development
```

### 2. Deploy Minio with Skaffold to a specific environment

Please refer to the [main documentation](../../README.md) for more details about deployment with Skaffold.

> Note: The `development` environment is used in this example.

Run the following Skaffold command to deploy Minio:
```bash
skaffold run -p development -m minio
```

### 3. Monitor Backups

```bash
# Check the status of cronjobs
kubectl get cronjobs -n fw-middleware

# Check logs from the most recent backup job
kubectl logs -n fw-middleware job/minio-aws-backup-<timestamp>
kubectl logs -n fw-middleware job/minio-gcs-backup-<timestamp>
```

### 4. Manual Backup Trigger

```bash
# Create a job from the cronjob
kubectl create job --from=cronjob/minio-aws-backup minio-aws-manual-backup -n fw-middleware
```

## Documentation
- 
