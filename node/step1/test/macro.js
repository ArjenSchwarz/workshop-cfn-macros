const macro = require('../macro');
var assert = require('assert')
var retError, result, fragment, requestId;

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
        retError = err;
        result = value;
        done();
      });
    });
    it('Check that success is returned', function () {
      assert.equal(result['status'], "success");
    });
    it('Check that requestId is returned', function () {
      assert.equal(result['requestId'], requestId);
    });
    it('Check input is passed through', function () {
      assert.equal(result['fragment'], fragment);
    });
  });
});
