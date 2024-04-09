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


ns_ses = aws_infrastructure.tasks.library.terraform.create_tasks(
    config_key=CONFIG_KEY,
    terraform_bin=TERRAFORM_BIN,
    terraform_dir=TERRAFORM_DIR,
    auto_approve=False,
    terraform_variables_factory=terraform_variables_factory,
    terraform_variables_path=TERRAFORM_VARIABLES_PATH,
    output_tuple_factory=namedtuple(
        'ses',
        [
            'domain_identity_arn',
        ]
    )
)

compose_collection(
    ns,
    ns_ses,
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

ses_read_only = aws_infrastructure.tasks.library.terraform.create_context_manager_read_only(
    init=ns_ses.tasks['init'],
    output=ns_ses.tasks['output'],
)
