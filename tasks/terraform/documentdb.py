from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.documentdb
import aws_infrastructure.tasks.library.terraform
from invoke import Collection
from pathlib import Path

from tasks.constants import TERRAFORM_BIN
import tasks.terraform.vpc

CONFIG_KEY = 'documentdb'
TERRAFORM_DIR = './terraform/documentdb'
TERRAFORM_VARIABLES_PATH = Path(TERRAFORM_DIR, 'variables.generated.tfvars')
DOCUMENTDB_NAME = 'scope-documentdb'

ns = Collection('documentdb')


# Define variables to provide to Terraform
def terraform_variables_factory(*, context):
    with tasks.terraform.vpc.vpc_read_only(context=context) as vpc_read_only:
        subnet_ids = vpc_read_only.output.subnet_ids

    return {
        'subnet_ids': subnet_ids,
    }


ns_documentdb = aws_infrastructure.tasks.library.documentdb.create_tasks(
    config_key=CONFIG_KEY,
    terraform_bin=TERRAFORM_BIN,
    terraform_dir=TERRAFORM_DIR,
    terraform_variables_factory=terraform_variables_factory,
    terraform_variables_path=TERRAFORM_VARIABLES_PATH,
    name=DOCUMENTDB_NAME,
)

compose_collection(
    ns,
    ns_documentdb,
    sub=False,
    exclude=aws_infrastructure.tasks.library.terraform.exclude_without_state(
        terraform_dir=TERRAFORM_DIR,
        exclude=[
            "destroy",  # Prevent destroy
            "init",
            "output",
        ],
        exclude_without_state=[
            "destroy",
        ],
    ),
)

documentdb_read_only = aws_infrastructure.tasks.library.documentdb.create_documentdb_read_only(
    ns_documentdb=ns_documentdb
)
