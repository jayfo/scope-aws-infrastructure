from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.minikube_helm
import aws_infrastructure.tasks.library.terraform
from invoke import Collection

import terraform_eip.tasks

CONFIG_KEY = 'terraform_instance'
BIN_TERRAFORM = './bin/terraform.exe'
DIR_TERRAFORM = './terraform_instance'
DIR_HELM_REPO = './helm_repo'
INSTANCES = ['instance']


# Define variables to provide to Terraform
def variables(*, context):
    with terraform_eip.tasks.eip_read_only(context=context) as eip_read_only:
        return {
            'eip_id': eip_read_only.output.id,
            'eip_public_ip': eip_read_only.output.public_ip
        }


ns = Collection('instance')

ns_minikube_helm = aws_infrastructure.tasks.library.minikube_helm.create_tasks(
    config_key=CONFIG_KEY,
    bin_terraform=BIN_TERRAFORM,
    dir_terraform=DIR_TERRAFORM,
    dir_helm_repo=DIR_HELM_REPO,
    instances=INSTANCES,
    variables=variables
)

compose_collection(
    ns,
    ns_minikube_helm,
    sub=False,
    exclude=aws_infrastructure.tasks.library.terraform.exclude_destroy_without_state(
        dir_terraform=DIR_TERRAFORM,
        exclude=[
            'init',
        ],
    )
)
