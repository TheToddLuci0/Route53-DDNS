import aws_cdk as core
import aws_cdk.assertions as assertions

from r53_ddns_unifi.r53_ddns_unifi_stack import R53DdnsUnifiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in r53_ddns_unifi/r53_ddns_unifi_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = R53DdnsUnifiStack(app, "r53-ddns-unifi")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
