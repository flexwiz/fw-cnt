# https://docs.docker.com/build/bake/

variable "DEFAULT_TAG" {
  # default = "docker.io/ntdtfr/keycloak:latest"
  default = "keycloak:latest"
}

// Special target: https://github.com/docker/metadata-action#bake-definition
target "docker-metadata-action" {
  tags = ["${DEFAULT_TAG}"]
}

// Default target if none specified
group "default" {
  targets = ["image-dev"]
}

target "image" {
  inherits = ["docker-metadata-action"]
  context = "."
  dockerfile = "./keycloak/Dockerfile"  // Path to your Dockerfile
}

target "image-dev" {
  inherits = ["image"]
  dockerfile = "./keycloak/Dockerfile.dev"  // Path to your Dockerfile
  output = ["type=docker"]
}

target "image-all" {
  inherits = ["image"]
  platforms = [
    "linux/amd64",
    "linux/arm/v6",
    "linux/arm/v7",
    "linux/arm64"
    # "linux/386",
    # "linux/ppc64le",
    # "linux/s390x"
  ]
}