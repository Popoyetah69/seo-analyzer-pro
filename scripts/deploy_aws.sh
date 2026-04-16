#!/bin/bash
# SEO Analyzer Pro - AWS Deployment Script
# Deploy to AWS using CloudFormation

set -e

echo "=========================================="
echo "SEO Analyzer Pro - AWS Deployment"
echo "=========================================="
echo ""

# Check prerequisites
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Install from: https://aws.amazon.com/cli/"
    exit 1
fi

echo "✅ AWS CLI found"
echo ""

# Get inputs
read -p "Enter AWS profile (default): " AWS_PROFILE
read -p "Enter region (us-east-1, eu-west-1, etc): " AWS_REGION
read -p "Enter app name: " APP_NAME
read -p "Enter domain name (optional): " DOMAIN_NAME

AWS_PROFILE=${AWS_PROFILE:-default}
AWS_REGION=${AWS_REGION:-us-east-1}

echo ""
echo "=========================================="
echo "Creating CloudFormation Stack..."
echo "=========================================="
echo ""

# Create CloudFormation template
cat > cloudformation-template.yaml <<'EOF'
AWSTemplateFormatVersion: '2010-09-09'
Description: 'SEO Analyzer Pro - Complete Stack'

Parameters:
  AppName:
    Type: String
    Default: seo-analyzer-pro
  
  InstanceType:
    Type: String
    Default: t3.micro

Resources:
  # VPC
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${AppName}-vpc'

  # Security Group
  SecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: SEO Analyzer Pro Security Group
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 5432
          ToPort: 5432
          CidrIp: 10.0.0.0/16

  # RDS Database
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      Engine: postgres
      EngineVersion: '14.6'
      DBInstanceClass: db.t3.micro
      AllocatedStorage: '20'
      StorageType: gp2
      DBName: seoanalyzer
      MasterUsername: admin
      MasterUserPassword: !Sub '{{resolve:secretsmanager:${DBSecret}:SecretString:password}}'
      VpcSecurityGroups:
        - !Ref SecurityGroup
      Tags:
        - Key: Name
          Value: !Sub '${AppName}-db'

  # Application Load Balancer
  LoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub '${AppName}-alb'
      Subnets: !GetAZs ''
      SecurityGroups:
        - !Ref SecurityGroup
      Tags:
        - Key: Name
          Value: !Sub '${AppName}-alb'

  # ECS Cluster
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub '${AppName}-cluster'

  # CloudFront Distribution
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        DefaultCacheBehavior:
          AllowedMethods:
            - GET
            - HEAD
          CachePolicyId: 658327ea-f89d-4fab-a63d-7e88639e58f6
          OriginRequestPolicyId: 216adef5-5c7f-47e4-b989-5492eafa07d3
          TargetOriginId: backend
          ViewerProtocolPolicy: redirect-to-https
        Enabled: true
        Origins:
          - Id: backend
            DomainName: !GetAtt LoadBalancer.DNSName
            CustomOriginConfig:
              HTTPPort: 80
              OriginProtocolPolicy: http-only

Outputs:
  LoadBalancerDNS:
    Description: DNS name of load balancer
    Value: !GetAtt LoadBalancer.DNSName
  
  DatabaseEndpoint:
    Description: RDS endpoint
    Value: !GetAtt DBInstance.Endpoint.Address

EOF

# Deploy stack
echo "Deploying CloudFormation stack..."

aws cloudformation create-stack \
  --stack-name "$APP_NAME" \
  --template-body file://cloudformation-template.yaml \
  --parameters ParameterKey=AppName,ParameterValue="$APP_NAME" \
  --region "$AWS_REGION" \
  --profile "$AWS_PROFILE"

echo "⏳ Stack creation initiated..."
echo ""
echo "Monitor progress:"
echo "  aws cloudformation describe-stacks --stack-name $APP_NAME --region $AWS_REGION --profile $AWS_PROFILE"
echo ""
echo "Estimated monthly cost:"
echo "  • EC2: $5-15"
echo "  • RDS: $15-25"
echo "  • Load Balancer: $16"
echo "  • CloudFront: $1-5"
echo "  Total: $37-61/month"
