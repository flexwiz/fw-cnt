// docker-bake.hcl
// https://docs.docker.com/build/bake/
variable "TAG" {
  default = "latest"
}

variable "REGISTRY" {
  default = "docker.io"
}

variable "REPOSITORY" {
  default = "ntdtfr/keycloak"
}

// Base target for shared configuration
// Special target: https://github.com/docker/metadata-action#bake-definition
target "docker-metadata-action" {}

// Base target with common build configuration
target "base" {
  context = "."
  dockerfile = "Dockerfile"
  platforms = ["linux/amd64", "linux/arm64"]
  labels = {
    org.opencontainers.image.title=Keycloak
    org.opencontainers.image.description=Keycloak component
    org.opencontainers.image.vendor=ntdt
  }
}

// Development target
target "development" {
  inherits = ["base"]
  target = "development"
  tags = ["${REGISTRY}/${REPOSITORY}:dev"]
}

// Production target
target "production" {
  inherits = ["base", "docker-metadata-action"]
  target = "production"
}

// Test target for CI
target "test" {
  inherits = ["base"]
  target = "test"
  output = ["type=cacheonly"]
}
