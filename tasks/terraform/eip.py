from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.eip
import aws_infrastructure.tasks.library.terraform
from invoke import Collection

from tasks.constants import TERRAFORM_BIN

CONFIG_KEY = 'eip'
TERRAFORM_DIR = './terraform/eip'

ns = Collection('eip')

ns_eip = aws_infrastructure.tasks.library.eip.create_tasks(
    config_key=CONFIG_KEY,
    terraform_bin=TERRAFORM_BIN,
    terraform_dir=TERRAFORM_DIR,
)

compose_collection(
    ns,
    ns_eip,
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

eip_read_only = aws_infrastructure.tasks.library.eip.create_eip_read_only(
    ns_eip=ns_eip
)
