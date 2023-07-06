import pytest

from aws_cdk import core
from constructs import Construct
from bin.api_rest_stack import ApiRestStack


def test_api_rest_stack_init():
    # Test that ApiRestStack initializes without throwing an exception
    app = core.App()
    ApiRestStack(app, "MyTestStack")

    
def test_api_rest_stack_resources():
    # Test that ApiRestStack creates the correct resources
    app = core.App()
    stack = ApiRestStack(app, "MyTestStack")
     # Assert VPC resource is created
    assert len(stack.node.find_all_children('vpc')) == 1
     # Assert Secrets Manager Endpoint is created
    assert len(stack.node.find_all_children('sm')) == 1
     # Assert RDS Data API Endpoint is created
    assert len(stack.node.find_all_children('rds_data')) == 1
     # Assert DB Cluster is created
    assert len(stack.node.find_all_children('Database')) == 1
     # Assert Lambda Layer is created
    assert len(stack.node.find_all_children('LambdaLayer')) == 1
     # Assert Lambda Functions are created
    assert len(stack.node.find_all_children('LambdaPostHandler')) == 1
    assert len(stack.node.find_all_children('LambdaGetHandler')) == 1
     # Assert API Gateway is created
    assert len(stack.node.find_all_children('Endpoint')) == 1