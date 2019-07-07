"use strict";

exports.handler = function(event, context, callback) {
    var macro_response = {
        "requestId": event["requestId"],
        "status": "success",
        "fragment": event["fragment"]
    };
    var fragment = event['fragment'];
    var result = fragment;

    macro_response['fragment'] = result;
    callback(null, macro_response);
};