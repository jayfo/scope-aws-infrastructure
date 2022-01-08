# """
# Exploratory task for CodeBuild.
# """
#
# from aws_infrastructure.tasks import compose_collection
# import aws_infrastructure.tasks.library.codebuild
# import aws_infrastructure.tasks.library.terraform
# from datetime import datetime
# from invoke import Collection
#
# import tasks.terraform.ecr
#
# CONFIG_KEY = 'codebuild'
# TERRAFORM_BIN = './bin/terraform.exe'
# TERRAFORM_DIR = './terraform_codebuild'
#
# BUILD_TIMESTAMP = datetime.now().strftime('%Y%m%d%H%M')
#
#
# def codebuild_environment_variables_scope_app_factory(*, context):
#     repository = 'scope_aws_infrastructure/scope_app'
#
#     with terraform_ecr.tasks.ecr_read_only(context=context) as ecr_read_only:
#         return {
#             'REGISTRY_URL': ecr_read_only.output.registry_url,
#             'REPOSITORY': repository,
#             'REPOSITORY_URL': ecr_read_only.output.repository_urls[repository],
#             'REPOSITORY_TAGS': ' '.join([
#                 'latest',
#                 '{}'.format(BUILD_TIMESTAMP),
#             ])
#         }
#
#
# def codebuild_environment_variables_scope_web_factory(*, context):
#     repository = 'scope_aws_infrastructure/scope_web'
#
#     with terraform_ecr.tasks.ecr_read_only(context=context) as ecr_read_only:
#         return {
#             'REGISTRY_URL': ecr_read_only.output.registry_url,
#             'REPOSITORY': repository,
#             'REPOSITORY_URL': ecr_read_only.output.repository_urls[repository],
#             'REPOSITORY_TAGS': ' '.join([
#                 'latest',
#                 '{}'.format(BUILD_TIMESTAMP),
#             ])
#         }
#
#
# ns = Collection('codebuild')
#
# ns_terraform = aws_infrastructure.tasks.library.codebuild.create_tasks(
#     config_key=CONFIG_KEY,
#     terraform_bin=TERRAFORM_BIN,
#     terraform_dir=TERRAFORM_DIR,
#     instances=[
#         'scope_app',
#         'scope_web'
#     ],
#     codebuild_environment_variables_factory={
#         'scope_app': codebuild_environment_variables_scope_app_factory,
#         'scope_web': codebuild_environment_variables_scope_web_factory,
#     }
# )
#
# compose_collection(
#     ns,
#     ns_terraform,
#     sub=False,
#     exclude=aws_infrastructure.tasks.library.terraform.exclude_without_state(
#         terraform_dir=TERRAFORM_DIR,
#         exclude=[
#             'init',
#             'apply',
#         ],
#         exclude_without_state=[
#             'destroy',
#         ]
#     )
# )
