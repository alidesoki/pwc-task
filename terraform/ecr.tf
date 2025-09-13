resource "aws_ecr_repository" "app_repo" {
  name                 = "${var.name_prefix}-app"
  image_tag_mutability = "MUTABLE"
  tags = {
    Environment = var.env_name
    Provisioner = var.provisioner
  }
}
