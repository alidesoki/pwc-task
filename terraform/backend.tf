terraform {
  backend "s3" {
    bucket = "dummy-terraform-state-bucket"
    key    = "state/terraform.tfstate"
    region = "us-east-1"
  }
}
