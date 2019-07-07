const macro = require('../macro');
var assert = require('assert');
var retError, result, fragment, requestId, generated_resource_name;

describe('handler', function () {
  context('Macro Returns Values', function () {
    before('Invoke function', function (done) {
      fragment = {
        "Resources": {
          "S3Bucket": {
              "Type": "AWS::S3::Bucket"
            }
          }
        };
      requestId = "testRequest";
      var event = {
        'region': 'ap-southeast-2',
        'requestId': requestId,
        'fragment': fragment
      };
      var context = {
        functionName: 'NaclExpander'
      };
      macro.handler(event, context, function (err, value) {
        retError = err ;
        result = value ;
        done();
      });
    });
    it('Check that success is returned', function () {
      assert.equal(result.status, "success");
    });
    it('Check that requestId is returned', function () {
      assert.equal(result.requestId, requestId);
    });
    it('Check input is passed through', function () {
      assert.equal(result.fragment, fragment);
    });
  });
  context('Nacl Association is created', function () {
    before('Invoke function', function (done) {
      generated_resource_name = 'SubnetANaclPublic';
      fragment = {"Resources": {"NaclPublic": { "Type": "AWS::EC2::NetworkAcl", "Properties": {"Association": ["SubnetA"]}}}};
      requestId = "testRequest";
      var event = {
        'region': 'ap-southeast-2',
        'requestId': requestId,
        'fragment': fragment
      };
      var context = {
        functionName: 'NaclExpander'
      };
      macro.handler(event, context, function (err, value) {
        retError = err ;
        result = value ;
        done();
      });
    });
    it('Check that success and requestId are returned', function () {
      assert.equal(result.status, "success");
    });
    it('Check that requestId is returned', function () {
      assert.equal(result.requestId, requestId);
    });
    it('Check all expected resources exist', function () {
      var expected_resources = ["NaclPublic", generated_resource_name]
      assert.deepEqual(Object.keys(result.fragment.Resources), expected_resources);
    });
    it('Check that correct type is set for association', function () {
      var expected_resource_type = 'AWS::EC2::SubnetNetworkAclAssociation';
      assert.equal(result.fragment.Resources[generated_resource_name].Type, expected_resource_type);
    });
    it('Check that correct properties are set for association', function () {
      var properties = result.fragment.Resources[generated_resource_name].Properties;
      assert.deepEqual(properties.NetworkAclId, {"Ref": "NaclPublic"});
      assert.deepEqual(properties.SubnetId, {"Ref": "SubnetA"});
    });
    it('Check that all Macro specific properties are removed', function () {
      assert.equal(result.fragment.Resources.NaclPublic.Properties.hasOwnProperty('Association'), false);
      assert.equal(result.fragment.Resources.NaclPublic.Properties.hasOwnProperty('Inbound'), false);
      assert.equal(result.fragment.Resources.NaclPublic.Properties.hasOwnProperty('Outbound'), false);
    });
  });
  context('Single Port Inbound', function () {
    before('Invoke function', function (done) {
      generated_resource_name = 'NaclPublicInbound100';
      fragment = {"Resources": { "NaclPublic": { "Type": "AWS::EC2::NetworkAcl", "Properties": { "Inbound": [ "100,6,allow,0.0.0.0/0,443"]}}}};
      requestId = "testRequest";
      var event = {
        'region': 'ap-southeast-2',
        'requestId': requestId,
        'fragment': fragment
      };
      var context = {
        functionName: 'NaclExpander'
      };
      macro.handler(event, context, function (err, value) {
        retError = err ;
        result = value ;
        done();
      });
    });
    it('Check that success and requestId are returned', function () {
      assert.equal(result.status, "success");
    });
    it('Check that requestId is returned', function () {
      assert.equal(result.requestId, requestId);
    });
    it('Check all expected resources exist', function () {
      var expected_resources = ["NaclPublic", generated_resource_name]
      assert.deepEqual(Object.keys(result.fragment.Resources), expected_resources);
    });
    it('Check that correct type is set for association', function () {
      var expected_resource_type = 'AWS::EC2::NetworkAclEntry';
      assert.equal(result.fragment.Resources[generated_resource_name].Type, expected_resource_type);
    });
    it('Check that correct properties are set for association', function () {
      var properties = result.fragment.Resources[generated_resource_name].Properties;
      assert.deepEqual(properties['CidrBlock'], '0.0.0.0/0');
      assert.deepEqual(properties['Protocol'], '6');
      assert.deepEqual(properties['Egress'], false);
      assert.deepEqual(properties['NetworkAclId'], { Ref: 'NaclPublic' });
      assert.deepEqual(properties['RuleAction'], 'allow');
      assert.deepEqual(properties['RuleNumber'], '100');
      assert.deepEqual(properties['PortRange']['From'], '443');
      assert.deepEqual(properties['PortRange']['To'], '443');
    });
    it('Check that all Macro specific properties are removed', function () {
      assert.equal(result.fragment.Resources.NaclPublic.Properties.hasOwnProperty('Association'), false);
      assert.equal(result.fragment.Resources.NaclPublic.Properties.hasOwnProperty('Inbound'), false);
      assert.equal(result.fragment.Resources.NaclPublic.Properties.hasOwnProperty('Outbound'), false);
    });
  });
  context('Single Port Outbound', function () {
    before('Invoke function', function (done) {
      generated_resource_name = 'NaclPublicOutbound100';
      fragment = {"Resources": { "NaclPublic": { "Type": "AWS::EC2::NetworkAcl", "Properties": { "Outbound": [ "100,6,allow,0.0.0.0/0,443"]}}}};
      requestId = "testRequest";
      var event = {
        'region': 'ap-southeast-2',
        'requestId': requestId,
        'fragment': fragment
      };
      var context = {
        functionName: 'NaclExpander'
      };
      macro.handler(event, context, function (err, value) {
        retError = err ;
        result = value ;
        done();
      });
    });
    it('Check that success and requestId are returned', function () {
      assert.equal(result.status, "success");
    });
    it('Check that requestId is returned', function () {
      assert.equal(result.requestId, requestId);
    });
    it('Check all expected resources exist', function () {
      var expected_resources = ["NaclPublic", generated_resource_name]
      assert.deepEqual(Object.keys(result.fragment.Resources), expected_resources);
    });
    it('Check that correct type is set for association', function () {
      var expected_resource_type = 'AWS::EC2::NetworkAclEntry';
      assert.equal(result.fragment.Resources[generated_resource_name].Type, expected_resource_type);
    });
    it('Check that correct properties are set for association', function () {
      var properties = result.fragment.Resources[generated_resource_name].Properties;
      assert.deepEqual(properties['CidrBlock'], '0.0.0.0/0');
      assert.deepEqual(properties['Protocol'], '6');
      assert.deepEqual(properties['Egress'], true);
      assert.deepEqual(properties['NetworkAclId'], { Ref: 'NaclPublic' });
      assert.deepEqual(properties['RuleAction'], 'allow');
      assert.deepEqual(properties['RuleNumber'], '100');
      assert.deepEqual(properties['PortRange']['From'], '443');
      assert.deepEqual(properties['PortRange']['To'], '443');
    });
    it('Check that all Macro specific properties are removed', function () {
      assert.equal(result.fragment.Resources.NaclPublic.Properties.hasOwnProperty('Association'), false);
      assert.equal(result.fragment.Resources.NaclPublic.Properties.hasOwnProperty('Inbound'), false);
      assert.equal(result.fragment.Resources.NaclPublic.Properties.hasOwnProperty('Outbound'), false);
    });
  });
});
