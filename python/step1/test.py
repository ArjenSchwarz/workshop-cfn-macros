import macro
import json
import unittest

class TestStringMethods(unittest.TestCase):
    def testMacroReturnsValues(self):
        event = {}
        event["region"] = "ap-southeast-2"
        event["requestId"] = "testRequest"
        event["fragment"] = {"Resources": {"S3Bucket": {
            "Type": "AWS::S3::Bucket"}}}
        result = macro.handler(event, None)
        self.assertEqual(result["requestId"], event["requestId"])
        self.assertEqual(result["status"], "success")

    def testNonNaclFragmentPassedThrough(self):
        event = {}
        event["region"] = "ap-southeast-2"
        event["requestId"] = "testRequest"
        event["fragment"] = {"Resources": {"S3Bucket": {
            "Type": "AWS::S3::Bucket"}}}
        result = macro.handler(event, None)
        fragment = result["fragment"]
        expected_resources = ["S3Bucket"]
        expected_resources.sort()
        actual_resources = list(fragment["Resources"].keys())
        actual_resources.sort()
        self.assertEqual(expected_resources, actual_resources)
        self.assertEqual(
            fragment["Resources"]["S3Bucket"]["Type"], "AWS::S3::Bucket")

if __name__ == '__main__':
    unittest.main()
