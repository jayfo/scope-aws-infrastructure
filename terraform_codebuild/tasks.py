"""
Exploratory task for CodeBuild.
"""

from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.codebuild
import aws_infrastructure.tasks.library.terraform
from datetime import datetime
from invoke import Collection

import terraform_ecr.tasks

CONFIG_KEY = 'codebuild'
BIN_TERRAFORM = './bin/terraform.exe'
DIR_TERRAFORM = './terraform_codebuild'

BUILD_TIMESTAMP = datetime.now().strftime('%Y%m%d%H%M')


def codebuild_environment_variables_scope_app(*, context):
    repository = 'scope_aws_infrastructure/scope_app'

    with terraform_ecr.tasks.ecr_read_only(context=context) as ecr_read_only:
        return {
            'REGISTRY_URL': ecr_read_only.output.registry_url,
            'REPOSITORY': repository,
            'REPOSITORY_URL': ecr_read_only.output.repository_urls[repository],
            'REPOSITORY_TAGS': 'latest {}'.format(BUILD_TIMESTAMP)
        }


def codebuild_environment_variables_scope_web(*, context):
    repository = 'scope_aws_infrastructure/scope_web'

    with terraform_ecr.tasks.ecr_read_only(context=context) as ecr_read_only:
        return {
            'REGISTRY_URL': ecr_read_only.output.registry_url,
            'REPOSITORY': repository,
            'REPOSITORY_URL': ecr_read_only.output.repository_urls[repository],
            'REPOSITORY_TAGS': 'latest {}'.format(BUILD_TIMESTAMP)
        }


ns = Collection('codebuild')

ns_terraform = aws_infrastructure.tasks.library.codebuild.create_tasks(
    config_key=CONFIG_KEY,
    bin_terraform=BIN_TERRAFORM,
    dir_terraform=DIR_TERRAFORM,
    instances=[
        'scope_app',
        'scope_web'
    ],
    codebuild_environment_variables={
        'scope_app': codebuild_environment_variables_scope_app,
        'scope_web': codebuild_environment_variables_scope_web,
    }
)

compose_collection(
    ns,
    ns_terraform,
    sub=False,
    exclude=aws_infrastructure.tasks.library.terraform.exclude_destroy_without_state(
        dir_terraform=DIR_TERRAFORM,
        exclude=[
            'init',
            'apply',
        ],
    )
)
