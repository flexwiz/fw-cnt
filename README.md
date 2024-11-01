# Common Tools

## Prerequisites

To be able to use these `common-tools` with minikube, k3d, kind or another Kubernetes tools, you need to install the following tools:

- kubectl

```bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/`kubectl version --client --short`/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```

- minikube

```bash
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && chmod +x minikube \
  && sudo mv minikube /usr/local/bin/
```

- skaffold

```bash
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 \
  && chmod +x skaffold \
  && sudo mv skaffold /usr/local/bin/
```

- helm

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

## How to use skaffold ?

First you will need to start `minikube`:

```bash
minikube start --cpus=max --memory=max
```

You can use `common-tools` in two ways :

- Clone the repository & launch your favorite skaffold command

```bash
skaffold run --port-forward=user                      # Run all skaffold modules defined in skaffold.yaml + port-forward
skaffold run --port-forward=user -m postgres           # Run postgres module + port-forward postgres
skaffold run --port-forward=user -m postgres,redis  # Run postgres & redis module + port-forward postgres & redis
```

- Reference this repository from another one (ex: `api-gateway`, `ms-immo`), using the `requires` section in your `skaffold.yaml`

```yaml
requires:
  - configs: ["common-tools"]
    git:
      repo: git@github.com:ntdtfr/common-tools.git
```