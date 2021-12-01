from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.instance_helmfile
import aws_infrastructure.tasks.library.minikube
import aws_infrastructure.tasks.library.terraform
from invoke import Collection
from pathlib import Path

import tasks.terraform.documentdb
import tasks.terraform.ecr
import tasks.terraform.eip
import tasks.terraform.vpc

CONFIG_KEY = 'instance'
TERRAFORM_BIN = './bin/terraform.exe'
TERRAFORM_DIR = './terraform/instance'
HELM_REPO_DIR = './helm_repo'
STAGING_LOCAL_HELMFILE_DIR = './.staging/helmfile'
STAGING_REMOTE_HELM_DIR = './.staging/helm'
STAGING_REMOTE_HELMFILE_DIR = './.staging/helmfile'
INSTANCE_NAME = 'instance'
TERRAFORM_VARIABLES_PATH = Path(TERRAFORM_DIR, 'variables.generated.tfvars')


ns = Collection('instance')

#
# Default tasks for maintaining the instance.
#


# Define variables to provide to Terraform
def terraform_variables_factory(*, context):
    with tasks.terraform.eip.eip_read_only(context=context) as eip_read_only:
        eip_id = eip_read_only.output.id
        eip_public_ip = eip_read_only.output.public_ip

    with tasks.terraform.vpc.vpc_read_only(context=context) as vpc_read_only:
        vpc_id = vpc_read_only.output.vpc_id
        vpc_default_security_group_id = vpc_read_only.output.default_security_group_id
        subnet_id = vpc_read_only.output.subnet_id

    return {
        'eip_id': eip_id,
        'eip_public_ip': eip_public_ip,
        'vpc_id': vpc_id,
        'vpc_default_security_group_id': vpc_default_security_group_id,
        'subnet_id': subnet_id,
    }


ns_minikube = aws_infrastructure.tasks.library.minikube.create_tasks(
    config_key=CONFIG_KEY,
    terraform_bin=TERRAFORM_BIN,
    terraform_dir=TERRAFORM_DIR,
    helm_repo_dir=HELM_REPO_DIR,
    staging_local_helmfile_dir=STAGING_LOCAL_HELMFILE_DIR,
    staging_remote_helm_dir=STAGING_REMOTE_HELM_DIR,
    staging_remote_helmfile_dir=STAGING_REMOTE_HELMFILE_DIR,
    instance_names=[INSTANCE_NAME],
    terraform_variables_factory=terraform_variables_factory,
    terraform_variables_path=TERRAFORM_VARIABLES_PATH,
)

compose_collection(
    ns,
    ns_minikube,
    sub=False,
    exclude=aws_infrastructure.tasks.library.terraform.exclude_without_state(
        terraform_dir=TERRAFORM_DIR,
        exclude=[
            'init',
            'helm-install',
            'helmfile-apply',
            'ssh-port-forward',
        ],
        exclude_without_state=[
            'destroy',
        ]
    )
)


# #
# # A task for deploying our primary Helmfile to the instance.
# #
#
# # Helmfile deployment requires information on accessing the DocumentDB
# def documentdb_helmfile_values_factory(*, context):
#     with terraform_documentdb.tasks.documentdb_read_only(context=context) as documentdb_read_only:
#         return {
#             'documentdbAdminUser': documentdb_read_only.output.admin_user,
#             'documentdbAdminPassword': documentdb_read_only.output.admin_password,
#             'documentdbEndpoint': documentdb_read_only.output.endpoint,
#             'documentdbHosts': documentdb_read_only.output.hosts,
#         }
#
#
# # Helmfile deployment requires information on accessing the ECR
# def ecr_helmfile_values_factory(*, context):
#     with terraform_ecr.tasks.ecr_read_only(context=context) as ecr_read_only:
#         return {
#             'registryUrl': ecr_read_only.output.registry_url,
#             'registryUser': ecr_read_only.output.registry_user,
#             'registryPassword': ecr_read_only.output.registry_password,
#         }
#
#
# ssh_config_path = Path(TERRAFORM_DIR, INSTANCE_NAME, 'ssh_config.yaml')
#
# if ssh_config_path.exists():
#     task_helmfile_scope = aws_infrastructure.tasks.library.instance_helmfile.task_helmfile_apply(
#         config_key=CONFIG_KEY,
#         ssh_config_path=ssh_config_path,
#         staging_local_dir=STAGING_LOCAL_HELMFILE_DIR,
#         staging_remote_dir=STAGING_REMOTE_HELMFILE_DIR,
#         helmfile_path='./helmfile/helmfile_scope/helmfile.yaml',
#         helmfile_config_path='./helmfile/helmfile_scope/helmfile-config.yaml',
#         helmfile_values_factories={
#             'documentdb': documentdb_helmfile_values_factory,
#             'ecr': ecr_helmfile_values_factory,
#         },
#     )
#
#     ns.add_task(task_helmfile_scope, name='helmfile-scope')
