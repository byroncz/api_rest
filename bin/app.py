# This code is a Python script that uses the AWS CDK (Cloud Development Kit) to define and
# deploy an AWS CloudFormation stack.
#!/usr/bin/env python3
import aws_cdk as cdk

from api_rest_stack import ApiRestStack


app = cdk.App()
ApiRestStack(app, "APIRest")

app.synth()
