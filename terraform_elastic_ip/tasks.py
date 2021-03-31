import aws_infrastructure.task_templates.terraform
from collections import namedtuple
from invoke import Collection

# Key for configuration
CONFIG_KEY = 'terraform_elastic_ip'

# Configured a collection
ns = Collection('elastic-ip')

ns.configure({
    CONFIG_KEY: {
        'working_dir': 'terraform_elastic_ip',
        'bin_dir': '../bin'
    }
})

# Define and import tasks
terraform_tasks = aws_infrastructure.task_templates.terraform.create_tasks(
    config_key=CONFIG_KEY,
    output_tuple_factory=namedtuple('elastic_ip', ['id', 'public_ip'])
)

# Add tasks to our collection
# - Exclude 'init' and 'output' for legibility, could be enabled for debugging.
for task_current in terraform_tasks.tasks.values():
    if task_current.name in ['init', 'output']:
        continue

    ns.add_task(task_current)

# Provide only init and output to the context manager.
# It therefore can only access the elastic ip, cannot create or destroy the elastic ip.
elastic_ip = aws_infrastructure.task_templates.terraform.create_context_manager(
    init=terraform_tasks.tasks['init'],
    output=terraform_tasks.tasks['output'],
)
