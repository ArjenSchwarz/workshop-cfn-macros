# Step 3: Create NACL Entries

In this step we build upon our knowledge from the previous step to build the entries for the NACL. If you haven't done so yet, make sure you switch your local copy to this same branch by running the command `git checkout step3`.

## Step 3.1 Create NetworkAclEntry resources

That means we want our Macro to turn this:

```yaml
  NaclPublic:
    Type: AWS::EC2::NetworkAcl
    Properties:
      VpcId: !Ref VPC
      Inbound:
        - "100,6,allow,0.0.0.0/0,443"
      Outbound:
        - "100,6,allow,0.0.0.0/0,443"
```

into:

```yaml
  NaclPublic:
    Type: AWS::EC2::NetworkAcl
    Properties:
      VpcId: !Ref VPC
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

While there are more moving parts, such as the need to break apart the entries themselves, this is similar to what you did in step 2. You will need to create the entries and remove the `Inbound` and `Outbound` properties from the `NetworkAcl` resource.

Keep in mind that for readability we've separated the Inbound and Outbound entries, but once transformed the only difference between them is the `Egress` property value. In addition, the naming used for the entries in the tests is `$Nacl$Direction$Rulenumber` which results in the names used in the example above.

The syntax for the Inbound and Outbound entries is:

```bash
"rule number,protocol,allow/deny,CIDR,ports"
```

## Proceed to Step 4

Once you have the above working, please [proceed to step 4](https://github.com/ArjenSchwarz/workshop-cfn-macros/blob/step4/step4.md).
