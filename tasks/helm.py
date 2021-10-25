"""
Tasks for managing Helm charts.
"""

from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.helm
from invoke import Collection

CONFIG_KEY = 'helm'
HELM_BIN = './bin/helm.exe'
HELM_CHARTS_DIRS = [
    './helm',
]
HELM_REPO_DIR = './helm_repo'
STAGING_LOCAL_DIR = './.staging/helm_repo'

ns = Collection('helm')

ns_helm = aws_infrastructure.tasks.library.helm.create_tasks(
    config_key=CONFIG_KEY,
    helm_bin=HELM_BIN,
    helm_charts_dirs=HELM_CHARTS_DIRS,
    helm_repo_dir=HELM_REPO_DIR,
    staging_local_dir=STAGING_LOCAL_DIR,
)

compose_collection(
    ns,
    ns_helm,
    sub=False
)
