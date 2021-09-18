from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.terraform
from invoke import Collection

import terraform_eip.tasks

CONFIG_KEY = 'dns'
BIN_TERRAFORM = './bin/terraform.exe'
DIR_TERRAFORM = './terraform_dns'

ns = Collection('dns')


# Define variables to provide to Terraform
def terraform_variables(*, context):
    with terraform_eip.tasks.eip_read_only(context=context) as eip:
        return {
            'eip_public_ip': eip.output.public_ip
        }


ns_dns = aws_infrastructure.tasks.library.terraform.create_tasks(
    config_key=CONFIG_KEY,
    bin_terraform=BIN_TERRAFORM,
    dir_terraform=DIR_TERRAFORM,
    terraform_variables=terraform_variables,
)

compose_collection(
    ns,
    ns_dns,
    sub=False,
    exclude=aws_infrastructure.tasks.library.terraform.exclude_destroy_without_state(
        dir_terraform=DIR_TERRAFORM,
        exclude=[
            'init',
            'output',
        ],
    )
)
