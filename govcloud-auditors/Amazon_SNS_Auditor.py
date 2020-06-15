# This file is part of ElectricEye.

# ElectricEye is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ElectricEye is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with ElectricEye.
# If not, see https://github.com/jonrau1/ElectricEye/blob/master/LICENSE.

import datetime
import json
import os
import boto3
from auditors.Auditor import Auditor

# import boto3 clients
sns = boto3.client("sns")
sts = boto3.client("sts")
# create region variable
awsRegion = os.environ["AWS_REGION"]


class SNSTopicEncryptionCheck(Auditor):
    def execute(self):
        awsAccountId = sts.get_caller_identity()["Account"]
        # loop through SNS topics
        response = sns.list_topics()
        mySnsTopics = response["Topics"]
        for topic in mySnsTopics:
            topicarn = str(topic["TopicArn"])
            topicName = topicarn.replace(
                "arn:aws-us-gov:sns:" + awsRegion + ":" + awsAccountId + ":", ""
            )
            response = sns.get_topic_attributes(TopicArn=topicarn)
            iso8601Time = (
                datetime.datetime.utcnow()
                .replace(tzinfo=datetime.timezone.utc)
                .isoformat()
            )
            try:
                # this is a passing check
                encryptionCheck = str(response["Attributes"]["KmsMasterKeyId"])
                finding = {
                    "SchemaVersion": "2018-10-08",
                    "Id": topicarn + "/sns-topic-encryption-check",
                    "ProductArn": "arn:aws-us-gov:securityhub:"
                    + awsRegion
                    + ":"
                    + awsAccountId
                    + ":product/"
                    + awsAccountId
                    + "/default",
                    "GeneratorId": topicarn,
                    "AwsAccountId": awsAccountId,
                    "Types": [
                        "Software and Configuration Checks/AWS Security Best Practices",
                        "Effects/Data Exposure",
                    ],
                    "FirstObservedAt": iso8601Time,
                    "CreatedAt": iso8601Time,
                    "UpdatedAt": iso8601Time,
                    "Severity": {"Label": "INFORMATIONAL"},
                    "Confidence": 99,
                    "Title": "[SNS.1] SNS topics should be encrypted",
                    "Description": "SNS topic " + topicName + " is encrypted.",
                    "Remediation": {
                        "Recommendation": {
                            "Text": "For more information on SNS encryption at rest and how to configure it refer to the Encryption at Rest section of the Amazon Simple Notification Service Developer Guide.",
                            "Url": "https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html",
                        }
                    },
                    "ProductFields": {"Product Name": "ElectricEye"},
                    "Resources": [
                        {
                            "Type": "AwsSnsTopic",
                            "Id": topicarn,
                            "Partition": "aws-us-gov",
                            "Region": awsRegion,
                            "Details": {"AwsSnsTopic": {"TopicName": topicName}},
                        }
                    ],
                    "Compliance": {
                        "Status": "PASSED",
                        "RelatedRequirements": [
                            "NIST CSF PR.DS-1",
                            "NIST SP 800-53 MP-8",
                            "NIST SP 800-53 SC-12",
                            "NIST SP 800-53 SC-28",
                            "AICPA TSC CC6.1",
                            "ISO 27001:2013 A.8.2.3",
                        ],
                    },
                    "Workflow": {"Status": "RESOLVED"},
                    "RecordState": "ARCHIVED",
                }
                yield finding
            except:
                finding = {
                    "SchemaVersion": "2018-10-08",
                    "Id": topicarn + "/sns-topic-encryption-check",
                    "ProductArn": "arn:aws-us-gov:securityhub:"
                    + awsRegion
                    + ":"
                    + awsAccountId
                    + ":product/"
                    + awsAccountId
                    + "/default",
                    "GeneratorId": topicarn,
                    "AwsAccountId": awsAccountId,
                    "Types": [
                        "Software and Configuration Checks/AWS Security Best Practices",
                        "Effects/Data Exposure",
                    ],
                    "FirstObservedAt": iso8601Time,
                    "CreatedAt": iso8601Time,
                    "UpdatedAt": iso8601Time,
                    "Severity": {"Label": "HIGH"},
                    "Confidence": 99,
                    "Title": "[SNS.1] SNS topics should be encrypted",
                    "Description": "SNS topic "
                    + topicName
                    + " is not encrypted. Refer to the remediation instructions to remediate this behavior",
                    "Remediation": {
                        "Recommendation": {
                            "Text": "For more information on SNS encryption at rest and how to configure it refer to the Encryption at Rest section of the Amazon Simple Notification Service Developer Guide.",
                            "Url": "https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html",
                        }
                    },
                    "ProductFields": {"Product Name": "ElectricEye"},
                    "Resources": [
                        {
                            "Type": "AwsSnsTopic",
                            "Id": topicarn,
                            "Partition": "aws-us-gov",
                            "Region": awsRegion,
                            "Details": {"AwsSnsTopic": {"TopicName": topicName}},
                        }
                    ],
                    "Compliance": {
                        "Status": "FAILED",
                        "RelatedRequirements": [
                            "NIST CSF PR.DS-1",
                            "NIST SP 800-53 MP-8",
                            "NIST SP 800-53 SC-12",
                            "NIST SP 800-53 SC-28",
                            "AICPA TSC CC6.1",
                            "ISO 27001:2013 A.8.2.3",
                        ],
                    },
                    "Workflow": {"Status": "NEW"},
                    "RecordState": "ACTIVE",
                }
                yield finding


class SNSHTTPEncryptionCheck(Auditor):
    def execute(self):
        awsAccountId = sts.get_caller_identity()["Account"]
        # loop through SNS topics
        response = sns.list_topics()
        mySnsTopics = response["Topics"]
        for topic in mySnsTopics:
            topicarn = str(topic["TopicArn"])
            topicName = topicarn.replace(
                "arn:aws-us-gov:sns:" + awsRegion + ":" + awsAccountId + ":", ""
            )
            response = sns.list_subscriptions_by_topic(TopicArn=topicarn)
            mySubs = response["Subscriptions"]
            for subscriptions in mySubs:
                subProtocol = str(subscriptions["Protocol"])
                iso8601Time = (
                    datetime.datetime.utcnow()
                    .replace(tzinfo=datetime.timezone.utc)
                    .isoformat()
                )
                if subProtocol == "http":
                    finding = {
                        "SchemaVersion": "2018-10-08",
                        "Id": topicarn + "/sns-http-subscription-check",
                        "ProductArn": "arn:aws-us-gov:securityhub:"
                        + awsRegion
                        + ":"
                        + awsAccountId
                        + ":product/"
                        + awsAccountId
                        + "/default",
                        "GeneratorId": topicarn,
                        "AwsAccountId": awsAccountId,
                        "Types": [
                            "Software and Configuration Checks/AWS Security Best Practices",
                            "Effects/Data Exposure",
                        ],
                        "FirstObservedAt": iso8601Time,
                        "CreatedAt": iso8601Time,
                        "UpdatedAt": iso8601Time,
                        "Severity": {"Label": "HIGH"},
                        "Confidence": 99,
                        "Title": "[SNS.2] SNS topics should not use HTTP subscriptions",
                        "Description": "SNS topic "
                        + topicName
                        + " has a HTTP subscriber. Refer to the remediation instructions to remediate this behavior",
                        "Remediation": {
                            "Recommendation": {
                                "Text": "For more information on SNS encryption in transit refer to the Enforce Encryption of Data in Transit section of the Amazon Simple Notification Service Developer Guide.",
                                "Url": "https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html#enforce-encryption-data-in-transit",
                            }
                        },
                        "ProductFields": {"Product Name": "ElectricEye"},
                        "Resources": [
                            {
                                "Type": "AwsSnsTopic",
                                "Id": topicarn,
                                "Partition": "aws-us-gov",
                                "Region": awsRegion,
                                "Details": {"AwsSnsTopic": {"TopicName": topicName}},
                            }
                        ],
                        "Compliance": {
                            "Status": "FAILED",
                            "RelatedRequirements": [
                                "NIST CSF ID.AM-2",
                                "NIST SP 800-53 CM-8",
                                "NIST SP 800-53 PM-5",
                                "AICPA TSC CC3.2",
                                "AICPA TSC CC6.1",
                                "ISO 27001:2013 A.8.1.1",
                                "ISO 27001:2013 A.8.1.2",
                                "ISO 27001:2013 A.12.5.1",
                            ],
                        },
                        "Workflow": {"Status": "NEW"},
                        "RecordState": "ACTIVE",
                    }
                    yield finding
                else:
                    finding = {
                        "SchemaVersion": "2018-10-08",
                        "Id": topicarn + "/sns-http-subscription-check",
                        "ProductArn": "arn:aws-us-gov:securityhub:"
                        + awsRegion
                        + ":"
                        + awsAccountId
                        + ":product/"
                        + awsAccountId
                        + "/default",
                        "GeneratorId": topicarn,
                        "AwsAccountId": awsAccountId,
                        "Types": [
                            "Software and Configuration Checks/AWS Security Best Practices",
                            "Effects/Data Exposure",
                        ],
                        "FirstObservedAt": iso8601Time,
                        "CreatedAt": iso8601Time,
                        "UpdatedAt": iso8601Time,
                        "Severity": {"Label": "INFORMATIONAL"},
                        "Confidence": 99,
                        "Title": "[SNS.2] SNS topics should not use HTTP subscriptions",
                        "Description": "SNS topic "
                        + topicName
                        + " does not have a HTTP subscriber.",
                        "Remediation": {
                            "Recommendation": {
                                "Text": "For more information on SNS encryption in transit refer to the Enforce Encryption of Data in Transit section of the Amazon Simple Notification Service Developer Guide.",
                                "Url": "https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html#enforce-encryption-data-in-transit",
                            }
                        },
                        "ProductFields": {"Product Name": "ElectricEye"},
                        "Resources": [
                            {
                                "Type": "AwsSnsTopic",
                                "Id": topicarn,
                                "Partition": "aws-us-gov",
                                "Region": awsRegion,
                                "Details": {"AwsSnsTopic": {"TopicName": topicName}},
                            }
                        ],
                        "Compliance": {
                            "Status": "PASSED",
                            "RelatedRequirements": [
                                "NIST CSF ID.AM-2",
                                "NIST SP 800-53 CM-8",
                                "NIST SP 800-53 PM-5",
                                "AICPA TSC CC3.2",
                                "AICPA TSC CC6.1",
                                "ISO 27001:2013 A.8.1.1",
                                "ISO 27001:2013 A.8.1.2",
                                "ISO 27001:2013 A.12.5.1",
                            ],
                        },
                        "Workflow": {"Status": "RESOLVED"},
                        "RecordState": "ARCHIVED",
                    }
                    yield finding


class SNSPublicAccessCheck(Auditor):
    def execute(self):
        awsAccountId = sts.get_caller_identity()["Account"]
        # loop through SNS topics
        response = sns.list_topics()
        mySnsTopics = response["Topics"]
        for topic in mySnsTopics:
            topicarn = str(topic["TopicArn"])
            topicName = topicarn.replace(
                "arn:aws-us-gov:sns:" + awsRegion + ":" + awsAccountId + ":", ""
            )
            response = sns.get_topic_attributes(TopicArn=topicarn)
            statement_json = response["Attributes"]["Policy"]
            statement = json.loads(statement_json)
            fail = False
            # this results in one finding per topic instead of one finding per statement
            for sid in statement["Statement"]:
                access = sid["Principal"].get("aws-us-gov", None)
                iso8601Time = (
                    datetime.datetime.utcnow()
                    .replace(tzinfo=datetime.timezone.utc)
                    .isoformat()
                )
                if access != "*" or (access == "*" and "Condition" in sid):
                    continue
                else:
                    fail = True
                    break
            if not fail:
                finding = {
                    "SchemaVersion": "2018-10-08",
                    "Id": topicarn + "/sns-public-access-check",
                    "ProductArn": "arn:aws-us-gov:securityhub:"
                    + awsRegion
                    + ":"
                    + awsAccountId
                    + ":product/"
                    + awsAccountId
                    + "/default",
                    "GeneratorId": topicarn,
                    "AwsAccountId": awsAccountId,
                    "Types": [
                        "Software and Configuration Checks/AWS Security Best Practices",
                        "Effects/Data Exposure",
                    ],
                    "FirstObservedAt": iso8601Time,
                    "CreatedAt": iso8601Time,
                    "UpdatedAt": iso8601Time,
                    "Severity": {"Label": "INFORMATIONAL"},
                    "Confidence": 75,  # The Condition may not effectively limit access
                    "Title": "[SNS.3] SNS topics should not have public access",
                    "Description": "SNS topic "
                    + topicName
                    + " does not have public access or limited by a Condition. Refer to the remediation instructions to review sns access policy",
                    "Remediation": {
                        "Recommendation": {
                            "Text": "For more information on SNS Access Policy Best Practices refer to Amazons Best Practice rules for Amazon SNS.",
                            "Url": "https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html#ensure-topics-not-publicly-accessible",
                        }
                    },
                    "ProductFields": {"Product Name": "ElectricEye"},
                    "Resources": [
                        {
                            "Type": "AwsSnsTopic",
                            "Id": topicarn,
                            "Partition": "aws-us-gov",
                            "Region": awsRegion,
                            "Details": {"AwsSnsTopic": {"TopicName": topicName}},
                        }
                    ],
                    "Compliance": {
                        "Status": "PASSED",
                        "RelatedRequirements": [
                            "NIST CSF PR.AC-3",
                            "NIST SP 800-53 AC-1",
                            "NIST SP 800-53 AC-17",
                            "NIST SP 800-53 AC-19",
                            "NIST SP 800-53 AC-20",
                            "NIST SP 800-53 SC-15",
                            "AICPA TSC CC6.6",
                            "ISO 27001:2013 A.6.2.1",
                            "ISO 27001:2013 A.6.2.2",
                            "ISO 27001:2013 A.11.2.6",
                            "ISO 27001:2013 A.13.1.1",
                            "ISO 27001:2013 A.13.2.1",
                        ],
                    },
                    "Workflow": {"Status": "RESOLVED"},
                    "RecordState": "ARCHIVED",
                }
                yield finding
            else:
                finding = {
                    "SchemaVersion": "2018-10-08",
                    "Id": topicarn + "/sns-public-access-check",
                    "ProductArn": "arn:aws-us-gov:securityhub:"
                    + awsRegion
                    + ":"
                    + awsAccountId
                    + ":product/"
                    + awsAccountId
                    + "/default",
                    "GeneratorId": topicarn,
                    "AwsAccountId": awsAccountId,
                    "Types": [
                        "Software and Configuration Checks/AWS Security Best Practices",
                        "Effects/Data Exposure",
                    ],
                    "FirstObservedAt": iso8601Time,
                    "CreatedAt": iso8601Time,
                    "UpdatedAt": iso8601Time,
                    "Severity": {"Label": "HIGH"},
                    "Confidence": 99,
                    "Title": "[SNS.3] SNS topics should not have public access",
                    "Description": "SNS topic "
                    + topicName
                    + " has public access. Refer to the remediation instructions to remediate this behavior",
                    "Remediation": {
                        "Recommendation": {
                            "Text": "For more information on SNS Access Policy Best Practices refer to Amazons Best Practice rules for Amazon SNS.",
                            "Url": "https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html#ensure-topics-not-publicly-accessible",
                        }
                    },
                    "ProductFields": {"Product Name": "ElectricEye"},
                    "Resources": [
                        {
                            "Type": "AwsSnsTopic",
                            "Id": topicarn,
                            "Partition": "aws-us-gov",
                            "Region": awsRegion,
                            "Details": {"AwsSnsTopic": {"TopicName": topicName}},
                        }
                    ],
                    "Compliance": {
                        "Status": "FAILED",
                        "RelatedRequirements": [
                            "NIST CSF PR.AC-3",
                            "NIST SP 800-53 AC-1",
                            "NIST SP 800-53 AC-17",
                            "NIST SP 800-53 AC-19",
                            "NIST SP 800-53 AC-20",
                            "NIST SP 800-53 SC-15",
                            "AICPA TSC CC6.6",
                            "ISO 27001:2013 A.6.2.1",
                            "ISO 27001:2013 A.6.2.2",
                            "ISO 27001:2013 A.11.2.6",
                            "ISO 27001:2013 A.13.1.1",
                            "ISO 27001:2013 A.13.2.1",
                        ],
                    },
                    "Workflow": {"Status": "NEW"},
                    "RecordState": "ACTIVE",
                }
                yield finding


class SNSCrossAccountCheck(Auditor):
    def execute(self):
        awsAccountId = sts.get_caller_identity()["Account"]
        # loop through SNS topics
        response = sns.list_topics()
        mySnsTopics = response["Topics"]
        for topic in mySnsTopics:
            topicarn = str(topic["TopicArn"])
            topicName = topicarn.replace(
                "arn:aws-us-gov:sns:" + awsRegion + ":" + awsAccountId + ":", ""
            )
            response = sns.get_topic_attributes(TopicArn=topicarn)
            myPolicy_json = str(response["Attributes"]["Policy"])
            myPolicy = json.loads(myPolicy_json)
            fail = False
            for statement in myPolicy["Statement"]:
                principal = statement["Principal"].get("aws-us-gov", None)
                iso8601Time = (
                    datetime.datetime.utcnow()
                    .replace(tzinfo=datetime.timezone.utc)
                    .isoformat()
                )
                if principal and principal != "*":
                    if not principal.isdigit():
                        # This assumes if it is not a digit that it must be an arn.
                        # not sure if this is a safe assumption.
                        principal = principal.split(":")[4]
                    if principal == awsAccountId:
                        continue
                    else:
                        fail = True
                        break
            if not fail:
                finding = {
                    "SchemaVersion": "2018-10-08",
                    "Id": topicarn + "/sns-cross-account-check",
                    "ProductArn": "arn:aws-us-gov:securityhub:"
                    + awsRegion
                    + ":"
                    + awsAccountId
                    + ":product/"
                    + awsAccountId
                    + "/default",
                    "GeneratorId": topicarn,
                    "AwsAccountId": awsAccountId,
                    "Types": [
                        "Software and Configuration Checks/AWS Security Best Practices",
                        "Effects/Data Exposure",
                    ],
                    "FirstObservedAt": iso8601Time,
                    "CreatedAt": iso8601Time,
                    "UpdatedAt": iso8601Time,
                    "Severity": {"Label": "INFORMATIONAL"},
                    "Confidence": 99,
                    "Title": "[SNS.4] SNS topics should not allow cross-account access",
                    "Description": "SNS topic "
                    + topicName
                    + " does not have cross-account access.",
                    "Remediation": {
                        "Recommendation": {
                            "Text": "For more information on SNS best practices refer to the Amazon SNS security best practices section of the Amazon Simple Notification Service Developer Guide.",
                            "Url": "https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html#enforce-encryption-data-in-transit",
                        }
                    },
                    "ProductFields": {"Product Name": "ElectricEye"},
                    "Resources": [
                        {
                            "Type": "AwsSnsTopic",
                            "Id": topicarn,
                            "Partition": "aws-us-gov",
                            "Region": awsRegion,
                            "Details": {
                                "AwsSnsTopic": {"TopicName": topicName}
                            },
                        }
                    ],
                    "Compliance": {
                        "Status": "PASSED",
                        "RelatedRequirements": [
                            "NIST CSF PR.AC-3",
                            "NIST SP 800-53 AC-1",
                            "NIST SP 800-53 AC-17",
                            "NIST SP 800-53 AC-19",
                            "NIST SP 800-53 AC-20",
                            "NIST SP 800-53 SC-15",
                            "AICPA TSC CC6.6",
                            "ISO 27001:2013 A.6.2.1",
                            "ISO 27001:2013 A.6.2.2",
                            "ISO 27001:2013 A.11.2.6",
                            "ISO 27001:2013 A.13.1.1",
                            "ISO 27001:2013 A.13.2.1",
                        ],
                    },
                    "Workflow": {"Status": "RESOLVED"},
                    "RecordState": "ARCHIVED",
                }
                yield finding
            else:
                finding = {
                    "SchemaVersion": "2018-10-08",
                    "Id": topicarn + "/sns-cross-account-check",
                    "ProductArn": "arn:aws-us-gov:securityhub:"
                    + awsRegion
                    + ":"
                    + awsAccountId
                    + ":product/"
                    + awsAccountId
                    + "/default",
                    "GeneratorId": topicarn,
                    "AwsAccountId": awsAccountId,
                    "Types": [
                        "Software and Configuration Checks/AWS Security Best Practices",
                        "Effects/Data Exposure",
                    ],
                    "FirstObservedAt": iso8601Time,
                    "CreatedAt": iso8601Time,
                    "UpdatedAt": iso8601Time,
                    "Severity": {"Label": "Low"},
                    "Confidence": 99,
                    "Title": "[SNS.4] SNS topics should not allow cross-account access",
                    "Description": "SNS topic "
                    + topicName
                    + " has cross-account access.",
                    "Remediation": {
                        "Recommendation": {
                            "Text": "For more information on SNS best practices refer to the Amazon SNS security best practices section of the Amazon Simple Notification Service Developer Guide.",
                            "Url": "https://docs.aws.amazon.com/sns/latest/dg/sns-security-best-practices.html#enforce-encryption-data-in-transit",
                        }
                    },
                    "ProductFields": {"Product Name": "ElectricEye"},
                    "Resources": [
                        {
                            "Type": "AwsSnsTopic",
                            "Id": topicarn,
                            "Partition": "aws-us-gov",
                            "Region": awsRegion,
                            "Details": {
                                "AwsSnsTopic": {"TopicName": topicName}
                            },
                        }
                    ],
                    "Compliance": {
                        "Status": "FAILED",
                        "RelatedRequirements": [
                            "NIST CSF PR.AC-3",
                            "NIST SP 800-53 AC-1",
                            "NIST SP 800-53 AC-17",
                            "NIST SP 800-53 AC-19",
                            "NIST SP 800-53 AC-20",
                            "NIST SP 800-53 SC-15",
                            "AICPA TSC CC6.6",
                            "ISO 27001:2013 A.6.2.1",
                            "ISO 27001:2013 A.6.2.2",
                            "ISO 27001:2013 A.11.2.6",
                            "ISO 27001:2013 A.13.1.1",
                            "ISO 27001:2013 A.13.2.1",
                        ],
                    },
                    "Workflow": {"Status": "NEW"},
                    "RecordState": "ACTIVE",
                }
                yield finding
