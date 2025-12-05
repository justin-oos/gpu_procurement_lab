# Copyright 2025 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Define locals
locals {
  scripts_dir = "${path.root}/../scripts/"
  
  file_templates = {
    "base_env.sh" = {
      template        = templatefile("${path.module}/base_env_tpl.sh", {
        project_id      = var.project_id,
        location        = var.region,
        gcs_bucket_name = var.gcs_bucket_name,
      })
      output_file_path = "${local.scripts_dir}/base_env.sh"
      permissions     = "0755"
    }
  }
}

# Create Scripts Directory if missing
resource "null_resource" "create_scripts_dir_if_missing" {
  provisioner "local-exec" {
    command = "mkdir -p ${local.scripts_dir}"
  }
}

# Generate files from templates
resource "local_file" "templated_files" {
  for_each = local.file_templates

  content         = each.value.template
  filename        = "${each.value.output_file_path}"
  file_permission = each.value.permissions

  depends_on = [
    null_resource.create_scripts_dir_if_missing
  ]
}
