from aws_infrastructure.tasks import compose_collection
from invoke import Collection

import tasks.helm
# import terraform_codebuild.tasks
import tasks.terraform.documentdb
import tasks.terraform.dns
import tasks.terraform.ecr
import tasks.terraform.eip
import tasks.terraform.instance
import tasks.terraform.vpc

# Build our task collection
ns = Collection()

# Compose from helm.py
compose_collection(ns, tasks.helm.ns, name='helm')

# Compose from terraform_codebuild
# compose_collection(ns, terraform_codebuild.tasks.ns, name='codebuild')

# Compose from terraform_documentdb
compose_collection(ns, tasks.terraform.documentdb.ns, name='documentdb')

# Compose from terraform_dns
compose_collection(ns, tasks.terraform.dns.ns, name='dns')

# Compose from terraform_ecr
compose_collection(ns, tasks.terraform.ecr.ns, name='ecr')

# Compose from terraform_eip
compose_collection(ns, tasks.terraform.eip.ns, name='eip')

# Compose from terraform_instance
compose_collection(ns, tasks.terraform.instance.ns, name='instance')

# Compose from terraform_vpc
compose_collection(ns, tasks.terraform.vpc.ns, name='vpc')
