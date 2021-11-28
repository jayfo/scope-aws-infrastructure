from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.aws_configure
import aws_infrastructure.tasks.library.color
from invoke import Collection

import tasks.helm
# import terraform_codebuild.tasks
import tasks.aws
# import tasks.terraform.documentdb
import tasks.terraform.dns
import tasks.terraform.ecr
import tasks.terraform.eip
import tasks.terraform.instance
import tasks.terraform.vpc

# Enable color
aws_infrastructure.tasks.library.color.enable_color()
# Apply the current AWS configuration
aws_infrastructure.tasks.library.aws_configure.apply_aws_env(aws_env_path=tasks.aws.AWS_ENV_PATH)

# Build our task collection
ns = Collection()

# Compose from aws.py
compose_collection(ns, tasks.aws.ns, name='aws')

# Compose from helm.py
compose_collection(ns, tasks.helm.ns, name='helm')

# Compose from terraform
ns_terraform = Collection('terraform')

compose_collection(ns_terraform, tasks.terraform.dns.ns, name='dns')
compose_collection(ns_terraform, tasks.terraform.ecr.ns, name='ecr')
compose_collection(ns_terraform, tasks.terraform.eip.ns, name='eip')
compose_collection(ns_terraform, tasks.terraform.instance.ns, name='instance')
compose_collection(ns_terraform, tasks.terraform.vpc.ns, name='vpc')

compose_collection(ns, ns_terraform, name='terraform')


# Compose from terraform_codebuild
# compose_collection(ns, terraform_codebuild.tasks.ns, name='codebuild')
#
# Compose from terraform_documentdb
# compose_collection(ns, tasks.terraform.documentdb.ns, name='documentdb')


# # Compose from terraform_ecr
# compose_collection(ns, tasks.terraform.ecr.ns, name='ecr')
#
#
# # Compose from terraform_vpc
# compose_collection(ns, tasks.terraform.vpc.ns, name='vpc')
