from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.config
from invoke import Collection
import terraform_eip.tasks

import tasks.helm

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

# Compose from terraform_eip
compose_collection(ns, terraform_eip.tasks.ns, name='eip')
