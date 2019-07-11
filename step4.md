# Step 4: Finishing touches

Now that you have a working macro, in this step we will (optionally) add some finishing touches for a complete solution. Based on how much time you have left, you may wish to skip to 4.2 to deploy your Macro and implement 4.1. If you haven't done so yet, make sure you switch your local copy to this same branch by running the command `git checkout step4`.

## 4.1 Support for port ranges and IPv6

The NACL entries we built so far only supported a single port. But that rules out 2 other options.

1. A range (for example port 443 till 446)
2. All ports, generally marked as -1 in the CloudFormation for NACL entries

Most likely the second option will already work, but you have to ensure that is still the case after supporting the range. So your task is to update the code in such a way that it supports all 3 of the entries below:

```yaml
    - "100,6,allow,0.0.0.0/0,443"
    - "110,-1,allow,10.0.0.0/8,-1"
    - "150,6,allow,0.0.0.0/0,32768-61000"
```

IPv6 is handled differently in the resulting CloudFormation. So you will need to differentiate between IPv6 (`2406:da1c:a9e:b901::/64`) and IPv4 (`10.0.0.0/8`) CIDR ranges. In the tests it is assumed that the code will be able to differentiate between IPv4 and IPv6 so you can add them to your Inbound and Outbound properties the same as the rest.

There are tests available for both of these functionalities in the step 4 directories.

## 4.2 Build the CloudFormation template

The last step is to build the CloudFormation template to deploy the Macro.

A couple of things to note here:

1. You will need to implement a `AWS::CloudFormation::Macro` resource to ensure the Macro is usable. For the name property use `NaclExpander`.
2. You will need to grant permissions to CloudFormation to run the Lambda function containing the Macro.
3. You can use the property `Code` in your Lambda function resource to refer to a local file. e.g. `Code: ./macro.py`

### Optional: Install cfn-lint

When it comes to CloudFormation templates, a good tool to have is cfn-lint. This allows you to do a lint check on your CloudFormation templates and can even be integrated into your IDE of choice. If you don't have it yet, you can install it following the [instructions on GitHub](https://github.com/aws-cloudformation/cfn-python-lint). It's not required, but it might be helpful for building this template.

## 4.3 CloudFormation S3 packaging bucket

As we've written the code of our Lambda function in a separate file, we will need to `package` our final CloudFormation template. For the Lambda function this means it will upload a zipfile to an S3 bucket. If you already have a bucket you wish to use for this, that's great! Otherwise please create one. You can do so manually in the Console, or by using the provided `s3.yml` CloudFormation template.

The easiest way is perhaps to use the included `Makefile` that through the command `make deploy-s3` will create the bucket for you.

## 4.4 Deploy the CloudFormation template

As we built the code in a separate file, you can use the `aws cloudformation package` command to automatically push up the zipped code to the S3 Bucket from step 1.1 and create a CloudFormation template that includes a reference to the code.

If you don't have experience with it the complete command to run is below. This assumes your S3 bucket is called `lambda-artefacts-bucket-123456`, your template is `macro-template.yml`, and you want the resulting packaged template to be called `macro-packaged.yml`.

```bash
aws cloudformation package --template-file ./python/finished/cfn-template.yml --s3-bucket lambda-artefacts-bucket-123456 --output-template-file macro-packaged.yml
```

You can then deploy the template by running the following command.

```bash
aws cloudformation deploy --template-file ./macro-packaged.yml --stack-name Macro-NaclExpander --capabilities CAPABILITY_IAM
```

If you don't have access to the AWS CLI you can instead zip up your code manually and upload it to your S3 bucket. This then requires you to manually change the template to ensure the `Code` property knows where to look. That means instead of pointing at the local path for the file you point it at the S3 bucket. This is done with the below code:

```yaml
    Properties:
      Code:
        S3Bucket: name-of-your-bucket
        S3Key: name-of-your-zipfile
```

After this you can then use the CloudFormation Console to deploy the template.

## You are done!

Feel free to [proceed to the final step](https://github.com/ArjenSchwarz/workshop-cfn-macros/blob/finished/finished.md). In there you can compare what you wrote to the example provided as well as find a `test-vpc.yml` CloudFormation template that you can use to test your work by spinning up a VPC that uses the Macro.
