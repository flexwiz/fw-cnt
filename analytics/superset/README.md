# superset
A custom Superset project for analytics and data visualizations

## Convert Superset Helm chart to Kubernetes YAML (optional)

If the Kubernetes YAML manifest are not exist, use the `helm template` command to convert the superset Helm chart to a YAML manifests.

```bash
helm repo add superset https://apache.github.io/superset
helm template superset superset/superset --output-dir ./k8s/superset
```

## How to build the docker image on local ?

```bash
docker buildx bake image-dev
```

## How to run Superset ?

```bash
skaffold dev
```