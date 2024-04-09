from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.terraform
from collections import namedtuple
from invoke import Collection
from pathlib import Path

from tasks.constants import TERRAFORM_BIN
import tasks.terraform.ses

CONFIG_KEY = 'userpool'
TERRAFORM_DIR = './terraform/userpool'
TERRAFORM_VARIABLES_PATH = Path(TERRAFORM_DIR, "variables.generated.tfvars")

ns = Collection('userpool')


# Define variables to provide to Terraform
def terraform_variables_factory(*, context):
    with tasks.terraform.ses.ses_read_only(context=context) as ses_read_only:
        ses_domain_identity_arn = ses_read_only.output.domain_identity_arn

    return {
        'ses_domain_identity_arn': ses_domain_identity_arn,
    }


ns_userpool = aws_infrastructure.tasks.library.terraform.create_tasks(
    config_key=CONFIG_KEY,
    terraform_bin=TERRAFORM_BIN,
    terraform_dir=TERRAFORM_DIR,
    auto_approve=False,
    terraform_variables_factory=terraform_variables_factory,
    terraform_variables_path=TERRAFORM_VARIABLES_PATH,
    output_tuple_factory=namedtuple(
        'userpool',
        [
            'userpool',
            'userpool_client',
        ]
    )
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

userpool_read_only = aws_infrastructure.tasks.library.terraform.create_context_manager_read_only(
    init=ns_userpool.tasks['init'],
    output=ns_userpool.tasks['output'],
)
