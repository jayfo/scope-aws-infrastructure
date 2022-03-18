from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.terraform
from collections import namedtuple
from invoke import Collection

CONFIG_KEY = 'userpool'
TERRAFORM_BIN = './bin/terraform.exe'
TERRAFORM_DIR = './terraform/userpool'

ns = Collection('userpool')


ns_userpool = aws_infrastructure.tasks.library.terraform.create_tasks(
    config_key=CONFIG_KEY,
    terraform_bin=TERRAFORM_BIN,
    terraform_dir=TERRAFORM_DIR,
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
