/*
 * An elastic IP.
 */
resource "aws_eip" "eip" {
  tags = local.tags
}
