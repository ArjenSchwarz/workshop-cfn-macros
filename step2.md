# Step 2: Create associations

In this step we will make our Macro do some actual work! If you haven't done so yet, make sure you switch your local copy to this same branch by running the command `git checkout step2`.

## 2.1 Associate a NetworkAcl object to Subnets

In this step we want to ensure our Macro can turn this:

```yaml
  NaclPublic:
    Type: AWS::EC2::NetworkAcl
    Properties:
      VpcId: !Ref VPC
      Association:
        - SubnetA
```

into:

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
```

This requires your Lambda function to create new resources, so how do we do that?

When looking at the fragment in step 1 you may have noticed that all the resources are accessible through the Resources part of the fragment. And while we simply passed through everything that came in there, we can obviously modify the fragment as it comes through. So, that is what you want to do here by adding a `AWS::EC2::SubnetNetworkAclAssociation` for every item in the `Association` property of our `AWS::EC2::NetworkAcl`, and eventually removing the `Association` property itself (as that is not accepted by CloudFormation).

One important note, remember that every resource in CloudFormation needs its own name. The included tests all assume that you will therefore name the associations as `$Subnet$Nacl`, which means in the above example you give the association between `SubnetA` and `NaclPublic` the name `SubnetANaclPublic`. If you don't want to use the tests you can use any naming standard you yourself enjoy, just keep in mind that they have to stay the same between different deployments of the same template.

## Proceed to Step 3

Once you have the above working, please proceed to [step 3](https://github.com/ArjenSchwarz/workshop-cfn-macros/blob/step3/step3.md).
