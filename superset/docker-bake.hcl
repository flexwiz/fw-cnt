# https://docs.docker.com/build/bake/

variable "DEFAULT_TAG" {
  default = "docker.io/flexwiz/superset:4.0.1"
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
  context = "./"
  dockerfile = "./Dockerfile"
}

# docker buildx bake image-dev
target "image-dev" {
  inherits = ["image"]
  dockerfile = "./Dockerfile.dev"
  output = ["type=docker"]
}

target "image-all" {
  inherits = ["image"]
  platforms = [
    "linux/amd64",
    "linux/arm64"
    # "linux/arm/v6",
    # "linux/arm/v7",
    # "linux/386",
    # "linux/ppc64le",
    # "linux/s390x"
  ]
}
