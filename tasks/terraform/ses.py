from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.terraform
from collections import namedtuple
from invoke import Collection

from tasks.constants import TERRAFORM_BIN

CONFIG_KEY = 'ses'
TERRAFORM_DIR = './terraform/ses'

ns = Collection('ses')


ns_userpool = aws_infrastructure.tasks.library.terraform.create_tasks(
    config_key=CONFIG_KEY,
    terraform_bin=TERRAFORM_BIN,
    terraform_dir=TERRAFORM_DIR,
    auto_approve=False,
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
