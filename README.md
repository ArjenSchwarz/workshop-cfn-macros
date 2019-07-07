# CloudFormation Macros Workshop - NaclExpander

This workshop is aimed at building your first CloudFormation Macro, and was designed for the [Melbourne AWS Programming and Tools Meetup](https://www.meetup.com/Melbourne-AWS-Programming-and-Tools-Meetup/), but can be run independently. The main requirement is that you have an AWS account you can run this in, and have coding experience in a language supported by Lambda. Examples/Answers are provided in both Python (3.7) and Node (10.x).

Last year AWS released CloudFormation Macros and, by doing so, gave us the ability to fully customise our CloudFormation templates. Macros run as Lambda functions that you write yourself and CloudFormation will allow these functions to change your templates in any way you want them to. This can be anything you imagine; duplicating entries, ensuring naming standards, pulling information from S3, up to and including writing your own custom templates that create a complete environment. In this workshop we'll take a first step in this process by building one such Macro and laying the groundwork for you to create your own.

I wrote a more extensive explanation of CloudFormation Macros, including a very simple example, [on my site](https://ig.nore.me/2018/11/building-and-testing-cloudformation-macros/). If you're not already familiar with the concept of Macros, I suggest you read that before you begin as it will likely help you understand how some of this works.

## NaclExpander

The Macro we'll be building in this workshop is one I call NaclExpander. This is a Macro that shows how you can easily turn some of the verbose and complicated CloudFormation syntax into something that's a lot easier to work with.

In effect, what it does is expand the existing `AWS::EC2::NetworkAcl` CloudFormation resource into something that contains the versions of the other required resources. So instead of this:

```yaml
  NaclPublic:
    Type: AWS::EC2::NetworkAcl
    Properties:
      VpcId: !Ref VPC

  SubnetANaclPublic:
    Type: AWS::EC2::SubnetNetworkAclAssociation
    Properties:
      NetworkAclId: !Ref NaclPublic
      SubnetId: !Ref SubnetA

  NaclPublicInbound100:
    Type: AWS::EC2::NetworkAclEntry
    Properties:
      Egress: false
      NetworkAclId: !Ref 'NaclPublic'
      Protocol: '6'
      RuleAction: allow
      RuleNumber: '100'
      CidrBlock: '0.0.0.0/0'
      PortRange:
        From: '443'
        To: '443'

  NaclPublicOutbound100:
    Type: AWS::EC2::NetworkAclEntry
    Properties:
      Egress: true
      NetworkAclId: !Ref 'NaclPublic'
      Protocol: '6'
      RuleAction: allow
      RuleNumber: '100'
      CidrBlock: '0.0.0.0/0'
      PortRange:
        From: '443'
        To: '443'
```

you would write this:

```yaml
Resources:
  NaclPublic:
    Type: AWS::EC2::NetworkAcl
    Properties:
      VpcId: !Ref VPC
      Inbound:
        - "100,6,allow,0.0.0.0/0,443"
      Outbound:
        - "100,6,allow,0.0.0.0/0,443"
      Association:
        - SubnetA
```

As you can see, this short version is far more readable (whether you agree with the specific syntax or not).

## Going through the workshop

The workshop itself is fairly straightforward. When you clone this repo out you will be in the `master` branch. This branch only contains this README file and a Makefile. To get started you can checkout the branch `step1`. This branch then contains everything you need for this step as well as a file called `step1.md`. This file will tell you what you need to do and how you can verify that it is working. Afterwards you can then move on to the `step2` branch, and continue like that. The last branch is the one called `finished`, which will contain everything, including a CloudFormation template you can use to test that everything went right.

The included Makefile contains a way to run everything. This includes switching to the different branches (e.g. `make goto-step1`), running the included unit tests (e.g. `make python-test-step1`), running a linter over all CloudFormation templates (`make cfn-lint`), as well as packaging and deploying CloudFormation templates. This is only included to make running commands a bit easier and there is no requirement to use the Makefile.
