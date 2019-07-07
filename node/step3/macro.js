"use strict";

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
        };
    };

    macro_response['fragment'] = result;
    callback(null, macro_response);
};