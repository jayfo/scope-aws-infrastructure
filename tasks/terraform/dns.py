from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.terraform
from invoke import Collection
from pathlib import Path

from tasks.constants import TERRAFORM_BIN
import tasks.terraform.eip

CONFIG_KEY = "dns"
TERRAFORM_DIR = "./terraform/dns"
TERRAFORM_VARIABLES_PATH = Path(TERRAFORM_DIR, "variables.generated.tfvars")

ns = Collection("dns")


# Define variables to provide to Terraform
def terraform_variables_factory(*, context):
    with tasks.terraform.eip.eip_read_only(context=context) as eip:
        return {
            "eip_public_ip": eip.output.public_ip,
        }


ns_dns = aws_infrastructure.tasks.library.terraform.create_tasks(
    config_key=CONFIG_KEY,
    terraform_bin=TERRAFORM_BIN,
    terraform_dir=TERRAFORM_DIR,
    auto_approve=False,
    terraform_variables_factory=terraform_variables_factory,
    terraform_variables_path=TERRAFORM_VARIABLES_PATH,
)

compose_collection(
    ns,
    ns_dns,
    sub=False,
    exclude=aws_infrastructure.tasks.library.terraform.exclude_without_state(
        terraform_dir=TERRAFORM_DIR,
        exclude=[
            "destroy",  # Prevent destroy
            "init",
            "output",
        ],
        exclude_without_state=[
            # Prevent destroy
            # "destroy",
        ],
    ),
)
