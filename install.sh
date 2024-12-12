#!/bin/bash
echo "TEMPORARY INSTALL - replace with Makefile when appropriate"
mkdir .remote_deployment
mkdir .remote_deployment/lambda_extract
mkdir .remote_deployment/layer_requests
touch .remote_deployment/layer_requests/placeholder.txt
echo "PLACEHOLDER PLACEHOLDER" >> .remote_deployment/layer_requests/placeholder.txt
cp -v src/extract.py .remote_deployment/lambda_extract/extract.py
zip -r .remote_deployment/lambda_extract.zip .remote_deployment/lambda_extract
zip -r .remote_deployment/layer_requests.zip .remote_deployment/layer_requests
