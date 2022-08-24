# Route53 DDNS
A serverless dynamic DNS provider for AWS backed DNS.


## Deployment

This application uses the AWS CDK. Install instructions [here](https://aws.amazon.com/getting-started/guides/setup-cdk/module-two/).

```bash
pip install -r requirements.txt
cdk deploy
```

The output will include a invocation URL

## Useage
Simply call the endpoint `/prod/nic/update` with the querystring `?hostname=example.com&myip=192.168.1.1`


## TODO
- [ ] Auth that actually works
  - [ ] Limit which users can change which domains?
