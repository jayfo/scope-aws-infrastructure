/*
 * ID of the VPC.
 */
output "vpc_id" {
  value = module.vpc.vpc_id
}

/*
 * ID of the default security group, automatically assigned by AWS.
 */
output "default_security_group_id" {
  value = module.vpc.default_security_group_id
}

/*
 * ID of the default subnet.
 */
output "subnet_id" {
  value = module.vpc.subnet_id
}

/*
 * ID of all the subnets.
 */
output "subnet_ids" {
  value = module.vpc.subnet_ids
}
