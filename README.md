```markdown

# Cloud Native Python Application Deployment on Amazon EKS with Monitoring

This project demonstrates the end-to-end deployment of a Python microservice on Amazon EKS (Elastic Kubernetes Service). Infrastructure is provisioned using Terraform, deployments are managed by ArgoCD and Helm, and CI/CD is automated with GitHub Actions. Monitoring is provided by Prometheus and Grafana.


## Project Structure

```
pwc-task/
├── .github/
│   └── workflows/
│       ├── terraform.yml
│       ├── docker.yml
│       └── helm-update.yml
├── manifests/
│   ├── argocd/
│   │   ├── project.yaml
│   │   └── application.yaml
│   ├── helm/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates.yaml
│   └── monitoring/
│       ├── prometheus-application.yaml
│       └── grafana-application.yaml
├── terraform/
│   ├── main.tf
│   └── backend.tf
├── src/
│   ├── Dockerfile
│   └── (your python app files)
├── README.md
└── ...
```


## Prerequisites

*   [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
*   [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
*   [Docker](https://docs.docker.com/get-docker/)
*   [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
*   [Helm](https://helm.sh/docs/intro/install/)
*   A [GitHub](https://github.com/) account
*   An [AWS ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html) repository


## Steps to Deploy

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd pwc-task
```


### 2. Provision the Infrastructure using Terraform

Terraform will provision:
- EKS cluster
- Route 53 hosted zone for `pwc-task.com`
- ACM certificate for `pwc-task.com`, `prometheus.pwc-task.com`, and `grafana.pwc-task.com`

Initialize and apply the Terraform configuration:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### 3. Configure GitHub Secrets

For the CI/CD pipeline to work, add the following secrets to your GitHub repository:

*   `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: Your AWS credentials
*   `ECR_REPO`: Your ECR repository URL (e.g., <aws_account_id>.dkr.ecr.<region>.amazonaws.com/python-app)


### 4. Application Deployment with ArgoCD and Helm

ArgoCD manages deployments using manifests in `manifests/argocd/` and Helm chart in `manifests/helm/`.
Your Python app, Prometheus, and Grafana are exposed via AWS ALB Ingress using custom domains:
- App: `https://pwc-task.com`
- Prometheus: `https://prometheus.pwc-task.com`
- Grafana: `https://grafana.pwc-task.com`
All Ingresses use the ACM certificate provisioned by Terraform.

### 5. CI/CD Workflows

*   **Terraform:** `.github/workflows/terraform.yml` runs on changes in `terraform/`.
*   **Docker:** `.github/workflows/docker.yml` builds and pushes the Docker image from `src/` to ECR, tags as `latest` and short commit hash.
*   **Helm Update:** `.github/workflows/helm-update.yml` manually updates the Helm chart image tag.

### 6. Exposing Metrics for Monitoring

To enable Prometheus monitoring, expose a `/metrics` endpoint in your Python app using `prometheus_client`:

```python
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from flask import Response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
```

### 7. Prometheus and Grafana Monitoring

Prometheus and Grafana are deployed via ArgoCD using manifests in `manifests/monitoring/`.

#### Configure Prometheus to Scrape Your App

Edit the Prometheus Application manifest or Helm values to add a scrape config for your app. Example static config:

```yaml
server:
  extraScrapeConfigs:
    - job_name: 'python-app'
      static_configs:
        - targets: ['python-app.default.svc.cluster.local:80']
```

Or deploy a ServiceMonitor CRD if using kube-prometheus-stack.


#### Accessing Prometheus and Grafana

Prometheus and Grafana are exposed via ALB Ingress at:
- Prometheus: `https://prometheus.pwc-task.com`
- Grafana: `https://grafana.pwc-task.com` (default admin:admin)
Your app: `https://pwc-task.com`
DNS records for these domains are managed in Route 53.

#### Visualizing Metrics in Grafana

Add Prometheus as a data source in Grafana and create dashboards using your app’s metrics.

### 8. Clean Up

To destroy all resources created by Terraform:

```bash
cd terraform
terraform destroy
```
