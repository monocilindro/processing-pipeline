aws_region = "ap-southeast-2"
project_name = "ausseabed-processing-pipeline"
vpc_cidr = "173.31.0.0/16"
public_cidrs = [
    "173.31.0.0/16"
    ]
accessip = "0.0.0.0/0"

# geoserver/mapserver vars
server_cpu = 512
server_memory = 4096
#------- compute vars---------------

#fargate_cpu = 512
#fargate_memory = 1024
#app_image = "288871573946.dkr.ecr.ap-southeast-2.amazonaws.com/callcarisbatch:latest"
