###
### CHECK COMMENTS FOR NECESSARY TASKS
###

variable "project_name" {
    type = string
    default = "watching-the-clouds"
}

variable "abv_name" {
    type = string
    default = "utc"
}

variable "lambda_extract_source_dir" {
    type = string
    default = "../src/extract/"
}

variable "lambda_comp_exclude_list" {
    type = list(string)
    default = [".pytest_cache", "__pycache__", "test"]
}

variable "layer_requests_file" {
    type = string
    default = "../.remote_deployment/layer_requests.zip"
    ### REMOVE COMMENT WHEN FILE GENERATION HAS BEEN HANDLED!!! ###
}

variable "openweather_api_key" {
    type = string
    default = ""
}