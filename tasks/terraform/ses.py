from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.terraform
from collections import namedtuple
from invoke import Collection
from pathlib import Path

from tasks.constants import TERRAFORM_BIN
import tasks.terraform.dns

CONFIG_KEY = 'ses'
TERRAFORM_DIR = './terraform/ses'
TERRAFORM_VARIABLES_PATH = Path(TERRAFORM_DIR, "variables.generated.tfvars")

ns = Collection('ses')


# Define variables to provide to Terraform
def terraform_variables_factory(*, context):
    with tasks.terraform.dns.dns_read_only(context=context) as dns_read_only:
        hosted_zone_id = dns_read_only.output.hosted_zone_id

    return {
        'hosted_zone_id': hosted_zone_id,
    }


ns_userpool = aws_infrastructure.tasks.library.terraform.create_tasks(
    config_key=CONFIG_KEY,
    terraform_bin=TERRAFORM_BIN,
    terraform_dir=TERRAFORM_DIR,
    auto_approve=False,
    terraform_variables_factory=terraform_variables_factory,
    terraform_variables_path=TERRAFORM_VARIABLES_PATH,
)

compose_collection(
    ns,
    ns_userpool,
    sub=False,
    exclude=aws_infrastructure.tasks.library.terraform.exclude_without_state(
        terraform_dir=TERRAFORM_DIR,
        exclude=[
            "destroy",  # Prevent destroy
            'init',
            'output',
        ],
        exclude_without_state=[
            'destroy',
        ]
    )
)
