variable "project_name" {
    type = string
    default = "under-the-clouds"
}

variable "abv_name" {
    type = string
    default = "utc"
}

variable "lambda_extract_source_dir" {
    type = string
    default = "${path.module}/../.remote_deployment/lambda_extract/"
}

variable "lambda_comp_exclude_list" {
    type = list(string)
    default = [".pytest_cache", "src/__pycache__", "test"]
}

