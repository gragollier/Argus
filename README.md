# Argus
From the Greek `Argus Panoptes`, Argus is the monitoring service for my homelab. It monitors hosts and alerts me of changes using Slack. As of now, this only monitors and reports issues, it does not store logs.

## Setup
All configuration lives in the `config.yaml` file. You can see the included example, `config.example.yaml` for help.

## Deployment
### Automatic
By default, Argus is deployed to the Kubernetes cluster on pushes to Gitlab. Gitlab will build the image, push it to Harbor then deploy it to Kubernetes.

### Manual
Argus can also be deployed manually as a docker image. Simply build the provided docker image and run it.
```shell
$ docker build -t argus:latest .
$ docker run argus:latest
```

## Modules
- HostMonitor
    - Basic power state monitoring using IPMI