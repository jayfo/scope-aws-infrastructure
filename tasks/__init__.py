from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.aws_configure
import aws_infrastructure.tasks.library.color
from invoke import Collection

import tasks.aws
import tasks.codebuild.server_flask
import tasks.codebuild.web_patient
import tasks.codebuild.web_registry
import tasks.database
import tasks.documentdb
import tasks.helm
import tasks.helmfile
import tasks.terraform.documentdb
import tasks.terraform.dns
import tasks.terraform.ecr
import tasks.terraform.eip
import tasks.terraform.instance
import tasks.terraform.userpool
import tasks.terraform.vpc
import tasks.test

# Enable color
aws_infrastructure.tasks.library.color.enable_color()
# Apply the current AWS configuration
aws_infrastructure.tasks.library.aws_configure.apply_aws_env(
    aws_env_path=tasks.aws.AWS_ENV_PATH
)

# Build our task collection
ns = Collection()

# Compose from aws.py
compose_collection(ns, tasks.aws.ns, name="aws")

# Compose from codebuild
ns_codebuild = Collection("codebuild")

compose_collection(ns_codebuild, tasks.codebuild.server_flask.ns, name="server_flask")
compose_collection(ns_codebuild, tasks.codebuild.web_patient.ns, name="web_patient")
compose_collection(ns_codebuild, tasks.codebuild.web_registry.ns, name="web_registry")

compose_collection(ns, ns_codebuild, name="codebuild")

# Compose from database.py
compose_collection(ns, tasks.database.ns, name="database")

# Compose from documentdb.py
compose_collection(ns, tasks.documentdb.ns, name="documentdb")

# Compose from helm.py
compose_collection(ns, tasks.helm.ns, name="helm")

# Compose from helmfile.py
compose_collection(ns, tasks.helmfile.ns, name="helmfile")

# Compose from terraform
ns_terraform = Collection("terraform")

compose_collection(ns_terraform, tasks.terraform.dns.ns, name="dns")
compose_collection(ns_terraform, tasks.terraform.documentdb.ns, name="documentdb")
compose_collection(ns_terraform, tasks.terraform.ecr.ns, name="ecr")
compose_collection(ns_terraform, tasks.terraform.eip.ns, name="eip")
compose_collection(ns_terraform, tasks.terraform.instance.ns, name="instance")
compose_collection(ns_terraform, tasks.terraform.userpool.ns, name="userpool")
compose_collection(ns_terraform, tasks.terraform.vpc.ns, name="vpc")

compose_collection(ns, ns_terraform, name="terraform")

# Compose from test.py
compose_collection(ns, tasks.test.ns, name="test")
