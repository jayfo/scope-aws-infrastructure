from invoke import Collection

import terraform_elastic_ip.tasks
import terraform_instance.tasks

ns = Collection()

ns_terraform_elastic_ip = terraform_elastic_ip.tasks.ns
ns.add_collection(ns_terraform_elastic_ip)
ns.configure(ns_terraform_elastic_ip.configuration())

ns_terraform_instance = terraform_instance.tasks.ns
ns.add_collection(ns_terraform_instance)
ns.configure(ns_terraform_instance.configuration())
