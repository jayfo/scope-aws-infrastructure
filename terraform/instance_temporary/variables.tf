/*
 * VPC in which to create the instance.
 */
variable "vpc_id" {
  type = string
  default = null
}

/*
 * Default security group ID for the VPC.
 */
variable "vpc_default_security_group_id" {
  type = string
  default = null
}

/*
 * Subnet in which to create the instance.
 */
variable "subnet_id" {
  type = string
  default = null
}
