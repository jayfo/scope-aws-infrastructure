/*
 * ID of the Minikube AMI.
 */
module "minikube_ami" {
  source = "github.com/fogies/aws-infrastructure//terraform_common/minikube_ami"

  # UW Scope
  owner_id = "522780171838"
  instance_type = "t3.xlarge"
  docker_volume_size = "50"
  build_timestamp = "20220213225548"
}

/*
 * Instance of Minikube Helm.
 */
module "minikube_instance" {
  source = "github.com/fogies/aws-infrastructure//terraform_common/minikube_instance"

  name = "instance"

  ami_id = module.minikube_ami.id
  aws_instance_type = "t3.xlarge"

  vpc_id = var.vpc_id
  vpc_default_security_group_id = var.vpc_default_security_group_id
  subnet_id = var.subnet_id

  eip_id = var.eip_id
  eip_public_ip = var.eip_public_ip

  tags = local.tags
}
