# Step 1: Preparation

This step is just to ensure you've got everything ready to work on the rest of the steps. Recommended time on this step < 20 minutes.

## 1.1 CloudFormation S3 packaging bucket

As we write the code of our Lambda function in a separate file, we will need to `package` our final CloudFormation template. For the Lambda function this means it will upload a zipfile to an S3 bucket. If you already have a bucket you wish to use for this, that's great! Otherwise please create one. You can do so manually in the Console, or by using the provided `s3.yml` CloudFormation template.

The easiest way is perhaps to use the included `Makefile` that through the command `make deploy-s3` will create the bucket for you.

### Bonus (optional): Install cfn-lint

When it comes to CloudFormation templates, a good tool to have is cfn-lint. This allows you to do a lint check on your CloudFormation templates and can even be integrated into your IDE of choice. If you don't have it yet, you can install it following the [instructions on GitHub](https://github.com/aws-cloudformation/cfn-python-lint). It's not required, but it might be useful in step 4.

## 1.2 Choose your language

Steps for the workshop are available in either the Python 3.7 or Node 10.x runtimes. It is recommended you use either of these languages, but if you prefer something else that is of course possible. However, unless you want to deploy a custom runtime you should keep it to a natively supported language.

Both Python and Node will have the answers for each step available in the next step. In addition, both languages will have tests available for test-driven development. While Python uses the built-in test framework, for Node it uses the [Mocha test framework](https://mochajs.org).

## 1.3 Build the macro definition in the Lambda function

We need an initial Lambda function that we can start from for our Macro. It has 2 requirements:

1. It needs to pull in the `fragment` (aka template) from the event.
2. The handler should return a response consisting of:
    * `fragment` (with the same value as `event['fragment']`)
    * `requestId` (with the same value as `event['fragment']`)
    * `status` (with the value of `success` if successful)

The [documentation has more details on this](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-macros.html#template-macros-author).

For Python and Node you will find placeholder files and a test file that verifies the end result in their respective step1 directories.

Please note that the files in the stepX directories will not be overwritten when you check out the next step so when you move on you can decide to copy what you've written to the next step and work from there instead of using the provided example code.

## Proceed to Step 2

Once you are done with the above (or wish to proceed otherwise), please check out the step2 branch of the repository.
