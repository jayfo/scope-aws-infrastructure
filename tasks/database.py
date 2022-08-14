from aws_infrastructure.tasks.collection import compose_collection
from invoke import Collection

import scope.tasks.database_initialize
import scope.tasks.database_populate
import scope.tasks.database_reset

INSTANCE_SSH_CONFIG_PATH = "./secrets/configuration/instance_ssh.yaml"
DOCUMENTDB_CONFIG_PATH = "./secrets/configuration/documentdb.yaml"
COGNITO_CONFIG_PATH = "./secrets/configuration/cognito.yaml"

DATABASE_DEV_CONFIG_PATH = "./secrets/configuration/database_dev.yaml"
POPULATE_DEV_DIR_PATH = "./secrets/configuration/populate_dev"

DATABASE_DEMO_CONFIG_PATH = "./secrets/configuration/database_demo.yaml"
POPULATE_DEMO_DIR_PATH = "./secrets/configuration/populate_demo"
POPULATE_DEMO_RESET_DIR_PATH = "./secrets/configuration/populate_demo_reset"

DATABASE_MULTICARE_CONFIG_PATH = "./secrets/configuration/database_multicare.yaml"
POPULATE_MULTICARE_DIR_PATH = "./secrets/configuration/populate_multicare"

DATABASE_SCCA_CONFIG_PATH = "./secrets/configuration/database_scca.yaml"
POPULATE_SCCA_DIR_PATH = "./secrets/configuration/populate_scca"

# Build task collection
ns = Collection("database")

ns_dev = Collection("dev")
ns_dev.add_task(scope.tasks.database_initialize.task_initialize(
    instance_ssh_config_path=INSTANCE_SSH_CONFIG_PATH,
    documentdb_config_path=DOCUMENTDB_CONFIG_PATH,
    database_config_path=DATABASE_DEV_CONFIG_PATH,
), "initialize")
ns_dev.add_task(scope.tasks.database_populate.task_populate(
    instance_ssh_config_path=INSTANCE_SSH_CONFIG_PATH,
    documentdb_config_path=DOCUMENTDB_CONFIG_PATH,
    database_config_path=DATABASE_DEV_CONFIG_PATH,
    cognito_config_path=COGNITO_CONFIG_PATH,
    populate_dir_path=POPULATE_DEMO_DIR_PATH,
), "populate")
ns_dev.add_task(scope.tasks.database_reset.task_reset(
    instance_ssh_config_path=INSTANCE_SSH_CONFIG_PATH,
    documentdb_config_path=DOCUMENTDB_CONFIG_PATH,
    database_config_path=DATABASE_DEV_CONFIG_PATH,
    populate_reset=False,
), "reset")

ns_demo = Collection("demo")
ns_demo.add_task(scope.tasks.database_initialize.task_initialize(
    instance_ssh_config_path=INSTANCE_SSH_CONFIG_PATH,
    documentdb_config_path=DOCUMENTDB_CONFIG_PATH,
    database_config_path=DATABASE_DEMO_CONFIG_PATH,
), "initialize")
ns_demo.add_task(scope.tasks.database_populate.task_populate(
    instance_ssh_config_path=INSTANCE_SSH_CONFIG_PATH,
    documentdb_config_path=DOCUMENTDB_CONFIG_PATH,
    database_config_path=DATABASE_DEMO_CONFIG_PATH,
    cognito_config_path=COGNITO_CONFIG_PATH,
    populate_dir_path=POPULATE_DEMO_DIR_PATH,
), "populate")
ns_demo.add_task(scope.tasks.database_reset.task_reset(
    instance_ssh_config_path=INSTANCE_SSH_CONFIG_PATH,
    documentdb_config_path=DOCUMENTDB_CONFIG_PATH,
    database_config_path=DATABASE_DEMO_CONFIG_PATH,
    populate_reset=False,
), "reset")
ns_demo.add_task(scope.tasks.database_reset.task_reset(
    instance_ssh_config_path=INSTANCE_SSH_CONFIG_PATH,
    documentdb_config_path=DOCUMENTDB_CONFIG_PATH,
    database_config_path=DATABASE_DEMO_CONFIG_PATH,
    populate_reset=True,
    populate_dir_path=POPULATE_DEMO_DIR_PATH,
    populate_reset_dir_path=POPULATE_DEMO_RESET_DIR_PATH,
), "reset-populate")

ns_multicare = Collection("multicare")
ns_multicare.add_task(scope.tasks.database_initialize.task_initialize(
    instance_ssh_config_path=INSTANCE_SSH_CONFIG_PATH,
    documentdb_config_path=DOCUMENTDB_CONFIG_PATH,
    database_config_path=DATABASE_MULTICARE_CONFIG_PATH,
), "initialize")
ns_multicare.add_task(scope.tasks.database_populate.task_populate(
    instance_ssh_config_path=INSTANCE_SSH_CONFIG_PATH,
    documentdb_config_path=DOCUMENTDB_CONFIG_PATH,
    database_config_path=DATABASE_MULTICARE_CONFIG_PATH,
    cognito_config_path=COGNITO_CONFIG_PATH,
    populate_dir_path=POPULATE_MULTICARE_DIR_PATH,
), "populate")
ns_multicare.add_task(scope.tasks.database_reset.task_reset(
    instance_ssh_config_path=INSTANCE_SSH_CONFIG_PATH,
    documentdb_config_path=DOCUMENTDB_CONFIG_PATH,
    database_config_path=DATABASE_MULTICARE_CONFIG_PATH,
    populate_reset=False,
), "reset")

ns_scca = Collection("scca")
ns_scca.add_task(scope.tasks.database_initialize.task_initialize(
    instance_ssh_config_path=INSTANCE_SSH_CONFIG_PATH,
    documentdb_config_path=DOCUMENTDB_CONFIG_PATH,
    database_config_path=DATABASE_SCCA_CONFIG_PATH,
), "initialize")
ns_scca.add_task(scope.tasks.database_populate.task_populate(
    instance_ssh_config_path=INSTANCE_SSH_CONFIG_PATH,
    documentdb_config_path=DOCUMENTDB_CONFIG_PATH,
    database_config_path=DATABASE_SCCA_CONFIG_PATH,
    cognito_config_path=COGNITO_CONFIG_PATH,
    populate_dir_path=POPULATE_SCCA_DIR_PATH,
), "populate")
ns_scca.add_task(scope.tasks.database_reset.task_reset(
    instance_ssh_config_path=INSTANCE_SSH_CONFIG_PATH,
    documentdb_config_path=DOCUMENTDB_CONFIG_PATH,
    database_config_path=DATABASE_SCCA_CONFIG_PATH,
    populate_reset=False,
), "reset")

compose_collection(ns, ns_dev, name="dev")
compose_collection(ns, ns_demo, name="demo")
compose_collection(ns, ns_multicare, name="multicare")
compose_collection(ns, ns_scca, name="scca")
