"use strict";

function createEntry(isEgress, entry, resourceName) {
    var splitset = entry.split(',');
    // Generate entry
    var ruleNumber = splitset[0];
    var protocol = splitset[1];
    var action = splitset[2];
    var cidr = splitset[3];
    var port = splitset[4];

    var generatedEntry = {
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
    };

    var entryType = isEgress ? 'Outbound' : 'Inbound';
    var entryName = resourceName + entryType + ruleNumber
    return [entryName, generatedEntry]
};

exports.handler = function(event, context, callback) {
    var macro_response = {
        "requestId": event["requestId"],
        "status": "success",
        "fragment": event["fragment"]
    };
    var fragment = event['fragment'];
    var result = fragment;
    for (const resource in fragment['Resources']) {
        if (fragment['Resources'][resource]['Type'] == 'AWS::EC2::NetworkAcl') {
            if (fragment['Resources'][resource]['Properties']['Association']) {
                fragment['Resources'][resource]['Properties']['Association'].forEach(assoc => {
                    var generatedAssoc = {
                        "Type": "AWS::EC2::SubnetNetworkAclAssociation",
                        "Properties": {
                            "SubnetId": {"Ref": assoc},
                            "NetworkAclId": {"Ref": resource}
                        }
                    };
                    var entryName = assoc + resource;
                    result['Resources'][entryName] = generatedAssoc;
                });
                delete result['Resources'][resource]['Properties']['Association'];
            };
            if (fragment['Resources'][resource]['Properties']['Inbound']) {
                fragment['Resources'][resource]['Properties']['Inbound'].forEach(entry => {
                    var entryValues = createEntry(false, entry, resource);
                    result['Resources'][entryValues[0]] = entryValues[1];
                });
                delete result['Resources'][resource]['Properties']['Inbound'];
            };
            if (fragment['Resources'][resource]['Properties']['Outbound']) {
                fragment['Resources'][resource]['Properties']['Outbound'].forEach(entry => {
                    var entryValues = createEntry(true, entry, resource);
                    result['Resources'][entryValues[0]] = entryValues[1];
                });
                delete result['Resources'][resource]['Properties']['Outbound'];
            };
        };
    };

    macro_response['fragment'] = result;
    callback(null, macro_response);
};