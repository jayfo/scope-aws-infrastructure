import aws_infrastructure.task_templates.terraform
from invoke import Collection

import terraform_elastic_ip.tasks

# Key for configuration
CONFIG_KEY = 'terraform_dns'

# Configured a collection
ns = Collection('dns')

ns.configure({
    CONFIG_KEY: {
        'working_dir': 'terraform_dns',
        'bin_dir': '../bin'
    }
})


# Define variables to provide to Terraform
def variables(*, context):
    with terraform_elastic_ip.tasks.elastic_ip(context=context) as elastic_ip:
        return {
            'eip_public_ip': elastic_ip.output.public_ip
        }


# Define and import tasks
terraform_tasks = aws_infrastructure.task_templates.terraform.create_tasks(
    config_key=CONFIG_KEY,
    variables=variables
)

# Add tasks to our collection
# - Exclude 'init' and 'output' for legibility, could be enabled for debugging.
for task_current in terraform_tasks.tasks.values():
    if task_current.name in ['init', 'output']:
        continue

    ns.add_task(task_current)
