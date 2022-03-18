from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.vpc
import aws_infrastructure.tasks.library.terraform
from invoke import Collection

CONFIG_KEY = 'vpc'
TERRAFORM_BIN = './bin/terraform.exe'
TERRAFORM_DIR = './terraform/vpc'

ns = Collection('vpc')

ns_vpc = aws_infrastructure.tasks.library.vpc.create_tasks(
    config_key=CONFIG_KEY,
    terraform_bin=TERRAFORM_BIN,
    terraform_dir=TERRAFORM_DIR,
)

compose_collection(
    ns,
    ns_vpc,
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

vpc_read_only = aws_infrastructure.tasks.library.vpc.create_vpc_read_only(
    ns_vpc=ns_vpc
)
