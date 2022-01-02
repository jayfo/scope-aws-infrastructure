"""
Tasks for executing tests within appropriate environments.
"""

from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.tests
from invoke import Collection


CONFIG_KEY = "test"
TEST_CONFIGS = {
    "all": aws_infrastructure.tasks.library.tests.TestConfig(
        pipenv_pytest_dirs=[
            ".",
        ],
    ),
}

ns = Collection("test")

ns_dependencies = aws_infrastructure.tasks.library.tests.create_tasks(
    config_key=CONFIG_KEY,
    test_configs=TEST_CONFIGS,
)

compose_collection(
    ns,
    ns_dependencies,
    sub=False,
)
