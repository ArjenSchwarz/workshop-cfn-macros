import traceback
import json
import re
import os


def isIPv6NetACL(cidr):
    if ":" in cidr:
        return True
    else:
        return False


def createEntry(isEgress, entry, resourceName, condition):
    splitset = entry.split(',')
    # Generate entry
    ruleNumber = splitset[0]
    protocol = splitset[1]
    action = splitset[2]
    cidr = splitset[3]
    if splitset[4] == "-1":
        fromPort = "-1"
        toPort = "-1"
    else:
        ports = splitset[4].split('-')
        fromPort = ports[0]
        toPort = ports[1] if len(ports) == 2 else ports[0]

    generatedEntry = {
        "Type": "AWS::EC2::NetworkAclEntry",
        "Properties": {
            "Egress": isEgress,
            "NetworkAclId": {
                "Ref": resourceName
            },
            "Protocol": protocol,
            "RuleAction": action,
            "RuleNumber": ruleNumber
        }
    }
    if condition:
        generatedEntry["Condition"] = condition

    if isIPv6NetACL(cidr):
        generatedEntry["Properties"]["Ipv6CidrBlock"] = cidr
    else:
        generatedEntry["Properties"]["CidrBlock"] = cidr
    if protocol != -1:
        generatedEntry["Properties"]["PortRange"] = {
            "From": fromPort,
            "To": toPort
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
        if "Condition" in fragment["Resources"][resource]:
            condition = fragment["Resources"][resource]["Condition"]
        else:
            condition = ''
        if fragment['Resources'][resource]['Type'] == 'AWS::EC2::NetworkAcl':
            if "Inbound" in fragment['Resources'][resource]['Properties']:
                for entry in fragment['Resources'][resource]['Properties']['Inbound']:
                    entryName, generatedEntry = createEntry(
                        False, entry, resource, condition)
                    result['Resources'][entryName] = generatedEntry
                result['Resources'][resource]['Properties'].pop('Inbound')
            if "Outbound" in fragment['Resources'][resource]['Properties']:
                for entry in fragment['Resources'][resource]['Properties']['Outbound']:
                    entryName, generatedEntry = createEntry(
                        True, entry, resource, condition)
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
                    if condition:
                        generatedAssoc["Condition"] = condition
                    entryName = assoc + resource
                    result['Resources'][entryName] = generatedAssoc
                result['Resources'][resource]['Properties'].pop('Association')

    macro_response['fragment'] = result
    return macro_response
