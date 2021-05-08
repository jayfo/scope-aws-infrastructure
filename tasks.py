from invoke import Collection

import aws_infrastructure.task_templates.config
import aws_infrastructure.task_templates.helm
import terraform_elastic_ip.tasks
import terraform_instance.tasks

ns = Collection()

# Tasks for Invoke configuration
ns_config = aws_infrastructure.task_templates.config.create_tasks()
ns.add_collection(ns_config)
ns.configure(ns_config.configuration())

# Tasks for Helm
HELM_CONFIG_KEY = 'helm'

ns_helm = aws_infrastructure.task_templates.helm.create_tasks(
    config_key=HELM_CONFIG_KEY
)
ns.add_collection(ns_helm)
ns.configure({
    HELM_CONFIG_KEY: {
        'bin_dir': 'bin',
        'helm_charts_dir': 'helm',
        'helm_repo_dir': 'helm_repo',
        'helm_repo_staging_dir': 'helm_repo_staging',
    }
})

# Tasks for our elastic ip
ns_terraform_elastic_ip = terraform_elastic_ip.tasks.ns
ns.add_collection(ns_terraform_elastic_ip)
ns.configure(ns_terraform_elastic_ip.configuration())

# Tasks for our instance
ns_terraform_instance = terraform_instance.tasks.ns
ns.add_collection(ns_terraform_instance)
ns.configure(ns_terraform_instance.configuration())
