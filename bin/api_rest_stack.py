from constructs import Construct
from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as secretsmanager,
    triggers
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
        db_cluster = rds.ServerlessCluster(self, 'Database',
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
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False
        )
        
        lambdaLayer = _lambda.LayerVersion(self, 'LambdaLayer',
            code = _lambda.AssetCode('src/layer'),
            compatible_runtimes = [_lambda.Runtime.PYTHON_3_10],
        ) 
        
        table_creator_lambda = triggers.TriggerFunction(self, "MyTrigger",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler='lambda_handler.handler',
            code=_lambda.Code.from_asset('src/lambda_creator'),
            vpc=vpc,
            timeout=Duration.seconds(120),
            layers=[lambdaLayer],
            environment={
                'DB_CLUSTER_ARN': db_cluster.cluster_arn,
                'SECRET_ARN': secret.secret_arn
            }
        )
        
        secret.grant_read(grantee=table_creator_lambda)
        db_cluster.grant_data_api_access(table_creator_lambda)        
        
        table_creator_lambda.execute_after(db_cluster)
        
        # Defines an AWS Lambda POST resource
        api_rest_post_lambda = _lambda.Function(
            self, 'LambdaPostHandler',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('src/lambda_post'),
            handler='lambda_handler.handler',
            vpc=vpc,
            timeout=Duration.seconds(120),
            layers=[lambdaLayer],
            environment={
                'DB_CLUSTER_ARN': db_cluster.cluster_arn,
                'SECRET_ARN': secret.secret_arn
            }
        )
        
        secret.grant_read(grantee=api_rest_post_lambda)
        db_cluster.grant_data_api_access(api_rest_post_lambda)
        
        # Defines an AWS Lambda GET resource
        api_rest_get_lambda = _lambda.Function(
            self, 'LambdaGetHandler',
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset('src/lambda_get'),
            handler='lambda_handler.handler',
            vpc=vpc,
            timeout=Duration.seconds(120),
            layers=[lambdaLayer],
            environment={
                'DB_CLUSTER_ARN': db_cluster.cluster_arn,
                'SECRET_ARN': secret.secret_arn
            }
        )
        
        secret.grant_read(grantee=api_rest_get_lambda)
        db_cluster.grant_data_api_access(api_rest_get_lambda)
        
        # Use apigw API Rest construct
        api = apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=api_rest_post_lambda,
        )
        
        # Add a resource to the API and a method to the resource
        test = api.root.add_resource('test')
        test.add_method('POST', apigw.LambdaIntegration(api_rest_post_lambda))
        test.add_method('GET', apigw.LambdaIntegration(api_rest_get_lambda))