# AGENTS

## Google Cloud CLI setup

Date: 2026-03-19

## GitHub CLI API token

For connecting to the GH CLI API, use the token from:

```bash
/opt/stacks/hosts.yml
```

## Git repository connection

Repository initialized locally on 2026-03-19 in:

```bash
/opt/stacks/qubitmdm
```

Remote configured:

```bash
origin git@github.com:avrcanio/qubitmdm.git
```

Connectivity check:

- `git ls-remote --heads origin` executed successfully.
- No remote heads were returned at that time (possible empty remote or no pushed branches).

### 1) Installed Google Cloud SDK
Command executed:

```bash
curl https://sdk.cloud.google.com | bash
```

Installation completed successfully.

Install location:

```bash
/root/google-cloud-sdk
```

Verified version:

- Google Cloud SDK 561.0.0
- bq 2.1.29
- bundled-python3-unix 3.13.10
- core 2026.03.13
- gcloud-crc32c 1.0.0
- gsutil 5.36

### 2) Installed Cloud Code related components
Command executed:

```bash
gcloud components install alpha beta skaffold minikube kubectl gke-gcloud-auth-plugin
```

Installed components:

- alpha
- beta
- skaffold
- minikube
- kubectl
- gke-gcloud-auth-plugin

### 3) Version checks
Verified binaries and versions:

- kubectl: v1.34.5-dispatcher
- minikube: v1.38.1
- skaffold: v2.17.3
- gke-gcloud-auth-plugin: Kubernetes v1.34.2+0dd7f7cd0b632699e47ecafa4acc8f77cfc73c06

### 4) Optional shell setup
To add gcloud to PATH and enable completion:

```bash
source /root/google-cloud-sdk/path.bash.inc
source /root/google-cloud-sdk/completion.bash.inc
```
