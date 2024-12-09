#!/bin/bash
echo "TEMPORARY INSTALL - replace with Makefile when appropriate"
mkdir terraform/.remote_deployment
mkdir terraform/.remote_deployment/lambda_extract
mkdir terraform/.remote_deployment/layer_requests
touch terraform/.remote_deployment/layer_requests/placeholder.txt
echo "PLACEHOLDER PLACEHOLDER" >> terraform/.remote_deployment/layer_requests/placeholder.txt
cp -v src/extract.py terraform/.remote_deployment/lambda_extract/extract.py
zip -r terraform/.remote_deployment/lambda_extract.zip terraform/.remote_deployment/lambda_extract
zip -r terraform/.remote_deployment/layer_requests.zip terraform/.remote_deployment/layer_requests
