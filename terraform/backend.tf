terraform {
  backend "s3" {
    bucket = "dummy-terraform-state-bucket"
    key    = "state/terraform.tfstate"
    region = "eu-central-1"
    use_lockfile = true
  }
}
