import boto3
import json


def handler(event, context):
    print(json.dumps(event))
    r53 = boto3.client('route53')

    domain = event['queryStringParameters']['hostname']
    ip = event['queryStringParameters']['myip']
    zones = {}

    pag = r53.get_paginator('list_hosted_zones')

    # get all the hosted zones
    for page in pag.paginate():
        for zone in page['HostedZones']:
            if zone['Name'][-1] == '.':
                zones[zone['Name'][0:-1]] = zone['Id'].split('/')[-1]
            else:
                zones[zone['Name']] = zone['Id'].split('/')[-1]

    # See if we have a match, starting with as far back as possible
    hz = None
    for i in range(0, len(domain.split('.'))):
        fragment = ".".join(domain.split('.')[i:])
        if fragment in zones.keys():
            hz = zones[fragment]
            break

    if hz is None:
        return {'body': json.dumps("failure\nNo such zone"),
                'statusCode': 400}
    
    change = r53.change_resource_record_sets(HostedZoneId=hz, ChangeBatch={
        'Comment': 'dDNS Change',
        'Changes':[{
            'Action': 'UPSERT',
            'ResourceRecordSet':{
                'Name': domain,
                'Type': 'A',
                'TTL': 60,
                'ResourceRecords': [{
                    'Value': ip
            }]
            }
        }]
    })

    return {'body':'good'}


if __name__ == '__main__':
    print(handler(None, None))
