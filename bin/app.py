#!/usr/bin/env python3
import aws_cdk as cdk

from api_rest_stack import ApiRestStack


app = cdk.App()
ApiRestStack(app, "APIRest")

app.synth()
