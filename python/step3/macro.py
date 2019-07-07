import traceback
import json
import re
import os


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
