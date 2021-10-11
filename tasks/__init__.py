from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.config
from invoke import Collection

import tasks.helm
import terraform_codebuild.tasks
import terraform_documentdb.tasks
import terraform_dns.tasks
import terraform_ecr.tasks
import terraform_eip.tasks
import terraform_instance.tasks
import terraform_vpc.tasks

# Build our task collection
ns = Collection()

# Tasks for Invoke configuration
compose_collection(
    ns,
    aws_infrastructure.tasks.library.config.create_tasks(),
    name='config'
)

# Compose from helm.py
compose_collection(ns, tasks.helm.ns, name='helm')

# Compose from terraform_codebuild
compose_collection(ns, terraform_codebuild.tasks.ns, name='codebuild')

# Compose from terraform_documentdb
compose_collection(ns, terraform_documentdb.tasks.ns, name='documentdb')

# Compose from terraform_dns
compose_collection(ns, terraform_dns.tasks.ns, name='dns')

# Compose from terraform_ecr
compose_collection(ns, terraform_ecr.tasks.ns, name='ecr')

# Compose from terraform_eip
compose_collection(ns, terraform_eip.tasks.ns, name='eip')

# Compose from terraform_instance
compose_collection(ns, terraform_instance.tasks.ns, name='instance')

# Compose from terraform_vpc
compose_collection(ns, terraform_vpc.tasks.ns, name='vpc')
