from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.codebuild
import aws_infrastructure.tasks.library.terraform
from datetime import datetime
from invoke import Collection

from tasks.constants import TERRAFORM_BIN
import tasks.terraform.ecr

CONFIG_KEY = "codebuild/server_flask"
TERRAFORM_DIR = "./terraform/codebuild/server_flask"
STAGING_LOCAL_DIR = "./.staging/codebuild/server_flask"
SOURCE_DIR = "./docker/server_flask"
CODEBUILD_PROJECT_NAME = "uwscope_server_flask"

BUILD_TIMESTAMP = datetime.now().strftime("%Y%m%d%H%M")


def codebuild_environment_variables_factory(*, context):
    with tasks.terraform.ecr.ecr_read_only(context=context) as ecr:
        return {
            "REGISTRY_URL": ecr.output.registry_url,
            "REPOSITORY": "uwscope/server_flask",
            "REPOSITORY_URL": ecr.output.repository_urls["uwscope/server_flask"],
            # "REPOSITORY_TAGS": "v0.15.0-beta01 v0.15.0-beta01-{}".format(BUILD_TIMESTAMP),
            "REPOSITORY_TAGS": "v0.16.1 v0.16.1-{}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "v0.16.0 v0.16.0-{}".format(BUILD_TIMESTAMP),
        }


ns = Collection("codebuild/server_flask")

ns_codebuild = aws_infrastructure.tasks.library.codebuild.create_tasks(
    config_key=CONFIG_KEY,
    terraform_bin=TERRAFORM_BIN,
    terraform_dir=TERRAFORM_DIR,
    staging_local_dir=STAGING_LOCAL_DIR,
    source_dir=SOURCE_DIR,
    codebuild_project_name=CODEBUILD_PROJECT_NAME,
    codebuild_environment_variables_factory=codebuild_environment_variables_factory,
)

compose_collection(
    ns,
    ns_codebuild,
    sub=False,
    exclude=aws_infrastructure.tasks.library.terraform.exclude_without_state(
        terraform_dir=TERRAFORM_DIR,
        exclude=[
            "init",
            "apply",
        ],
        exclude_without_state=[
            "destroy",
        ],
    ),
)
