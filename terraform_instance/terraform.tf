/*
 * Tag created resources.
 */
locals {
  tags = {
    "scope-aws-infrastructure/terraform_instance": ""
  }
}

/*
 * Instance of Minikube Helm.
 */
module "minikube_instance" {
  source = "github.com/fogies/aws-infrastructure//terraform_common/minikube_instance"

  name = "instance"

  ami_configuration = "amd64-medium"
  aws_instance_type = "t3.medium"

  vpc_id = var.vpc_id
  vpc_default_security_group_id = var.vpc_default_security_group_id
  subnet_id = var.subnet_id

  eip_id = var.eip_id
  eip_public_ip = var.eip_public_ip

  tags = local.tags
}
