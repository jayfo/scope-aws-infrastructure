from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.codebuild
import aws_infrastructure.tasks.library.terraform
from datetime import datetime
from invoke import Collection

import tasks.terraform.ecr

CONFIG_KEY = "codebuild/web_registry"
TERRAFORM_BIN = "./bin/terraform.exe"
TERRAFORM_DIR = "./terraform/codebuild/web_registry"
STAGING_LOCAL_DIR = "./.staging/codebuild/web_registry"
SOURCE_DIR = "./docker/web_registry"
CODEBUILD_PROJECT_NAME = "uwscope_web_registry"

BUILD_TIMESTAMP = datetime.now().strftime("%Y%m%d%H%M")


def codebuild_environment_variables_factory(*, context):
    with tasks.terraform.ecr.ecr_read_only(context=context) as ecr:
        return {
            "REGISTRY_URL": ecr.output.registry_url,
            "REPOSITORY": "uwscope/web_registry",
            "REPOSITORY_URL": ecr.output.repository_urls["uwscope/web_registry"],
            # 'REPOSITORY_TAGS': 'latest {}'.format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-02-16 {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-02-17 {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-02-18 {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-02-23 {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-02-25 {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-02-27 {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-03-01a {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-03-04a {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-03-05 {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-03-06 {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-03-07 {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-03-14b {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-03-17 {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-03-18b {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-03-19 {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-03-20 {}".format(BUILD_TIMESTAMP),
            # "REPOSITORY_TAGS": "freeze-2022-03-21a {}".format(BUILD_TIMESTAMP),
            "REPOSITORY_TAGS": "v0.2.0 v0.2.0-{}".format(BUILD_TIMESTAMP),
        }


ns = Collection("codebuild/web_registry")

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
