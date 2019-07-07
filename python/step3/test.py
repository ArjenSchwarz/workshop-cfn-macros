import macro
import json
import unittest

class TestStringMethods(unittest.TestCase):
    def testNonNaclPassedThrough(self):
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

    def testNaclSinglePortInbound(self):
        generated_resource_name = "NaclPublicInbound100"
        event = {}
        event["region"] = "ap-southeast-2"
        event["requestId"] = "testRequest"
        event["fragment"] = {"Resources": { "NaclPublic": { "Type": "AWS::EC2::NetworkAcl", "Properties": { "Inbound": [ "100,6,allow,0.0.0.0/0,443"]}}}}
        result = macro.handler(event, None)
        fragment = result["fragment"]
        expected_resources = ["NaclPublic", generated_resource_name]
        expected_resources.sort()
        actual_resources = list(fragment["Resources"].keys())
        actual_resources.sort()
        self.assertEqual(expected_resources, actual_resources)
        self.assertEqual(
            fragment["Resources"][generated_resource_name]["Type"], "AWS::EC2::NetworkAclEntry")
        properties_totest = fragment["Resources"][generated_resource_name]["Properties"]
        self.assertEqual(properties_totest["CidrBlock"], "0.0.0.0/0")
        self.assertEqual(properties_totest["Protocol"], "6")
        self.assertEqual(properties_totest["Egress"], False)
        self.assertEqual(properties_totest["NetworkAclId"], {"Ref": "NaclPublic"})
        self.assertEqual(properties_totest["RuleAction"], "allow")
        self.assertEqual(properties_totest["RuleNumber"], "100")
        self.assertEqual(properties_totest["PortRange"]["From"], "443")
        self.assertEqual(properties_totest["PortRange"]["To"], "443")
        self.assertRaises(KeyError, lambda: fragment["Resources"]["NaclPublic"]["Association"])
        self.assertRaises(KeyError, lambda: fragment["Resources"]["NaclPublic"]["Outbound"])
        self.assertRaises(KeyError, lambda: fragment["Resources"]["NaclPublic"]["Inbound"])

    def testNaclSinglePortOutbound(self):
        generated_resource_name = "NaclPublicOutbound100"
        event = {}
        event["region"] = "ap-southeast-2"
        event["requestId"] = "testRequest"
        event["fragment"] = {"Resources": { "NaclPublic": { "Type": "AWS::EC2::NetworkAcl", "Properties": { "Outbound": [ "100,6,allow,0.0.0.0/0,443"]}}}}
        result = macro.handler(event, None)
        fragment = result["fragment"]
        expected_resources = ["NaclPublic", generated_resource_name]
        expected_resources.sort()
        actual_resources = list(fragment["Resources"].keys())
        actual_resources.sort()
        self.assertEqual(expected_resources, actual_resources)
        self.assertEqual(
            fragment["Resources"][generated_resource_name]["Type"], "AWS::EC2::NetworkAclEntry")
        properties_totest = fragment["Resources"][generated_resource_name]["Properties"]
        self.assertEqual(properties_totest["CidrBlock"], "0.0.0.0/0")
        self.assertEqual(properties_totest["Protocol"], "6")
        self.assertEqual(properties_totest["Egress"], True)
        self.assertEqual(properties_totest["NetworkAclId"], {"Ref": "NaclPublic"})
        self.assertEqual(properties_totest["RuleAction"], "allow")
        self.assertEqual(properties_totest["RuleNumber"], "100")
        self.assertEqual(properties_totest["PortRange"]["From"], "443")
        self.assertEqual(properties_totest["PortRange"]["To"], "443")
        self.assertRaises(KeyError, lambda: fragment["Resources"]["NaclPublic"]["Association"])
        self.assertRaises(KeyError, lambda: fragment["Resources"]["NaclPublic"]["Outbound"])
        self.assertRaises(KeyError, lambda: fragment["Resources"]["NaclPublic"]["Inbound"])

    def testNaclAssociation(self):
        generated_resource_name = "SubnetANaclPublic"
        event = {}
        event["region"] = "ap-southeast-2"
        event["requestId"] = "testRequest"
        event["fragment"] = {"Resources": {"NaclPublic": {
            "Type": "AWS::EC2::NetworkAcl", "Properties": {"Association": ["SubnetA"]}}}}
        result = macro.handler(event, None)
        fragment = result["fragment"]
        expected_resources = ["NaclPublic", generated_resource_name]
        expected_resources.sort()
        actual_resources = list(fragment["Resources"].keys())
        actual_resources.sort()
        self.assertEqual(expected_resources, actual_resources)
        self.assertEqual(
            fragment["Resources"][generated_resource_name]["Type"], "AWS::EC2::SubnetNetworkAclAssociation")
        properties_totest = fragment["Resources"][generated_resource_name]["Properties"]
        self.assertEqual(properties_totest["NetworkAclId"], {"Ref": "NaclPublic"})
        self.assertEqual(properties_totest["SubnetId"], {"Ref": "SubnetA"})
        self.assertRaises(KeyError, lambda: fragment["Resources"]["NaclPublic"]["Association"])
        self.assertRaises(KeyError, lambda: fragment["Resources"]["NaclPublic"]["Outbound"])
        self.assertRaises(KeyError, lambda: fragment["Resources"]["NaclPublic"]["Inbound"])


if __name__ == '__main__':
    unittest.main()
