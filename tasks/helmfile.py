import aws_infrastructure.tasks.library.instance_helmfile
import scope.config
from invoke import Collection
from pathlib import Path

import tasks.terraform.ecr

CONFIG_KEY = "helmfile"
STAGING_LOCAL_HELMFILE_DIR = "./.staging/helmfile"
STAGING_REMOTE_HELM_DIR = "./.staging/helm"
STAGING_REMOTE_HELMFILE_DIR = "./.staging/helmfile"

INSTANCE_TERRAFORM_DIR = "./terraform/instance"
INSTANCE_NAME = "instance"
HELMFILE_PATH = "./helmfile/uwscope/helmfile.yaml"
HELMFILE_CONFIG_PATH = "./helmfile/uwscope/helmfile_config.yaml"
SSH_CONFIG_PATH = Path(INSTANCE_TERRAFORM_DIR, INSTANCE_NAME, "ssh_config.yaml")

FLASK_DEMO_CONFIG_PATH = "./secrets/configuration/flask_demo.yaml"
FLASK_DEV_CONFIG_PATH = "./secrets/configuration/flask_dev.yaml"
FLASK_MULTICARE_CONFIG_PATH = "./secrets/configuration/flask_multicare.yaml"
FLASK_SCCA_CONFIG_PATH = "./secrets/configuration/flask_scca.yaml"


# Information for accessing the ECR
def ecr_helmfile_values_factory(*, context):
    with tasks.terraform.ecr.ecr_read_only(context=context) as ecr_read_only:
        return {
            "registryUrl": ecr_read_only.output.registry_url,
            "registryUser": ecr_read_only.output.registry_user,
            "registryPassword": ecr_read_only.output.registry_password,
        }

#
# Demo configuration
#

# Information for configuring server_flask
def flask_demo_values_factory(*, context):
    flask_demo_config = scope.config.FlaskConfig.load(FLASK_DEMO_CONFIG_PATH)

    return {
        "flaskConfig": flask_demo_config.encode(),
    }


# Information for configuring web_patient
def web_patient_demo_values_factory(*, context):
    return {
        "webPatientConfig": {
            "flaskBaseUrl": "https://app.demo.uwscope.org/api/",
        }
    }


# Information for configuring web_registry
def web_registry_demo_values_factory(*, context):
    return {
        "webRegistryConfig": {
            "flaskBaseUrl": "https://registry.demo.uwscope.org/api/",
        }
    }

#
# Dev configuration
#

# Information for configuring server_flask
def flask_dev_values_factory(*, context):
    flask_dev_config = scope.config.FlaskConfig.load(FLASK_DEV_CONFIG_PATH)

    return {
        "flaskConfig": flask_dev_config.encode(),
    }


# Information for configuring web_patient
def web_patient_dev_values_factory(*, context):
    return {
        "webPatientConfig": {
            "flaskBaseUrl": "https://app.dev.uwscope.org/api/",
        }
    }


# Information for configuring web_registry
def web_registry_dev_values_factory(*, context):
    return {
        "webRegistryConfig": {
            "flaskBaseUrl": "https://registry.dev.uwscope.org/api/",
        }
    }


#
# MultiCare configuration
#

# Information for configuring server_flask
def flask_multicare_values_factory(*, context):
    flask_multicare_config = scope.config.FlaskConfig.load(FLASK_MULTICARE_CONFIG_PATH)

    return {
        "flaskConfig": flask_multicare_config.encode(),
    }


# Information for configuring web_patient
def web_patient_multicare_values_factory(*, context):
    return {
        "webPatientConfig": {
            "flaskBaseUrl": "https://app.multicare.uwscope.org/api/",
        }
    }


# Information for configuring web_registry
def web_registry_multicare_values_factory(*, context):
    return {
        "webRegistryConfig": {
            "flaskBaseUrl": "https://registry.multicare.uwscope.org/api/",
        }
    }


#
# SCCA configuration
#

# Information for configuring server_flask
def flask_scca_values_factory(*, context):
    flask_scca_config = scope.config.FlaskConfig.load(FLASK_SCCA_CONFIG_PATH)

    return {
        "flaskConfig": flask_scca_config.encode(),
    }


# Information for configuring web_patient
def web_patient_scca_values_factory(*, context):
    return {
        "webPatientConfig": {
            "flaskBaseUrl": "https://app.scca.uwscope.org/api/",
        }
    }


# Information for configuring web_registry
def web_registry_scca_values_factory(*, context):
    return {
        "webRegistryConfig": {
            "flaskBaseUrl": "https://registry.scca.uwscope.org/api/",
        }
    }


task_helmfile_apply = (
    aws_infrastructure.tasks.library.instance_helmfile.task_helmfile_apply(
        config_key=CONFIG_KEY,
        ssh_config_path=SSH_CONFIG_PATH,
        staging_local_dir=STAGING_LOCAL_HELMFILE_DIR,
        staging_remote_dir=STAGING_REMOTE_HELMFILE_DIR,
        helmfile_path=HELMFILE_PATH,
        helmfile_config_path=HELMFILE_CONFIG_PATH,
        helmfile_values_factories={
            "ecr_generated": ecr_helmfile_values_factory,
            # Dev Values
            "flask_dev_generated": flask_dev_values_factory,
            "web_patient_dev_generated": web_patient_dev_values_factory,
            "web_registry_dev_generated": web_registry_dev_values_factory,
            # Demo Values
            "flask_demo_generated": flask_demo_values_factory,
            "web_patient_demo_generated": web_patient_demo_values_factory,
            "web_registry_demo_generated": web_registry_demo_values_factory,
            # MultiCare Values
            "flask_multicare_generated": flask_multicare_values_factory,
            "web_patient_multicare_generated": web_patient_multicare_values_factory,
            "web_registry_multicare_generated": web_registry_multicare_values_factory,
            # SCCA Values
            "flask_scca_generated": flask_scca_values_factory,
            "web_patient_scca_generated": web_patient_scca_values_factory,
            "web_registry_scca_generated": web_registry_scca_values_factory,
        },
    )
)
task_helmfile_apply.__doc__ = "Apply helmfile/uwscope/helmfile.yaml in the instance."


ns = Collection("helmfile")
ns.add_task(task_helmfile_apply, "apply")
