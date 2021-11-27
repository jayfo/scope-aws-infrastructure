from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.aws_configure
from invoke import Collection
from pathlib import Path

CONFIG_KEY = 'aws'
AWSENV_PATH = './secrets/aws/.awsenv'
AWSCONFIGS = {
    'uwscope': aws_infrastructure.tasks.library.aws_configure.AWSConfig(
        aws_config_path='./secrets/aws/uw-scope.config',
        profile='uw-scope',
    )
}

ns = Collection('aws')

ns_configure = aws_infrastructure.tasks.library.aws_configure.create_tasks(
    config_key=CONFIG_KEY,
    awsenv_path=AWSENV_PATH,
    awsconfigs=AWSCONFIGS,
)

compose_collection(
    ns,
    ns_configure,
)
