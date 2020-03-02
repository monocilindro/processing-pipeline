output "aws_ecs_cluster_arn" {
  value = "${aws_ecs_cluster.main.arn}"
}


output "aws_ecs_task_definition_caris-version_arn" {
  value = "${aws_ecs_task_definition.caris-version.arn}"
}

output "aws_ecs_task_definition_startstopec2_arn" {
  value = "${aws_ecs_task_definition.startstopec2.arn}"
}

output "aws_ecs_task_definition_gdal_arn" {
  value = "${aws_ecs_task_definition.gdal.arn}"
}


output "aws_ecs_task_definition_mbsystem_arn" {
  value = "${aws_ecs_task_definition.mbsystem.arn}"
}


output "aws_ecs_task_definition_pdal_arn" {
  value = "${aws_ecs_task_definition.pdal.arn}"
}

