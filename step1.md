# Step 1: Preparation

This step is aimed to get you up and running. If you haven't done so yet, make sure you switch your local copy to this same branch by running the command `git checkout step1`.

## 1.1 Choose your language

Steps for the workshop are available in either the Python 3.7 or Node 10.x runtimes. It is recommended you use either of these languages, but if you prefer something else that is of course possible. However, unless you want to deploy a custom runtime you should keep it to a natively supported language.

Both Python and Node will have the answers for each step available in the next step. In addition, both languages will have tests available for test-driven development. While Python uses the built-in test framework, for Node it uses the [Mocha test framework](https://mochajs.org) which you can easily install using `npm install --global mocha`.

## 1.2 Build the macro definition in the Lambda function

We need an initial Lambda function that we can start from for our Macro. It has 2 requirements:

1. It needs to pull in the `fragment` (aka template) from the event.
2. The handler should return a response consisting of:
    * `fragment` (with the same value as `event['fragment']`)
    * `requestId` (with the same value as `event['requestId']`)
    * `status` (with the value of `success` if successful)

The [documentation has more details on this](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-macros.html#template-macros-author).

For Python and Node you will find placeholder files and a test file that verifies the end result in their respective step1 directories.

Please note that the files in the stepX directories will not be overwritten when you check out the next step so when you move on you can decide to copy what you've written to the next step and work from there instead of using the provided example code.

## Proceed to Step 2

Once you are done with the above (or wish to proceed otherwise), please [proceed to step 2](https://github.com/ArjenSchwarz/workshop-cfn-macros/blob/step2/step2.md).
