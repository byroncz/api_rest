from aws_cdk import (
        Stack,
        aws_lambda as _lambda,
        assertions
    )
from bin.api_rest_stack import ApiRestStack
import pytest


def test_lambda_function_created():
    stack = Stack()
    ApiRestStack(stack, 'ApiRestStack')
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::IAM::Role", 0)
    
    
# def test_lambda_has_env_vars():
#     stack = Stack()
#     ApiRestStack(stack, "ApiRestStack")

#     template = assertions.Template.from_stack(stack)
#     envCapture = assertions.Capture()

#     template.has_resource_properties("AWS::Lambda::Function", {
#         "Handler": "lambda_handler.handler",
#         "Environment": envCapture,
#         })

#     assert envCapture.as_object() == {
#             "Variables": {
#                 "DOWNSTREAM_FUNCTION_NAME": {"Ref": "downstream.function_name,"},
#                 "HITS_TABLE_NAME": {"Ref": "self._table.table_name"},
#                 },
#             }
