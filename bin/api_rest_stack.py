from constructs import Construct
from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as secretsmanager
)

import json


class ApiRestStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create a VPC
        vpc = ec2.Vpc(self, 'vpc')

        # Secrets Manager Endpoint
        vpc.add_interface_endpoint('sm',
            service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER
        )

        # RDS Data API Endpoint
        vpc.add_interface_endpoint('rds_data',
            service=ec2.InterfaceVpcEndpointAwsService.RDS_DATA
        )
        
        # Create username and password secret for DB Cluster
        secret = secretsmanager.Secret(self, "TemplatedSecret",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps({"username": "postgres"}),
                generate_string_key="password",
                exclude_characters='/@"'
            )
        )

        # Create relational database
        db_cluster = rds.ServerlessCluster(self, 'database',
            engine=rds.DatabaseClusterEngine.aurora_postgres(
                version=rds.AuroraPostgresEngineVersion.VER_13_3
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS  # ISOLATED
            ),
            credentials=rds.Credentials.from_secret(secret=secret),
            default_database_name='apirest',
            enable_data_api=True, 
            removal_policy=RemovalPolicy.RETAIN
        )
        
        # Defines an AWS Lambda resource
        api_rest_lambda = _lambda.Function(
            self, 'Handler',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('src/lambda'),
            handler='lambda_handler.handler',
            vpc=vpc,
            timeout=Duration.seconds(10),
            environment={
                'DB_CLUSTER_ARN': db_cluster.cluster_arn,
                'SECRET_ARN': secret.secret_arn
            }
        )
        
        secret.grant_read(grantee=api_rest_lambda)
        db_cluster.grant_data_api_access(api_rest_lambda)
        
        # Use apigw API Rest construct
        api = apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=api_rest_lambda,
        )
        
        # Add a resource to the API and a method to the resource
        section_1 = api.root.add_resource('section_1')
        section_1.add_method('POST', apigw.LambdaIntegration(api_rest_lambda))