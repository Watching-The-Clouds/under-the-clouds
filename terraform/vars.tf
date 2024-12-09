###
### CHECK COMMENTS FOR NECESSARY TASKS
###

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
    default = "/../.remote_deployment/lambda_extract/"
    ### ADJUST ACCORDING TO FILE STRUCTURE (unverified)
}

variable "lambda_comp_exclude_list" {
    type = list(string)
    default = [".pytest_cache", "src/__pycache__", "test"]
    ### ADJUST ACCORDING TO FILE STRUCTURE (unverified)
}

variable "layer_requests_file" {
    type = string
    default = "../.dependencies/layer_requests.zip"
    ### REMOVE COMMENT WHEN FILE GENERATION HAS BEEN HANDLED!!! ###
}