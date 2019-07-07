import traceback
import json
import re
import os

def handler(event, context):
    macro_response = {
        "requestId": event["requestId"],
        "status": "success"
    }
    # Globals, we only need the fragment in this case but you can get access to all others
    fragment = event['fragment']
    # The extra result copy allows separation of iteration over the fragment and modifying it
    result = fragment

    # This is where you will need to update the code

    # The macro response is what we'll return.
    # This includes the updated fragment piece.
    macro_response['fragment'] = result
    return macro_response
