# NaclExpander CloudFormation Macro

This Macro allows you to provide an easier way to define your NACL configuration. Instead of creating separate resources for every NACL entry and association, you can easily define them in the NACL itself.

## Syntax

```yaml
Resources:
  NaclPublic:
    Type: AWS::EC2::NetworkAcl
    Properties:
      VpcId: !Ref VPC
      Inbound:
        - "100,6,allow,0.0.0.0/0,443"
        - "110,6,allow,0.0.0.0/0,80"
      Outbound:
        - "100,6,allow,0.0.0.0/0,443"
        - "110,-1,allow,0.0.0.0/0,-1"
        - "150,6,allow,0.0.0.0/0,32768-61000"
      Association:
        - SubnetA
        - SubnetB
```

This will generate NACL entries for each of the Inbound and Outbound entries and creating associations to SubnetA and SubnetB.

The syntax for the Inbound and Outbound entries is:

```bash
"rule number,protocol,allow/deny,CIDR,ports"
```

The CIDR can be either IPv4 or IPv6, both are handled and identified correctly. If you provide a single port, that will be used for both the To and From, if you provide a port range (From-To) it will separate them and use them appropriately.

## Usage

Deploy the macro.yml CloudFormation template. This contains the Macro embedded into it. Subsequently you can use it in a template by enabling the NaclExpander transformation.

```yaml
Transform:
  - NaclExpander
```

## cfn-lint

If you use cfn-lint for your templates, the included `cfn-lint-override.json` file adds requirements and support for the Inbound/Outbound/Association properties in a `AWS::EC2::NetworkAcl` resource. Include that (and any other exceptions) in your project and use cfn-lint with `cfn-lint --override-spec path/to/override-file.json path/to/template.yml`.

## Development

Development should be done in the macro.py file, and you can then copy this code into the template. The Macro is written for deployment in the Python 3.7 Lambda, so take that into account.

`test.py` contains the unit tests, and should be updated/run when doing any work (`python3 test.py`).

## TODO

* Support for the ICMP codes and types. There are extra requirements when dealing with ICMP, according to the spec so these need to be available.
