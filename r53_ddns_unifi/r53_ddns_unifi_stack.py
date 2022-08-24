from os import path
from aws_cdk import (
    # Duration,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_apigateway as api_gateway,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct


class R53DdnsUnifiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "R53DdnsUnifiQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        fun = lambda_.Function(self, "Route53ChangeFuntion", code=lambda_.Code.from_asset(path.join(
            path.dirname(path.realpath(__file__)), "lambda")), handler="lambda.handler", runtime=lambda_.Runtime.PYTHON_3_9)
        api = api_gateway.LambdaRestApi(self, "Route53API", handler=fun)
        nic = api.root.add_resource("nic")
        upd = nic.add_resource("update")
        upd.add_method("GET")

        role = fun.role
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonRoute53ReadOnlyAccess"))
        role.attach_inline_policy(policy=iam.Policy(self, "Route53dDNS-policy", statements=[iam.PolicyStatement(
            actions=["route53:ChangeResourceRecordSets"],
            resources=["*"]
        )]))
