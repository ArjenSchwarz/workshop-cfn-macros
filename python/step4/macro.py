import traceback
import json
import re
import os


def createEntry(isEgress, entry, resourceName):
    splitset = entry.split(',')
    # Generate entry
    ruleNumber = splitset[0]
    protocol = splitset[1]
    action = splitset[2]
    cidr = splitset[3]
    port = splitset[4]

    generatedEntry = {
        "Type": "AWS::EC2::NetworkAclEntry",
        "Properties": {
            "Egress": isEgress,
            "NetworkAclId": {
                "Ref": resourceName
            },
            "Protocol": protocol,
            "RuleAction": action,
            "RuleNumber": ruleNumber,
            "PortRange": {
                "From": port,
                "To": port
            },
            "CidrBlock": cidr
        }
    }

    entryType = 'Outbound' if isEgress else 'Inbound'

    # Generate name
    entryName = resourceName + entryType + ruleNumber
    return entryName, generatedEntry

def handler(event, context):
    macro_response = {
        "requestId": event["requestId"],
        "status": "success"
    }
    # Globals
    fragment = event['fragment']
    result = fragment

    for resource in list(fragment["Resources"].keys()):
        if fragment['Resources'][resource]['Type'] == 'AWS::EC2::NetworkAcl':
            if "Inbound" in fragment['Resources'][resource]['Properties']:
                for entry in fragment['Resources'][resource]['Properties']['Inbound']:
                    entryName, generatedEntry = createEntry(False, entry, resource)
                    result['Resources'][entryName] = generatedEntry
                result['Resources'][resource]['Properties'].pop('Inbound')
            if "Outbound" in fragment['Resources'][resource]['Properties']:
                for entry in fragment['Resources'][resource]['Properties']['Outbound']:
                    entryName, generatedEntry = createEntry(
                        True, entry, resource)
                    result['Resources'][entryName] = generatedEntry
                result['Resources'][resource]['Properties'].pop('Outbound')
            if "Association" in fragment['Resources'][resource]['Properties']:
                for assoc in fragment['Resources'][resource]['Properties']['Association']:
                    generatedAssoc = {
                        "Type": "AWS::EC2::SubnetNetworkAclAssociation",
                        "Properties": {
                            "SubnetId": {"Ref": assoc},
                            "NetworkAclId": {"Ref": resource}
                        }
                    }
                    entryName = assoc + resource
                    result['Resources'][entryName] = generatedAssoc
                result['Resources'][resource]['Properties'].pop('Association')

    macro_response['fragment'] = result
    return macro_response
