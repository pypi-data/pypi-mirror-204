"""
Type annotations for connect service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/type_defs/)

Usage::

    ```python
    from mypy_boto3_connect.type_defs import ActionSummaryTypeDef

    data: ActionSummaryTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    ActionTypeType,
    AgentStatusStateType,
    AgentStatusTypeType,
    BehaviorTypeType,
    ChannelType,
    ContactFlowModuleStateType,
    ContactFlowModuleStatusType,
    ContactFlowStateType,
    ContactFlowTypeType,
    ContactInitiationMethodType,
    ContactStateType,
    CurrentMetricNameType,
    DirectoryTypeType,
    EventSourceNameType,
    GroupingType,
    HierarchyGroupMatchTypeType,
    HistoricalMetricNameType,
    HoursOfOperationDaysType,
    InstanceAttributeTypeType,
    InstanceStatusType,
    InstanceStorageResourceTypeType,
    IntegrationTypeType,
    LexVersionType,
    MonitorCapabilityType,
    ParticipantRoleType,
    ParticipantTimerTypeType,
    PhoneNumberCountryCodeType,
    PhoneNumberTypeType,
    PhoneNumberWorkflowStatusType,
    PhoneTypeType,
    QueueStatusType,
    QueueTypeType,
    QuickConnectTypeType,
    ReferenceStatusType,
    ReferenceTypeType,
    RehydrationTypeType,
    RulePublishStatusType,
    SortOrderType,
    SourceTypeType,
    StatisticType,
    StorageTypeType,
    StringComparisonTypeType,
    TaskTemplateFieldTypeType,
    TaskTemplateStatusType,
    TimerEligibleParticipantRolesType,
    TrafficDistributionGroupStatusType,
    TrafficTypeType,
    UnitType,
    UseCaseTypeType,
    VocabularyLanguageCodeType,
    VocabularyStateType,
    VoiceRecordingTrackType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ActionSummaryTypeDef",
    "QueueReferenceTypeDef",
    "AgentInfoTypeDef",
    "AgentStatusReferenceTypeDef",
    "AgentStatusSummaryTypeDef",
    "AgentStatusTypeDef",
    "AnswerMachineDetectionConfigTypeDef",
    "AssociateApprovedOriginRequestRequestTypeDef",
    "LexBotTypeDef",
    "LexV2BotTypeDef",
    "AssociateDefaultVocabularyRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AssociateLambdaFunctionRequestRequestTypeDef",
    "AssociatePhoneNumberContactFlowRequestRequestTypeDef",
    "AssociateQueueQuickConnectsRequestRequestTypeDef",
    "AssociateSecurityKeyRequestRequestTypeDef",
    "AttachmentReferenceTypeDef",
    "AttributeTypeDef",
    "AvailableNumberSummaryTypeDef",
    "ChatMessageTypeDef",
    "ChatStreamingConfigurationTypeDef",
    "ClaimPhoneNumberRequestRequestTypeDef",
    "PhoneNumberStatusTypeDef",
    "ContactFilterTypeDef",
    "ContactFlowModuleSummaryTypeDef",
    "ContactFlowModuleTypeDef",
    "ContactFlowSummaryTypeDef",
    "ContactFlowTypeDef",
    "QueueInfoTypeDef",
    "WisdomInfoTypeDef",
    "TagConditionTypeDef",
    "CreateAgentStatusRequestRequestTypeDef",
    "CreateContactFlowModuleRequestRequestTypeDef",
    "CreateContactFlowRequestRequestTypeDef",
    "CreateInstanceRequestRequestTypeDef",
    "CreateIntegrationAssociationRequestRequestTypeDef",
    "ParticipantDetailsToAddTypeDef",
    "ParticipantTokenCredentialsTypeDef",
    "OutboundCallerConfigTypeDef",
    "RuleTriggerEventSourceTypeDef",
    "CreateSecurityProfileRequestRequestTypeDef",
    "CreateTrafficDistributionGroupRequestRequestTypeDef",
    "CreateUseCaseRequestRequestTypeDef",
    "CreateUserHierarchyGroupRequestRequestTypeDef",
    "UserIdentityInfoTypeDef",
    "UserPhoneConfigTypeDef",
    "CreateVocabularyRequestRequestTypeDef",
    "CredentialsTypeDef",
    "CrossChannelBehaviorTypeDef",
    "CurrentMetricTypeDef",
    "CurrentMetricSortCriteriaTypeDef",
    "DateReferenceTypeDef",
    "DefaultVocabularyTypeDef",
    "DeleteContactFlowModuleRequestRequestTypeDef",
    "DeleteContactFlowRequestRequestTypeDef",
    "DeleteHoursOfOperationRequestRequestTypeDef",
    "DeleteInstanceRequestRequestTypeDef",
    "DeleteIntegrationAssociationRequestRequestTypeDef",
    "DeleteQuickConnectRequestRequestTypeDef",
    "DeleteRuleRequestRequestTypeDef",
    "DeleteSecurityProfileRequestRequestTypeDef",
    "DeleteTaskTemplateRequestRequestTypeDef",
    "DeleteTrafficDistributionGroupRequestRequestTypeDef",
    "DeleteUseCaseRequestRequestTypeDef",
    "DeleteUserHierarchyGroupRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeleteVocabularyRequestRequestTypeDef",
    "DescribeAgentStatusRequestRequestTypeDef",
    "DescribeContactFlowModuleRequestRequestTypeDef",
    "DescribeContactFlowRequestRequestTypeDef",
    "DescribeContactRequestRequestTypeDef",
    "DescribeHoursOfOperationRequestRequestTypeDef",
    "DescribeInstanceAttributeRequestRequestTypeDef",
    "DescribeInstanceRequestRequestTypeDef",
    "DescribeInstanceStorageConfigRequestRequestTypeDef",
    "DescribePhoneNumberRequestRequestTypeDef",
    "DescribeQueueRequestRequestTypeDef",
    "DescribeQuickConnectRequestRequestTypeDef",
    "DescribeRoutingProfileRequestRequestTypeDef",
    "DescribeRuleRequestRequestTypeDef",
    "DescribeSecurityProfileRequestRequestTypeDef",
    "SecurityProfileTypeDef",
    "DescribeTrafficDistributionGroupRequestRequestTypeDef",
    "TrafficDistributionGroupTypeDef",
    "DescribeUserHierarchyGroupRequestRequestTypeDef",
    "DescribeUserHierarchyStructureRequestRequestTypeDef",
    "DescribeUserRequestRequestTypeDef",
    "DescribeVocabularyRequestRequestTypeDef",
    "VocabularyTypeDef",
    "RoutingProfileReferenceTypeDef",
    "DisassociateApprovedOriginRequestRequestTypeDef",
    "DisassociateInstanceStorageConfigRequestRequestTypeDef",
    "DisassociateLambdaFunctionRequestRequestTypeDef",
    "DisassociateLexBotRequestRequestTypeDef",
    "DisassociatePhoneNumberContactFlowRequestRequestTypeDef",
    "DisassociateQueueQuickConnectsRequestRequestTypeDef",
    "RoutingProfileQueueReferenceTypeDef",
    "DisassociateSecurityKeyRequestRequestTypeDef",
    "DismissUserContactRequestRequestTypeDef",
    "DistributionTypeDef",
    "EmailReferenceTypeDef",
    "EncryptionConfigTypeDef",
    "EventBridgeActionDefinitionTypeDef",
    "FilterV2TypeDef",
    "FiltersTypeDef",
    "GetContactAttributesRequestRequestTypeDef",
    "GetFederationTokenRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "GetTaskTemplateRequestRequestTypeDef",
    "GetTrafficDistributionRequestRequestTypeDef",
    "HierarchyGroupConditionTypeDef",
    "HierarchyGroupSummaryReferenceTypeDef",
    "HierarchyGroupSummaryTypeDef",
    "HierarchyLevelTypeDef",
    "HierarchyLevelUpdateTypeDef",
    "ThresholdTypeDef",
    "HoursOfOperationTimeSliceTypeDef",
    "HoursOfOperationSummaryTypeDef",
    "InstanceStatusReasonTypeDef",
    "KinesisFirehoseConfigTypeDef",
    "KinesisStreamConfigTypeDef",
    "InstanceSummaryTypeDef",
    "IntegrationAssociationSummaryTypeDef",
    "TaskTemplateFieldIdentifierTypeDef",
    "ListAgentStatusRequestRequestTypeDef",
    "ListApprovedOriginsRequestRequestTypeDef",
    "ListBotsRequestRequestTypeDef",
    "ListContactFlowModulesRequestRequestTypeDef",
    "ListContactFlowsRequestRequestTypeDef",
    "ListContactReferencesRequestRequestTypeDef",
    "ListDefaultVocabulariesRequestRequestTypeDef",
    "ListHoursOfOperationsRequestRequestTypeDef",
    "ListInstanceAttributesRequestRequestTypeDef",
    "ListInstanceStorageConfigsRequestRequestTypeDef",
    "ListInstancesRequestRequestTypeDef",
    "ListIntegrationAssociationsRequestRequestTypeDef",
    "ListLambdaFunctionsRequestRequestTypeDef",
    "ListLexBotsRequestRequestTypeDef",
    "ListPhoneNumbersRequestRequestTypeDef",
    "PhoneNumberSummaryTypeDef",
    "ListPhoneNumbersSummaryTypeDef",
    "ListPhoneNumbersV2RequestRequestTypeDef",
    "ListPromptsRequestRequestTypeDef",
    "PromptSummaryTypeDef",
    "ListQueueQuickConnectsRequestRequestTypeDef",
    "QuickConnectSummaryTypeDef",
    "ListQueuesRequestRequestTypeDef",
    "QueueSummaryTypeDef",
    "ListQuickConnectsRequestRequestTypeDef",
    "ListRoutingProfileQueuesRequestRequestTypeDef",
    "RoutingProfileQueueConfigSummaryTypeDef",
    "ListRoutingProfilesRequestRequestTypeDef",
    "RoutingProfileSummaryTypeDef",
    "ListRulesRequestRequestTypeDef",
    "ListSecurityKeysRequestRequestTypeDef",
    "SecurityKeyTypeDef",
    "ListSecurityProfilePermissionsRequestRequestTypeDef",
    "ListSecurityProfilesRequestRequestTypeDef",
    "SecurityProfileSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTaskTemplatesRequestRequestTypeDef",
    "TaskTemplateMetadataTypeDef",
    "ListTrafficDistributionGroupsRequestRequestTypeDef",
    "TrafficDistributionGroupSummaryTypeDef",
    "ListUseCasesRequestRequestTypeDef",
    "UseCaseTypeDef",
    "ListUserHierarchyGroupsRequestRequestTypeDef",
    "ListUsersRequestRequestTypeDef",
    "UserSummaryTypeDef",
    "MetricFilterV2TypeDef",
    "ThresholdV2TypeDef",
    "MonitorContactRequestRequestTypeDef",
    "NotificationRecipientTypeTypeDef",
    "NumberReferenceTypeDef",
    "ParticipantDetailsTypeDef",
    "ParticipantTimerValueTypeDef",
    "PersistentChatTypeDef",
    "PhoneNumberQuickConnectConfigTypeDef",
    "PutUserStatusRequestRequestTypeDef",
    "QueueQuickConnectConfigTypeDef",
    "StringConditionTypeDef",
    "UserQuickConnectConfigTypeDef",
    "StringReferenceTypeDef",
    "UrlReferenceTypeDef",
    "ReferenceTypeDef",
    "ReleasePhoneNumberRequestRequestTypeDef",
    "ReplicateInstanceRequestRequestTypeDef",
    "ResumeContactRecordingRequestRequestTypeDef",
    "SearchAvailablePhoneNumbersRequestRequestTypeDef",
    "SecurityProfileSearchSummaryTypeDef",
    "SearchVocabulariesRequestRequestTypeDef",
    "VocabularySummaryTypeDef",
    "VoiceRecordingConfigurationTypeDef",
    "StopContactRecordingRequestRequestTypeDef",
    "StopContactRequestRequestTypeDef",
    "StopContactStreamingRequestRequestTypeDef",
    "SuspendContactRecordingRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TransferContactRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAgentStatusRequestRequestTypeDef",
    "UpdateContactAttributesRequestRequestTypeDef",
    "UpdateContactFlowContentRequestRequestTypeDef",
    "UpdateContactFlowMetadataRequestRequestTypeDef",
    "UpdateContactFlowModuleContentRequestRequestTypeDef",
    "UpdateContactFlowModuleMetadataRequestRequestTypeDef",
    "UpdateContactFlowNameRequestRequestTypeDef",
    "UpdateContactScheduleRequestRequestTypeDef",
    "UpdateInstanceAttributeRequestRequestTypeDef",
    "UpdatePhoneNumberRequestRequestTypeDef",
    "UpdateQueueHoursOfOperationRequestRequestTypeDef",
    "UpdateQueueMaxContactsRequestRequestTypeDef",
    "UpdateQueueNameRequestRequestTypeDef",
    "UpdateQueueStatusRequestRequestTypeDef",
    "UpdateQuickConnectNameRequestRequestTypeDef",
    "UpdateRoutingProfileDefaultOutboundQueueRequestRequestTypeDef",
    "UpdateRoutingProfileNameRequestRequestTypeDef",
    "UpdateSecurityProfileRequestRequestTypeDef",
    "UpdateUserHierarchyGroupNameRequestRequestTypeDef",
    "UpdateUserHierarchyRequestRequestTypeDef",
    "UpdateUserRoutingProfileRequestRequestTypeDef",
    "UpdateUserSecurityProfilesRequestRequestTypeDef",
    "UserReferenceTypeDef",
    "UserIdentityInfoLiteTypeDef",
    "RuleSummaryTypeDef",
    "AgentContactReferenceTypeDef",
    "StartOutboundVoiceContactRequestRequestTypeDef",
    "AssociateLexBotRequestRequestTypeDef",
    "AssociateBotRequestRequestTypeDef",
    "DisassociateBotRequestRequestTypeDef",
    "LexBotConfigTypeDef",
    "AssociateInstanceStorageConfigResponseTypeDef",
    "AssociateSecurityKeyResponseTypeDef",
    "ClaimPhoneNumberResponseTypeDef",
    "CreateAgentStatusResponseTypeDef",
    "CreateContactFlowModuleResponseTypeDef",
    "CreateContactFlowResponseTypeDef",
    "CreateHoursOfOperationResponseTypeDef",
    "CreateInstanceResponseTypeDef",
    "CreateIntegrationAssociationResponseTypeDef",
    "CreateQueueResponseTypeDef",
    "CreateQuickConnectResponseTypeDef",
    "CreateRoutingProfileResponseTypeDef",
    "CreateRuleResponseTypeDef",
    "CreateSecurityProfileResponseTypeDef",
    "CreateTaskTemplateResponseTypeDef",
    "CreateTrafficDistributionGroupResponseTypeDef",
    "CreateUseCaseResponseTypeDef",
    "CreateUserHierarchyGroupResponseTypeDef",
    "CreateUserResponseTypeDef",
    "CreateVocabularyResponseTypeDef",
    "DeleteVocabularyResponseTypeDef",
    "DescribeAgentStatusResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetContactAttributesResponseTypeDef",
    "ListAgentStatusResponseTypeDef",
    "ListApprovedOriginsResponseTypeDef",
    "ListLambdaFunctionsResponseTypeDef",
    "ListLexBotsResponseTypeDef",
    "ListSecurityProfilePermissionsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MonitorContactResponseTypeDef",
    "ReplicateInstanceResponseTypeDef",
    "StartChatContactResponseTypeDef",
    "StartContactStreamingResponseTypeDef",
    "StartOutboundVoiceContactResponseTypeDef",
    "StartTaskContactResponseTypeDef",
    "TransferContactResponseTypeDef",
    "UpdatePhoneNumberResponseTypeDef",
    "DescribeInstanceAttributeResponseTypeDef",
    "ListInstanceAttributesResponseTypeDef",
    "SearchAvailablePhoneNumbersResponseTypeDef",
    "StartContactStreamingRequestRequestTypeDef",
    "ClaimedPhoneNumberSummaryTypeDef",
    "UserDataFiltersTypeDef",
    "ListContactFlowModulesResponseTypeDef",
    "DescribeContactFlowModuleResponseTypeDef",
    "ListContactFlowsResponseTypeDef",
    "DescribeContactFlowResponseTypeDef",
    "ContactTypeDef",
    "ControlPlaneTagFilterTypeDef",
    "CreateParticipantRequestRequestTypeDef",
    "CreateParticipantResponseTypeDef",
    "CreateQueueRequestRequestTypeDef",
    "QueueTypeDef",
    "UpdateQueueOutboundCallerConfigRequestRequestTypeDef",
    "UpdateUserIdentityInfoRequestRequestTypeDef",
    "CreateUserRequestRequestTypeDef",
    "UpdateUserPhoneConfigRequestRequestTypeDef",
    "UserTypeDef",
    "GetFederationTokenResponseTypeDef",
    "MediaConcurrencyTypeDef",
    "CurrentMetricDataTypeDef",
    "ListDefaultVocabulariesResponseTypeDef",
    "DescribeSecurityProfileResponseTypeDef",
    "DescribeTrafficDistributionGroupResponseTypeDef",
    "DescribeVocabularyResponseTypeDef",
    "DimensionsTypeDef",
    "DisassociateRoutingProfileQueuesRequestRequestTypeDef",
    "RoutingProfileQueueConfigTypeDef",
    "TelephonyConfigTypeDef",
    "KinesisVideoStreamConfigTypeDef",
    "S3ConfigTypeDef",
    "GetCurrentMetricDataRequestRequestTypeDef",
    "ListAgentStatusRequestListAgentStatusesPaginateTypeDef",
    "ListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef",
    "ListBotsRequestListBotsPaginateTypeDef",
    "ListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef",
    "ListContactFlowsRequestListContactFlowsPaginateTypeDef",
    "ListContactReferencesRequestListContactReferencesPaginateTypeDef",
    "ListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef",
    "ListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef",
    "ListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef",
    "ListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef",
    "ListInstancesRequestListInstancesPaginateTypeDef",
    "ListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef",
    "ListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef",
    "ListLexBotsRequestListLexBotsPaginateTypeDef",
    "ListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef",
    "ListPhoneNumbersV2RequestListPhoneNumbersV2PaginateTypeDef",
    "ListPromptsRequestListPromptsPaginateTypeDef",
    "ListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef",
    "ListQueuesRequestListQueuesPaginateTypeDef",
    "ListQuickConnectsRequestListQuickConnectsPaginateTypeDef",
    "ListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef",
    "ListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef",
    "ListRulesRequestListRulesPaginateTypeDef",
    "ListSecurityKeysRequestListSecurityKeysPaginateTypeDef",
    "ListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef",
    "ListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef",
    "ListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef",
    "ListTrafficDistributionGroupsRequestListTrafficDistributionGroupsPaginateTypeDef",
    "ListUseCasesRequestListUseCasesPaginateTypeDef",
    "ListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef",
    "ListUsersRequestListUsersPaginateTypeDef",
    "SearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef",
    "SearchVocabulariesRequestSearchVocabulariesPaginateTypeDef",
    "HierarchyPathReferenceTypeDef",
    "HierarchyPathTypeDef",
    "ListUserHierarchyGroupsResponseTypeDef",
    "HierarchyStructureTypeDef",
    "HierarchyStructureUpdateTypeDef",
    "HistoricalMetricTypeDef",
    "HoursOfOperationConfigTypeDef",
    "ListHoursOfOperationsResponseTypeDef",
    "InstanceTypeDef",
    "ListInstancesResponseTypeDef",
    "ListIntegrationAssociationsResponseTypeDef",
    "InvisibleFieldInfoTypeDef",
    "ReadOnlyFieldInfoTypeDef",
    "RequiredFieldInfoTypeDef",
    "TaskTemplateDefaultFieldValueTypeDef",
    "TaskTemplateFieldTypeDef",
    "ListPhoneNumbersResponseTypeDef",
    "ListPhoneNumbersV2ResponseTypeDef",
    "ListPromptsResponseTypeDef",
    "ListQueueQuickConnectsResponseTypeDef",
    "ListQuickConnectsResponseTypeDef",
    "ListQueuesResponseTypeDef",
    "ListRoutingProfileQueuesResponseTypeDef",
    "ListRoutingProfilesResponseTypeDef",
    "ListSecurityKeysResponseTypeDef",
    "ListSecurityProfilesResponseTypeDef",
    "ListTaskTemplatesResponseTypeDef",
    "ListTrafficDistributionGroupsResponseTypeDef",
    "ListUseCasesResponseTypeDef",
    "ListUsersResponseTypeDef",
    "MetricV2TypeDef",
    "SendNotificationActionDefinitionTypeDef",
    "ParticipantTimerConfigurationTypeDef",
    "StartChatContactRequestRequestTypeDef",
    "QueueSearchCriteriaTypeDef",
    "RoutingProfileSearchCriteriaTypeDef",
    "SecurityProfileSearchCriteriaTypeDef",
    "UserSearchCriteriaTypeDef",
    "QuickConnectConfigTypeDef",
    "ReferenceSummaryTypeDef",
    "StartTaskContactRequestRequestTypeDef",
    "TaskActionDefinitionTypeDef",
    "UpdateContactRequestRequestTypeDef",
    "SearchSecurityProfilesResponseTypeDef",
    "SearchVocabulariesResponseTypeDef",
    "StartContactRecordingRequestRequestTypeDef",
    "UserSearchSummaryTypeDef",
    "ListRulesResponseTypeDef",
    "ListBotsResponseTypeDef",
    "DescribePhoneNumberResponseTypeDef",
    "GetCurrentUserDataRequestRequestTypeDef",
    "DescribeContactResponseTypeDef",
    "QueueSearchFilterTypeDef",
    "RoutingProfileSearchFilterTypeDef",
    "SecurityProfilesSearchFilterTypeDef",
    "UserSearchFilterTypeDef",
    "DescribeQueueResponseTypeDef",
    "SearchQueuesResponseTypeDef",
    "DescribeUserResponseTypeDef",
    "RoutingProfileTypeDef",
    "UpdateRoutingProfileConcurrencyRequestRequestTypeDef",
    "CurrentMetricResultTypeDef",
    "AssociateRoutingProfileQueuesRequestRequestTypeDef",
    "CreateRoutingProfileRequestRequestTypeDef",
    "UpdateRoutingProfileQueuesRequestRequestTypeDef",
    "GetTrafficDistributionResponseTypeDef",
    "UpdateTrafficDistributionRequestRequestTypeDef",
    "InstanceStorageConfigTypeDef",
    "UserDataTypeDef",
    "HierarchyGroupTypeDef",
    "DescribeUserHierarchyStructureResponseTypeDef",
    "UpdateUserHierarchyStructureRequestRequestTypeDef",
    "GetMetricDataRequestGetMetricDataPaginateTypeDef",
    "GetMetricDataRequestRequestTypeDef",
    "HistoricalMetricDataTypeDef",
    "CreateHoursOfOperationRequestRequestTypeDef",
    "HoursOfOperationTypeDef",
    "UpdateHoursOfOperationRequestRequestTypeDef",
    "DescribeInstanceResponseTypeDef",
    "TaskTemplateConstraintsTypeDef",
    "TaskTemplateDefaultsTypeDef",
    "GetMetricDataV2RequestRequestTypeDef",
    "MetricDataV2TypeDef",
    "ChatParticipantRoleConfigTypeDef",
    "CreateQuickConnectRequestRequestTypeDef",
    "QuickConnectTypeDef",
    "UpdateQuickConnectConfigRequestRequestTypeDef",
    "ListContactReferencesResponseTypeDef",
    "RuleActionTypeDef",
    "SearchUsersResponseTypeDef",
    "SearchQueuesRequestRequestTypeDef",
    "SearchQueuesRequestSearchQueuesPaginateTypeDef",
    "SearchRoutingProfilesRequestRequestTypeDef",
    "SearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef",
    "SearchSecurityProfilesRequestRequestTypeDef",
    "SearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef",
    "SearchUsersRequestRequestTypeDef",
    "SearchUsersRequestSearchUsersPaginateTypeDef",
    "DescribeRoutingProfileResponseTypeDef",
    "SearchRoutingProfilesResponseTypeDef",
    "GetCurrentMetricDataResponseTypeDef",
    "AssociateInstanceStorageConfigRequestRequestTypeDef",
    "DescribeInstanceStorageConfigResponseTypeDef",
    "ListInstanceStorageConfigsResponseTypeDef",
    "UpdateInstanceStorageConfigRequestRequestTypeDef",
    "GetCurrentUserDataResponseTypeDef",
    "DescribeUserHierarchyGroupResponseTypeDef",
    "HistoricalMetricResultTypeDef",
    "DescribeHoursOfOperationResponseTypeDef",
    "CreateTaskTemplateRequestRequestTypeDef",
    "GetTaskTemplateResponseTypeDef",
    "UpdateTaskTemplateRequestRequestTypeDef",
    "UpdateTaskTemplateResponseTypeDef",
    "MetricResultV2TypeDef",
    "UpdateParticipantRoleConfigChannelInfoTypeDef",
    "DescribeQuickConnectResponseTypeDef",
    "CreateRuleRequestRequestTypeDef",
    "RuleTypeDef",
    "UpdateRuleRequestRequestTypeDef",
    "GetMetricDataResponseTypeDef",
    "GetMetricDataV2ResponseTypeDef",
    "UpdateParticipantRoleConfigRequestRequestTypeDef",
    "DescribeRuleResponseTypeDef",
)

ActionSummaryTypeDef = TypedDict(
    "ActionSummaryTypeDef",
    {
        "ActionType": ActionTypeType,
    },
)

QueueReferenceTypeDef = TypedDict(
    "QueueReferenceTypeDef",
    {
        "Id": str,
        "Arn": str,
    },
    total=False,
)

AgentInfoTypeDef = TypedDict(
    "AgentInfoTypeDef",
    {
        "Id": str,
        "ConnectedToAgentTimestamp": datetime,
    },
    total=False,
)

AgentStatusReferenceTypeDef = TypedDict(
    "AgentStatusReferenceTypeDef",
    {
        "StatusStartTimestamp": datetime,
        "StatusArn": str,
        "StatusName": str,
    },
    total=False,
)

AgentStatusSummaryTypeDef = TypedDict(
    "AgentStatusSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Type": AgentStatusTypeType,
    },
    total=False,
)

AgentStatusTypeDef = TypedDict(
    "AgentStatusTypeDef",
    {
        "AgentStatusARN": str,
        "AgentStatusId": str,
        "Name": str,
        "Description": str,
        "Type": AgentStatusTypeType,
        "DisplayOrder": int,
        "State": AgentStatusStateType,
        "Tags": Dict[str, str],
    },
    total=False,
)

AnswerMachineDetectionConfigTypeDef = TypedDict(
    "AnswerMachineDetectionConfigTypeDef",
    {
        "EnableAnswerMachineDetection": bool,
        "AwaitAnswerMachinePrompt": bool,
    },
    total=False,
)

AssociateApprovedOriginRequestRequestTypeDef = TypedDict(
    "AssociateApprovedOriginRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Origin": str,
    },
)

LexBotTypeDef = TypedDict(
    "LexBotTypeDef",
    {
        "Name": str,
        "LexRegion": str,
    },
)

LexV2BotTypeDef = TypedDict(
    "LexV2BotTypeDef",
    {
        "AliasArn": str,
    },
    total=False,
)

_RequiredAssociateDefaultVocabularyRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateDefaultVocabularyRequestRequestTypeDef",
    {
        "InstanceId": str,
        "LanguageCode": VocabularyLanguageCodeType,
    },
)
_OptionalAssociateDefaultVocabularyRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateDefaultVocabularyRequestRequestTypeDef",
    {
        "VocabularyId": str,
    },
    total=False,
)

class AssociateDefaultVocabularyRequestRequestTypeDef(
    _RequiredAssociateDefaultVocabularyRequestRequestTypeDef,
    _OptionalAssociateDefaultVocabularyRequestRequestTypeDef,
):
    pass

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

AssociateLambdaFunctionRequestRequestTypeDef = TypedDict(
    "AssociateLambdaFunctionRequestRequestTypeDef",
    {
        "InstanceId": str,
        "FunctionArn": str,
    },
)

AssociatePhoneNumberContactFlowRequestRequestTypeDef = TypedDict(
    "AssociatePhoneNumberContactFlowRequestRequestTypeDef",
    {
        "PhoneNumberId": str,
        "InstanceId": str,
        "ContactFlowId": str,
    },
)

AssociateQueueQuickConnectsRequestRequestTypeDef = TypedDict(
    "AssociateQueueQuickConnectsRequestRequestTypeDef",
    {
        "InstanceId": str,
        "QueueId": str,
        "QuickConnectIds": Sequence[str],
    },
)

AssociateSecurityKeyRequestRequestTypeDef = TypedDict(
    "AssociateSecurityKeyRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Key": str,
    },
)

AttachmentReferenceTypeDef = TypedDict(
    "AttachmentReferenceTypeDef",
    {
        "Name": str,
        "Value": str,
        "Status": ReferenceStatusType,
    },
    total=False,
)

AttributeTypeDef = TypedDict(
    "AttributeTypeDef",
    {
        "AttributeType": InstanceAttributeTypeType,
        "Value": str,
    },
    total=False,
)

AvailableNumberSummaryTypeDef = TypedDict(
    "AvailableNumberSummaryTypeDef",
    {
        "PhoneNumber": str,
        "PhoneNumberCountryCode": PhoneNumberCountryCodeType,
        "PhoneNumberType": PhoneNumberTypeType,
    },
    total=False,
)

ChatMessageTypeDef = TypedDict(
    "ChatMessageTypeDef",
    {
        "ContentType": str,
        "Content": str,
    },
)

ChatStreamingConfigurationTypeDef = TypedDict(
    "ChatStreamingConfigurationTypeDef",
    {
        "StreamingEndpointArn": str,
    },
)

_RequiredClaimPhoneNumberRequestRequestTypeDef = TypedDict(
    "_RequiredClaimPhoneNumberRequestRequestTypeDef",
    {
        "TargetArn": str,
        "PhoneNumber": str,
    },
)
_OptionalClaimPhoneNumberRequestRequestTypeDef = TypedDict(
    "_OptionalClaimPhoneNumberRequestRequestTypeDef",
    {
        "PhoneNumberDescription": str,
        "Tags": Mapping[str, str],
        "ClientToken": str,
    },
    total=False,
)

class ClaimPhoneNumberRequestRequestTypeDef(
    _RequiredClaimPhoneNumberRequestRequestTypeDef, _OptionalClaimPhoneNumberRequestRequestTypeDef
):
    pass

PhoneNumberStatusTypeDef = TypedDict(
    "PhoneNumberStatusTypeDef",
    {
        "Status": PhoneNumberWorkflowStatusType,
        "Message": str,
    },
    total=False,
)

ContactFilterTypeDef = TypedDict(
    "ContactFilterTypeDef",
    {
        "ContactStates": Sequence[ContactStateType],
    },
    total=False,
)

ContactFlowModuleSummaryTypeDef = TypedDict(
    "ContactFlowModuleSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "State": ContactFlowModuleStateType,
    },
    total=False,
)

ContactFlowModuleTypeDef = TypedDict(
    "ContactFlowModuleTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Name": str,
        "Content": str,
        "Description": str,
        "State": ContactFlowModuleStateType,
        "Status": ContactFlowModuleStatusType,
        "Tags": Dict[str, str],
    },
    total=False,
)

ContactFlowSummaryTypeDef = TypedDict(
    "ContactFlowSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "ContactFlowType": ContactFlowTypeType,
        "ContactFlowState": ContactFlowStateType,
    },
    total=False,
)

ContactFlowTypeDef = TypedDict(
    "ContactFlowTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Name": str,
        "Type": ContactFlowTypeType,
        "State": ContactFlowStateType,
        "Description": str,
        "Content": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

QueueInfoTypeDef = TypedDict(
    "QueueInfoTypeDef",
    {
        "Id": str,
        "EnqueueTimestamp": datetime,
    },
    total=False,
)

WisdomInfoTypeDef = TypedDict(
    "WisdomInfoTypeDef",
    {
        "SessionArn": str,
    },
    total=False,
)

TagConditionTypeDef = TypedDict(
    "TagConditionTypeDef",
    {
        "TagKey": str,
        "TagValue": str,
    },
    total=False,
)

_RequiredCreateAgentStatusRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAgentStatusRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Name": str,
        "State": AgentStatusStateType,
    },
)
_OptionalCreateAgentStatusRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAgentStatusRequestRequestTypeDef",
    {
        "Description": str,
        "DisplayOrder": int,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateAgentStatusRequestRequestTypeDef(
    _RequiredCreateAgentStatusRequestRequestTypeDef, _OptionalCreateAgentStatusRequestRequestTypeDef
):
    pass

_RequiredCreateContactFlowModuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateContactFlowModuleRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Name": str,
        "Content": str,
    },
)
_OptionalCreateContactFlowModuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateContactFlowModuleRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Mapping[str, str],
        "ClientToken": str,
    },
    total=False,
)

class CreateContactFlowModuleRequestRequestTypeDef(
    _RequiredCreateContactFlowModuleRequestRequestTypeDef,
    _OptionalCreateContactFlowModuleRequestRequestTypeDef,
):
    pass

_RequiredCreateContactFlowRequestRequestTypeDef = TypedDict(
    "_RequiredCreateContactFlowRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Name": str,
        "Type": ContactFlowTypeType,
        "Content": str,
    },
)
_OptionalCreateContactFlowRequestRequestTypeDef = TypedDict(
    "_OptionalCreateContactFlowRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateContactFlowRequestRequestTypeDef(
    _RequiredCreateContactFlowRequestRequestTypeDef, _OptionalCreateContactFlowRequestRequestTypeDef
):
    pass

_RequiredCreateInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateInstanceRequestRequestTypeDef",
    {
        "IdentityManagementType": DirectoryTypeType,
        "InboundCallsEnabled": bool,
        "OutboundCallsEnabled": bool,
    },
)
_OptionalCreateInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateInstanceRequestRequestTypeDef",
    {
        "ClientToken": str,
        "InstanceAlias": str,
        "DirectoryId": str,
    },
    total=False,
)

class CreateInstanceRequestRequestTypeDef(
    _RequiredCreateInstanceRequestRequestTypeDef, _OptionalCreateInstanceRequestRequestTypeDef
):
    pass

_RequiredCreateIntegrationAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIntegrationAssociationRequestRequestTypeDef",
    {
        "InstanceId": str,
        "IntegrationType": IntegrationTypeType,
        "IntegrationArn": str,
    },
)
_OptionalCreateIntegrationAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIntegrationAssociationRequestRequestTypeDef",
    {
        "SourceApplicationUrl": str,
        "SourceApplicationName": str,
        "SourceType": SourceTypeType,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateIntegrationAssociationRequestRequestTypeDef(
    _RequiredCreateIntegrationAssociationRequestRequestTypeDef,
    _OptionalCreateIntegrationAssociationRequestRequestTypeDef,
):
    pass

ParticipantDetailsToAddTypeDef = TypedDict(
    "ParticipantDetailsToAddTypeDef",
    {
        "ParticipantRole": ParticipantRoleType,
        "DisplayName": str,
    },
    total=False,
)

ParticipantTokenCredentialsTypeDef = TypedDict(
    "ParticipantTokenCredentialsTypeDef",
    {
        "ParticipantToken": str,
        "Expiry": str,
    },
    total=False,
)

OutboundCallerConfigTypeDef = TypedDict(
    "OutboundCallerConfigTypeDef",
    {
        "OutboundCallerIdName": str,
        "OutboundCallerIdNumberId": str,
        "OutboundFlowId": str,
    },
    total=False,
)

_RequiredRuleTriggerEventSourceTypeDef = TypedDict(
    "_RequiredRuleTriggerEventSourceTypeDef",
    {
        "EventSourceName": EventSourceNameType,
    },
)
_OptionalRuleTriggerEventSourceTypeDef = TypedDict(
    "_OptionalRuleTriggerEventSourceTypeDef",
    {
        "IntegrationAssociationId": str,
    },
    total=False,
)

class RuleTriggerEventSourceTypeDef(
    _RequiredRuleTriggerEventSourceTypeDef, _OptionalRuleTriggerEventSourceTypeDef
):
    pass

_RequiredCreateSecurityProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSecurityProfileRequestRequestTypeDef",
    {
        "SecurityProfileName": str,
        "InstanceId": str,
    },
)
_OptionalCreateSecurityProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSecurityProfileRequestRequestTypeDef",
    {
        "Description": str,
        "Permissions": Sequence[str],
        "Tags": Mapping[str, str],
        "AllowedAccessControlTags": Mapping[str, str],
        "TagRestrictedResources": Sequence[str],
    },
    total=False,
)

class CreateSecurityProfileRequestRequestTypeDef(
    _RequiredCreateSecurityProfileRequestRequestTypeDef,
    _OptionalCreateSecurityProfileRequestRequestTypeDef,
):
    pass

_RequiredCreateTrafficDistributionGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTrafficDistributionGroupRequestRequestTypeDef",
    {
        "Name": str,
        "InstanceId": str,
    },
)
_OptionalCreateTrafficDistributionGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTrafficDistributionGroupRequestRequestTypeDef",
    {
        "Description": str,
        "ClientToken": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateTrafficDistributionGroupRequestRequestTypeDef(
    _RequiredCreateTrafficDistributionGroupRequestRequestTypeDef,
    _OptionalCreateTrafficDistributionGroupRequestRequestTypeDef,
):
    pass

_RequiredCreateUseCaseRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUseCaseRequestRequestTypeDef",
    {
        "InstanceId": str,
        "IntegrationAssociationId": str,
        "UseCaseType": UseCaseTypeType,
    },
)
_OptionalCreateUseCaseRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUseCaseRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateUseCaseRequestRequestTypeDef(
    _RequiredCreateUseCaseRequestRequestTypeDef, _OptionalCreateUseCaseRequestRequestTypeDef
):
    pass

_RequiredCreateUserHierarchyGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserHierarchyGroupRequestRequestTypeDef",
    {
        "Name": str,
        "InstanceId": str,
    },
)
_OptionalCreateUserHierarchyGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserHierarchyGroupRequestRequestTypeDef",
    {
        "ParentGroupId": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateUserHierarchyGroupRequestRequestTypeDef(
    _RequiredCreateUserHierarchyGroupRequestRequestTypeDef,
    _OptionalCreateUserHierarchyGroupRequestRequestTypeDef,
):
    pass

UserIdentityInfoTypeDef = TypedDict(
    "UserIdentityInfoTypeDef",
    {
        "FirstName": str,
        "LastName": str,
        "Email": str,
        "SecondaryEmail": str,
        "Mobile": str,
    },
    total=False,
)

_RequiredUserPhoneConfigTypeDef = TypedDict(
    "_RequiredUserPhoneConfigTypeDef",
    {
        "PhoneType": PhoneTypeType,
    },
)
_OptionalUserPhoneConfigTypeDef = TypedDict(
    "_OptionalUserPhoneConfigTypeDef",
    {
        "AutoAccept": bool,
        "AfterContactWorkTimeLimit": int,
        "DeskPhoneNumber": str,
    },
    total=False,
)

class UserPhoneConfigTypeDef(_RequiredUserPhoneConfigTypeDef, _OptionalUserPhoneConfigTypeDef):
    pass

_RequiredCreateVocabularyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateVocabularyRequestRequestTypeDef",
    {
        "InstanceId": str,
        "VocabularyName": str,
        "LanguageCode": VocabularyLanguageCodeType,
        "Content": str,
    },
)
_OptionalCreateVocabularyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateVocabularyRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateVocabularyRequestRequestTypeDef(
    _RequiredCreateVocabularyRequestRequestTypeDef, _OptionalCreateVocabularyRequestRequestTypeDef
):
    pass

CredentialsTypeDef = TypedDict(
    "CredentialsTypeDef",
    {
        "AccessToken": str,
        "AccessTokenExpiration": datetime,
        "RefreshToken": str,
        "RefreshTokenExpiration": datetime,
    },
    total=False,
)

CrossChannelBehaviorTypeDef = TypedDict(
    "CrossChannelBehaviorTypeDef",
    {
        "BehaviorType": BehaviorTypeType,
    },
)

CurrentMetricTypeDef = TypedDict(
    "CurrentMetricTypeDef",
    {
        "Name": CurrentMetricNameType,
        "Unit": UnitType,
    },
    total=False,
)

CurrentMetricSortCriteriaTypeDef = TypedDict(
    "CurrentMetricSortCriteriaTypeDef",
    {
        "SortByMetric": CurrentMetricNameType,
        "SortOrder": SortOrderType,
    },
    total=False,
)

DateReferenceTypeDef = TypedDict(
    "DateReferenceTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

DefaultVocabularyTypeDef = TypedDict(
    "DefaultVocabularyTypeDef",
    {
        "InstanceId": str,
        "LanguageCode": VocabularyLanguageCodeType,
        "VocabularyId": str,
        "VocabularyName": str,
    },
)

DeleteContactFlowModuleRequestRequestTypeDef = TypedDict(
    "DeleteContactFlowModuleRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactFlowModuleId": str,
    },
)

DeleteContactFlowRequestRequestTypeDef = TypedDict(
    "DeleteContactFlowRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactFlowId": str,
    },
)

DeleteHoursOfOperationRequestRequestTypeDef = TypedDict(
    "DeleteHoursOfOperationRequestRequestTypeDef",
    {
        "InstanceId": str,
        "HoursOfOperationId": str,
    },
)

DeleteInstanceRequestRequestTypeDef = TypedDict(
    "DeleteInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)

DeleteIntegrationAssociationRequestRequestTypeDef = TypedDict(
    "DeleteIntegrationAssociationRequestRequestTypeDef",
    {
        "InstanceId": str,
        "IntegrationAssociationId": str,
    },
)

DeleteQuickConnectRequestRequestTypeDef = TypedDict(
    "DeleteQuickConnectRequestRequestTypeDef",
    {
        "InstanceId": str,
        "QuickConnectId": str,
    },
)

DeleteRuleRequestRequestTypeDef = TypedDict(
    "DeleteRuleRequestRequestTypeDef",
    {
        "InstanceId": str,
        "RuleId": str,
    },
)

DeleteSecurityProfileRequestRequestTypeDef = TypedDict(
    "DeleteSecurityProfileRequestRequestTypeDef",
    {
        "InstanceId": str,
        "SecurityProfileId": str,
    },
)

DeleteTaskTemplateRequestRequestTypeDef = TypedDict(
    "DeleteTaskTemplateRequestRequestTypeDef",
    {
        "InstanceId": str,
        "TaskTemplateId": str,
    },
)

DeleteTrafficDistributionGroupRequestRequestTypeDef = TypedDict(
    "DeleteTrafficDistributionGroupRequestRequestTypeDef",
    {
        "TrafficDistributionGroupId": str,
    },
)

DeleteUseCaseRequestRequestTypeDef = TypedDict(
    "DeleteUseCaseRequestRequestTypeDef",
    {
        "InstanceId": str,
        "IntegrationAssociationId": str,
        "UseCaseId": str,
    },
)

DeleteUserHierarchyGroupRequestRequestTypeDef = TypedDict(
    "DeleteUserHierarchyGroupRequestRequestTypeDef",
    {
        "HierarchyGroupId": str,
        "InstanceId": str,
    },
)

DeleteUserRequestRequestTypeDef = TypedDict(
    "DeleteUserRequestRequestTypeDef",
    {
        "InstanceId": str,
        "UserId": str,
    },
)

DeleteVocabularyRequestRequestTypeDef = TypedDict(
    "DeleteVocabularyRequestRequestTypeDef",
    {
        "InstanceId": str,
        "VocabularyId": str,
    },
)

DescribeAgentStatusRequestRequestTypeDef = TypedDict(
    "DescribeAgentStatusRequestRequestTypeDef",
    {
        "InstanceId": str,
        "AgentStatusId": str,
    },
)

DescribeContactFlowModuleRequestRequestTypeDef = TypedDict(
    "DescribeContactFlowModuleRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactFlowModuleId": str,
    },
)

DescribeContactFlowRequestRequestTypeDef = TypedDict(
    "DescribeContactFlowRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactFlowId": str,
    },
)

DescribeContactRequestRequestTypeDef = TypedDict(
    "DescribeContactRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
    },
)

DescribeHoursOfOperationRequestRequestTypeDef = TypedDict(
    "DescribeHoursOfOperationRequestRequestTypeDef",
    {
        "InstanceId": str,
        "HoursOfOperationId": str,
    },
)

DescribeInstanceAttributeRequestRequestTypeDef = TypedDict(
    "DescribeInstanceAttributeRequestRequestTypeDef",
    {
        "InstanceId": str,
        "AttributeType": InstanceAttributeTypeType,
    },
)

DescribeInstanceRequestRequestTypeDef = TypedDict(
    "DescribeInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)

DescribeInstanceStorageConfigRequestRequestTypeDef = TypedDict(
    "DescribeInstanceStorageConfigRequestRequestTypeDef",
    {
        "InstanceId": str,
        "AssociationId": str,
        "ResourceType": InstanceStorageResourceTypeType,
    },
)

DescribePhoneNumberRequestRequestTypeDef = TypedDict(
    "DescribePhoneNumberRequestRequestTypeDef",
    {
        "PhoneNumberId": str,
    },
)

DescribeQueueRequestRequestTypeDef = TypedDict(
    "DescribeQueueRequestRequestTypeDef",
    {
        "InstanceId": str,
        "QueueId": str,
    },
)

DescribeQuickConnectRequestRequestTypeDef = TypedDict(
    "DescribeQuickConnectRequestRequestTypeDef",
    {
        "InstanceId": str,
        "QuickConnectId": str,
    },
)

DescribeRoutingProfileRequestRequestTypeDef = TypedDict(
    "DescribeRoutingProfileRequestRequestTypeDef",
    {
        "InstanceId": str,
        "RoutingProfileId": str,
    },
)

DescribeRuleRequestRequestTypeDef = TypedDict(
    "DescribeRuleRequestRequestTypeDef",
    {
        "InstanceId": str,
        "RuleId": str,
    },
)

DescribeSecurityProfileRequestRequestTypeDef = TypedDict(
    "DescribeSecurityProfileRequestRequestTypeDef",
    {
        "SecurityProfileId": str,
        "InstanceId": str,
    },
)

SecurityProfileTypeDef = TypedDict(
    "SecurityProfileTypeDef",
    {
        "Id": str,
        "OrganizationResourceId": str,
        "Arn": str,
        "SecurityProfileName": str,
        "Description": str,
        "Tags": Dict[str, str],
        "AllowedAccessControlTags": Dict[str, str],
        "TagRestrictedResources": List[str],
    },
    total=False,
)

DescribeTrafficDistributionGroupRequestRequestTypeDef = TypedDict(
    "DescribeTrafficDistributionGroupRequestRequestTypeDef",
    {
        "TrafficDistributionGroupId": str,
    },
)

TrafficDistributionGroupTypeDef = TypedDict(
    "TrafficDistributionGroupTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Description": str,
        "InstanceArn": str,
        "Status": TrafficDistributionGroupStatusType,
        "Tags": Dict[str, str],
    },
    total=False,
)

DescribeUserHierarchyGroupRequestRequestTypeDef = TypedDict(
    "DescribeUserHierarchyGroupRequestRequestTypeDef",
    {
        "HierarchyGroupId": str,
        "InstanceId": str,
    },
)

DescribeUserHierarchyStructureRequestRequestTypeDef = TypedDict(
    "DescribeUserHierarchyStructureRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)

DescribeUserRequestRequestTypeDef = TypedDict(
    "DescribeUserRequestRequestTypeDef",
    {
        "UserId": str,
        "InstanceId": str,
    },
)

DescribeVocabularyRequestRequestTypeDef = TypedDict(
    "DescribeVocabularyRequestRequestTypeDef",
    {
        "InstanceId": str,
        "VocabularyId": str,
    },
)

_RequiredVocabularyTypeDef = TypedDict(
    "_RequiredVocabularyTypeDef",
    {
        "Name": str,
        "Id": str,
        "Arn": str,
        "LanguageCode": VocabularyLanguageCodeType,
        "State": VocabularyStateType,
        "LastModifiedTime": datetime,
    },
)
_OptionalVocabularyTypeDef = TypedDict(
    "_OptionalVocabularyTypeDef",
    {
        "FailureReason": str,
        "Content": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

class VocabularyTypeDef(_RequiredVocabularyTypeDef, _OptionalVocabularyTypeDef):
    pass

RoutingProfileReferenceTypeDef = TypedDict(
    "RoutingProfileReferenceTypeDef",
    {
        "Id": str,
        "Arn": str,
    },
    total=False,
)

DisassociateApprovedOriginRequestRequestTypeDef = TypedDict(
    "DisassociateApprovedOriginRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Origin": str,
    },
)

DisassociateInstanceStorageConfigRequestRequestTypeDef = TypedDict(
    "DisassociateInstanceStorageConfigRequestRequestTypeDef",
    {
        "InstanceId": str,
        "AssociationId": str,
        "ResourceType": InstanceStorageResourceTypeType,
    },
)

DisassociateLambdaFunctionRequestRequestTypeDef = TypedDict(
    "DisassociateLambdaFunctionRequestRequestTypeDef",
    {
        "InstanceId": str,
        "FunctionArn": str,
    },
)

DisassociateLexBotRequestRequestTypeDef = TypedDict(
    "DisassociateLexBotRequestRequestTypeDef",
    {
        "InstanceId": str,
        "BotName": str,
        "LexRegion": str,
    },
)

DisassociatePhoneNumberContactFlowRequestRequestTypeDef = TypedDict(
    "DisassociatePhoneNumberContactFlowRequestRequestTypeDef",
    {
        "PhoneNumberId": str,
        "InstanceId": str,
    },
)

DisassociateQueueQuickConnectsRequestRequestTypeDef = TypedDict(
    "DisassociateQueueQuickConnectsRequestRequestTypeDef",
    {
        "InstanceId": str,
        "QueueId": str,
        "QuickConnectIds": Sequence[str],
    },
)

RoutingProfileQueueReferenceTypeDef = TypedDict(
    "RoutingProfileQueueReferenceTypeDef",
    {
        "QueueId": str,
        "Channel": ChannelType,
    },
)

DisassociateSecurityKeyRequestRequestTypeDef = TypedDict(
    "DisassociateSecurityKeyRequestRequestTypeDef",
    {
        "InstanceId": str,
        "AssociationId": str,
    },
)

DismissUserContactRequestRequestTypeDef = TypedDict(
    "DismissUserContactRequestRequestTypeDef",
    {
        "UserId": str,
        "InstanceId": str,
        "ContactId": str,
    },
)

DistributionTypeDef = TypedDict(
    "DistributionTypeDef",
    {
        "Region": str,
        "Percentage": int,
    },
)

EmailReferenceTypeDef = TypedDict(
    "EmailReferenceTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

EncryptionConfigTypeDef = TypedDict(
    "EncryptionConfigTypeDef",
    {
        "EncryptionType": Literal["KMS"],
        "KeyId": str,
    },
)

EventBridgeActionDefinitionTypeDef = TypedDict(
    "EventBridgeActionDefinitionTypeDef",
    {
        "Name": str,
    },
)

FilterV2TypeDef = TypedDict(
    "FilterV2TypeDef",
    {
        "FilterKey": str,
        "FilterValues": Sequence[str],
    },
    total=False,
)

FiltersTypeDef = TypedDict(
    "FiltersTypeDef",
    {
        "Queues": Sequence[str],
        "Channels": Sequence[ChannelType],
        "RoutingProfiles": Sequence[str],
    },
    total=False,
)

GetContactAttributesRequestRequestTypeDef = TypedDict(
    "GetContactAttributesRequestRequestTypeDef",
    {
        "InstanceId": str,
        "InitialContactId": str,
    },
)

GetFederationTokenRequestRequestTypeDef = TypedDict(
    "GetFederationTokenRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredGetTaskTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredGetTaskTemplateRequestRequestTypeDef",
    {
        "InstanceId": str,
        "TaskTemplateId": str,
    },
)
_OptionalGetTaskTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalGetTaskTemplateRequestRequestTypeDef",
    {
        "SnapshotVersion": str,
    },
    total=False,
)

class GetTaskTemplateRequestRequestTypeDef(
    _RequiredGetTaskTemplateRequestRequestTypeDef, _OptionalGetTaskTemplateRequestRequestTypeDef
):
    pass

GetTrafficDistributionRequestRequestTypeDef = TypedDict(
    "GetTrafficDistributionRequestRequestTypeDef",
    {
        "Id": str,
    },
)

HierarchyGroupConditionTypeDef = TypedDict(
    "HierarchyGroupConditionTypeDef",
    {
        "Value": str,
        "HierarchyGroupMatchType": HierarchyGroupMatchTypeType,
    },
    total=False,
)

HierarchyGroupSummaryReferenceTypeDef = TypedDict(
    "HierarchyGroupSummaryReferenceTypeDef",
    {
        "Id": str,
        "Arn": str,
    },
    total=False,
)

HierarchyGroupSummaryTypeDef = TypedDict(
    "HierarchyGroupSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
    },
    total=False,
)

HierarchyLevelTypeDef = TypedDict(
    "HierarchyLevelTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
    },
    total=False,
)

HierarchyLevelUpdateTypeDef = TypedDict(
    "HierarchyLevelUpdateTypeDef",
    {
        "Name": str,
    },
)

ThresholdTypeDef = TypedDict(
    "ThresholdTypeDef",
    {
        "Comparison": Literal["LT"],
        "ThresholdValue": float,
    },
    total=False,
)

HoursOfOperationTimeSliceTypeDef = TypedDict(
    "HoursOfOperationTimeSliceTypeDef",
    {
        "Hours": int,
        "Minutes": int,
    },
)

HoursOfOperationSummaryTypeDef = TypedDict(
    "HoursOfOperationSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
    },
    total=False,
)

InstanceStatusReasonTypeDef = TypedDict(
    "InstanceStatusReasonTypeDef",
    {
        "Message": str,
    },
    total=False,
)

KinesisFirehoseConfigTypeDef = TypedDict(
    "KinesisFirehoseConfigTypeDef",
    {
        "FirehoseArn": str,
    },
)

KinesisStreamConfigTypeDef = TypedDict(
    "KinesisStreamConfigTypeDef",
    {
        "StreamArn": str,
    },
)

InstanceSummaryTypeDef = TypedDict(
    "InstanceSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "IdentityManagementType": DirectoryTypeType,
        "InstanceAlias": str,
        "CreatedTime": datetime,
        "ServiceRole": str,
        "InstanceStatus": InstanceStatusType,
        "InboundCallsEnabled": bool,
        "OutboundCallsEnabled": bool,
    },
    total=False,
)

IntegrationAssociationSummaryTypeDef = TypedDict(
    "IntegrationAssociationSummaryTypeDef",
    {
        "IntegrationAssociationId": str,
        "IntegrationAssociationArn": str,
        "InstanceId": str,
        "IntegrationType": IntegrationTypeType,
        "IntegrationArn": str,
        "SourceApplicationUrl": str,
        "SourceApplicationName": str,
        "SourceType": SourceTypeType,
    },
    total=False,
)

TaskTemplateFieldIdentifierTypeDef = TypedDict(
    "TaskTemplateFieldIdentifierTypeDef",
    {
        "Name": str,
    },
    total=False,
)

_RequiredListAgentStatusRequestRequestTypeDef = TypedDict(
    "_RequiredListAgentStatusRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListAgentStatusRequestRequestTypeDef = TypedDict(
    "_OptionalListAgentStatusRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "AgentStatusTypes": Sequence[AgentStatusTypeType],
    },
    total=False,
)

class ListAgentStatusRequestRequestTypeDef(
    _RequiredListAgentStatusRequestRequestTypeDef, _OptionalListAgentStatusRequestRequestTypeDef
):
    pass

_RequiredListApprovedOriginsRequestRequestTypeDef = TypedDict(
    "_RequiredListApprovedOriginsRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListApprovedOriginsRequestRequestTypeDef = TypedDict(
    "_OptionalListApprovedOriginsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListApprovedOriginsRequestRequestTypeDef(
    _RequiredListApprovedOriginsRequestRequestTypeDef,
    _OptionalListApprovedOriginsRequestRequestTypeDef,
):
    pass

_RequiredListBotsRequestRequestTypeDef = TypedDict(
    "_RequiredListBotsRequestRequestTypeDef",
    {
        "InstanceId": str,
        "LexVersion": LexVersionType,
    },
)
_OptionalListBotsRequestRequestTypeDef = TypedDict(
    "_OptionalListBotsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListBotsRequestRequestTypeDef(
    _RequiredListBotsRequestRequestTypeDef, _OptionalListBotsRequestRequestTypeDef
):
    pass

_RequiredListContactFlowModulesRequestRequestTypeDef = TypedDict(
    "_RequiredListContactFlowModulesRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListContactFlowModulesRequestRequestTypeDef = TypedDict(
    "_OptionalListContactFlowModulesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ContactFlowModuleState": ContactFlowModuleStateType,
    },
    total=False,
)

class ListContactFlowModulesRequestRequestTypeDef(
    _RequiredListContactFlowModulesRequestRequestTypeDef,
    _OptionalListContactFlowModulesRequestRequestTypeDef,
):
    pass

_RequiredListContactFlowsRequestRequestTypeDef = TypedDict(
    "_RequiredListContactFlowsRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListContactFlowsRequestRequestTypeDef = TypedDict(
    "_OptionalListContactFlowsRequestRequestTypeDef",
    {
        "ContactFlowTypes": Sequence[ContactFlowTypeType],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListContactFlowsRequestRequestTypeDef(
    _RequiredListContactFlowsRequestRequestTypeDef, _OptionalListContactFlowsRequestRequestTypeDef
):
    pass

_RequiredListContactReferencesRequestRequestTypeDef = TypedDict(
    "_RequiredListContactReferencesRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
        "ReferenceTypes": Sequence[ReferenceTypeType],
    },
)
_OptionalListContactReferencesRequestRequestTypeDef = TypedDict(
    "_OptionalListContactReferencesRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

class ListContactReferencesRequestRequestTypeDef(
    _RequiredListContactReferencesRequestRequestTypeDef,
    _OptionalListContactReferencesRequestRequestTypeDef,
):
    pass

_RequiredListDefaultVocabulariesRequestRequestTypeDef = TypedDict(
    "_RequiredListDefaultVocabulariesRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListDefaultVocabulariesRequestRequestTypeDef = TypedDict(
    "_OptionalListDefaultVocabulariesRequestRequestTypeDef",
    {
        "LanguageCode": VocabularyLanguageCodeType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListDefaultVocabulariesRequestRequestTypeDef(
    _RequiredListDefaultVocabulariesRequestRequestTypeDef,
    _OptionalListDefaultVocabulariesRequestRequestTypeDef,
):
    pass

_RequiredListHoursOfOperationsRequestRequestTypeDef = TypedDict(
    "_RequiredListHoursOfOperationsRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListHoursOfOperationsRequestRequestTypeDef = TypedDict(
    "_OptionalListHoursOfOperationsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListHoursOfOperationsRequestRequestTypeDef(
    _RequiredListHoursOfOperationsRequestRequestTypeDef,
    _OptionalListHoursOfOperationsRequestRequestTypeDef,
):
    pass

_RequiredListInstanceAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredListInstanceAttributesRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListInstanceAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalListInstanceAttributesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListInstanceAttributesRequestRequestTypeDef(
    _RequiredListInstanceAttributesRequestRequestTypeDef,
    _OptionalListInstanceAttributesRequestRequestTypeDef,
):
    pass

_RequiredListInstanceStorageConfigsRequestRequestTypeDef = TypedDict(
    "_RequiredListInstanceStorageConfigsRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ResourceType": InstanceStorageResourceTypeType,
    },
)
_OptionalListInstanceStorageConfigsRequestRequestTypeDef = TypedDict(
    "_OptionalListInstanceStorageConfigsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListInstanceStorageConfigsRequestRequestTypeDef(
    _RequiredListInstanceStorageConfigsRequestRequestTypeDef,
    _OptionalListInstanceStorageConfigsRequestRequestTypeDef,
):
    pass

ListInstancesRequestRequestTypeDef = TypedDict(
    "ListInstancesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListIntegrationAssociationsRequestRequestTypeDef = TypedDict(
    "_RequiredListIntegrationAssociationsRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListIntegrationAssociationsRequestRequestTypeDef = TypedDict(
    "_OptionalListIntegrationAssociationsRequestRequestTypeDef",
    {
        "IntegrationType": IntegrationTypeType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListIntegrationAssociationsRequestRequestTypeDef(
    _RequiredListIntegrationAssociationsRequestRequestTypeDef,
    _OptionalListIntegrationAssociationsRequestRequestTypeDef,
):
    pass

_RequiredListLambdaFunctionsRequestRequestTypeDef = TypedDict(
    "_RequiredListLambdaFunctionsRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListLambdaFunctionsRequestRequestTypeDef = TypedDict(
    "_OptionalListLambdaFunctionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListLambdaFunctionsRequestRequestTypeDef(
    _RequiredListLambdaFunctionsRequestRequestTypeDef,
    _OptionalListLambdaFunctionsRequestRequestTypeDef,
):
    pass

_RequiredListLexBotsRequestRequestTypeDef = TypedDict(
    "_RequiredListLexBotsRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListLexBotsRequestRequestTypeDef = TypedDict(
    "_OptionalListLexBotsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListLexBotsRequestRequestTypeDef(
    _RequiredListLexBotsRequestRequestTypeDef, _OptionalListLexBotsRequestRequestTypeDef
):
    pass

_RequiredListPhoneNumbersRequestRequestTypeDef = TypedDict(
    "_RequiredListPhoneNumbersRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListPhoneNumbersRequestRequestTypeDef = TypedDict(
    "_OptionalListPhoneNumbersRequestRequestTypeDef",
    {
        "PhoneNumberTypes": Sequence[PhoneNumberTypeType],
        "PhoneNumberCountryCodes": Sequence[PhoneNumberCountryCodeType],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListPhoneNumbersRequestRequestTypeDef(
    _RequiredListPhoneNumbersRequestRequestTypeDef, _OptionalListPhoneNumbersRequestRequestTypeDef
):
    pass

PhoneNumberSummaryTypeDef = TypedDict(
    "PhoneNumberSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "PhoneNumber": str,
        "PhoneNumberType": PhoneNumberTypeType,
        "PhoneNumberCountryCode": PhoneNumberCountryCodeType,
    },
    total=False,
)

ListPhoneNumbersSummaryTypeDef = TypedDict(
    "ListPhoneNumbersSummaryTypeDef",
    {
        "PhoneNumberId": str,
        "PhoneNumberArn": str,
        "PhoneNumber": str,
        "PhoneNumberCountryCode": PhoneNumberCountryCodeType,
        "PhoneNumberType": PhoneNumberTypeType,
        "TargetArn": str,
    },
    total=False,
)

ListPhoneNumbersV2RequestRequestTypeDef = TypedDict(
    "ListPhoneNumbersV2RequestRequestTypeDef",
    {
        "TargetArn": str,
        "MaxResults": int,
        "NextToken": str,
        "PhoneNumberCountryCodes": Sequence[PhoneNumberCountryCodeType],
        "PhoneNumberTypes": Sequence[PhoneNumberTypeType],
        "PhoneNumberPrefix": str,
    },
    total=False,
)

_RequiredListPromptsRequestRequestTypeDef = TypedDict(
    "_RequiredListPromptsRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListPromptsRequestRequestTypeDef = TypedDict(
    "_OptionalListPromptsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListPromptsRequestRequestTypeDef(
    _RequiredListPromptsRequestRequestTypeDef, _OptionalListPromptsRequestRequestTypeDef
):
    pass

PromptSummaryTypeDef = TypedDict(
    "PromptSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
    },
    total=False,
)

_RequiredListQueueQuickConnectsRequestRequestTypeDef = TypedDict(
    "_RequiredListQueueQuickConnectsRequestRequestTypeDef",
    {
        "InstanceId": str,
        "QueueId": str,
    },
)
_OptionalListQueueQuickConnectsRequestRequestTypeDef = TypedDict(
    "_OptionalListQueueQuickConnectsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListQueueQuickConnectsRequestRequestTypeDef(
    _RequiredListQueueQuickConnectsRequestRequestTypeDef,
    _OptionalListQueueQuickConnectsRequestRequestTypeDef,
):
    pass

QuickConnectSummaryTypeDef = TypedDict(
    "QuickConnectSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "QuickConnectType": QuickConnectTypeType,
    },
    total=False,
)

_RequiredListQueuesRequestRequestTypeDef = TypedDict(
    "_RequiredListQueuesRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListQueuesRequestRequestTypeDef = TypedDict(
    "_OptionalListQueuesRequestRequestTypeDef",
    {
        "QueueTypes": Sequence[QueueTypeType],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListQueuesRequestRequestTypeDef(
    _RequiredListQueuesRequestRequestTypeDef, _OptionalListQueuesRequestRequestTypeDef
):
    pass

QueueSummaryTypeDef = TypedDict(
    "QueueSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "QueueType": QueueTypeType,
    },
    total=False,
)

_RequiredListQuickConnectsRequestRequestTypeDef = TypedDict(
    "_RequiredListQuickConnectsRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListQuickConnectsRequestRequestTypeDef = TypedDict(
    "_OptionalListQuickConnectsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "QuickConnectTypes": Sequence[QuickConnectTypeType],
    },
    total=False,
)

class ListQuickConnectsRequestRequestTypeDef(
    _RequiredListQuickConnectsRequestRequestTypeDef, _OptionalListQuickConnectsRequestRequestTypeDef
):
    pass

_RequiredListRoutingProfileQueuesRequestRequestTypeDef = TypedDict(
    "_RequiredListRoutingProfileQueuesRequestRequestTypeDef",
    {
        "InstanceId": str,
        "RoutingProfileId": str,
    },
)
_OptionalListRoutingProfileQueuesRequestRequestTypeDef = TypedDict(
    "_OptionalListRoutingProfileQueuesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListRoutingProfileQueuesRequestRequestTypeDef(
    _RequiredListRoutingProfileQueuesRequestRequestTypeDef,
    _OptionalListRoutingProfileQueuesRequestRequestTypeDef,
):
    pass

RoutingProfileQueueConfigSummaryTypeDef = TypedDict(
    "RoutingProfileQueueConfigSummaryTypeDef",
    {
        "QueueId": str,
        "QueueArn": str,
        "QueueName": str,
        "Priority": int,
        "Delay": int,
        "Channel": ChannelType,
    },
)

_RequiredListRoutingProfilesRequestRequestTypeDef = TypedDict(
    "_RequiredListRoutingProfilesRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListRoutingProfilesRequestRequestTypeDef = TypedDict(
    "_OptionalListRoutingProfilesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListRoutingProfilesRequestRequestTypeDef(
    _RequiredListRoutingProfilesRequestRequestTypeDef,
    _OptionalListRoutingProfilesRequestRequestTypeDef,
):
    pass

RoutingProfileSummaryTypeDef = TypedDict(
    "RoutingProfileSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
    },
    total=False,
)

_RequiredListRulesRequestRequestTypeDef = TypedDict(
    "_RequiredListRulesRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListRulesRequestRequestTypeDef = TypedDict(
    "_OptionalListRulesRequestRequestTypeDef",
    {
        "PublishStatus": RulePublishStatusType,
        "EventSourceName": EventSourceNameType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListRulesRequestRequestTypeDef(
    _RequiredListRulesRequestRequestTypeDef, _OptionalListRulesRequestRequestTypeDef
):
    pass

_RequiredListSecurityKeysRequestRequestTypeDef = TypedDict(
    "_RequiredListSecurityKeysRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListSecurityKeysRequestRequestTypeDef = TypedDict(
    "_OptionalListSecurityKeysRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListSecurityKeysRequestRequestTypeDef(
    _RequiredListSecurityKeysRequestRequestTypeDef, _OptionalListSecurityKeysRequestRequestTypeDef
):
    pass

SecurityKeyTypeDef = TypedDict(
    "SecurityKeyTypeDef",
    {
        "AssociationId": str,
        "Key": str,
        "CreationTime": datetime,
    },
    total=False,
)

_RequiredListSecurityProfilePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredListSecurityProfilePermissionsRequestRequestTypeDef",
    {
        "SecurityProfileId": str,
        "InstanceId": str,
    },
)
_OptionalListSecurityProfilePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalListSecurityProfilePermissionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListSecurityProfilePermissionsRequestRequestTypeDef(
    _RequiredListSecurityProfilePermissionsRequestRequestTypeDef,
    _OptionalListSecurityProfilePermissionsRequestRequestTypeDef,
):
    pass

_RequiredListSecurityProfilesRequestRequestTypeDef = TypedDict(
    "_RequiredListSecurityProfilesRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListSecurityProfilesRequestRequestTypeDef = TypedDict(
    "_OptionalListSecurityProfilesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListSecurityProfilesRequestRequestTypeDef(
    _RequiredListSecurityProfilesRequestRequestTypeDef,
    _OptionalListSecurityProfilesRequestRequestTypeDef,
):
    pass

SecurityProfileSummaryTypeDef = TypedDict(
    "SecurityProfileSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

_RequiredListTaskTemplatesRequestRequestTypeDef = TypedDict(
    "_RequiredListTaskTemplatesRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListTaskTemplatesRequestRequestTypeDef = TypedDict(
    "_OptionalListTaskTemplatesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Status": TaskTemplateStatusType,
        "Name": str,
    },
    total=False,
)

class ListTaskTemplatesRequestRequestTypeDef(
    _RequiredListTaskTemplatesRequestRequestTypeDef, _OptionalListTaskTemplatesRequestRequestTypeDef
):
    pass

TaskTemplateMetadataTypeDef = TypedDict(
    "TaskTemplateMetadataTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "Description": str,
        "Status": TaskTemplateStatusType,
        "LastModifiedTime": datetime,
        "CreatedTime": datetime,
    },
    total=False,
)

ListTrafficDistributionGroupsRequestRequestTypeDef = TypedDict(
    "ListTrafficDistributionGroupsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "InstanceId": str,
    },
    total=False,
)

TrafficDistributionGroupSummaryTypeDef = TypedDict(
    "TrafficDistributionGroupSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "InstanceArn": str,
        "Status": TrafficDistributionGroupStatusType,
    },
    total=False,
)

_RequiredListUseCasesRequestRequestTypeDef = TypedDict(
    "_RequiredListUseCasesRequestRequestTypeDef",
    {
        "InstanceId": str,
        "IntegrationAssociationId": str,
    },
)
_OptionalListUseCasesRequestRequestTypeDef = TypedDict(
    "_OptionalListUseCasesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListUseCasesRequestRequestTypeDef(
    _RequiredListUseCasesRequestRequestTypeDef, _OptionalListUseCasesRequestRequestTypeDef
):
    pass

UseCaseTypeDef = TypedDict(
    "UseCaseTypeDef",
    {
        "UseCaseId": str,
        "UseCaseArn": str,
        "UseCaseType": UseCaseTypeType,
    },
    total=False,
)

_RequiredListUserHierarchyGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListUserHierarchyGroupsRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListUserHierarchyGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListUserHierarchyGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListUserHierarchyGroupsRequestRequestTypeDef(
    _RequiredListUserHierarchyGroupsRequestRequestTypeDef,
    _OptionalListUserHierarchyGroupsRequestRequestTypeDef,
):
    pass

_RequiredListUsersRequestRequestTypeDef = TypedDict(
    "_RequiredListUsersRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListUsersRequestRequestTypeDef = TypedDict(
    "_OptionalListUsersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListUsersRequestRequestTypeDef(
    _RequiredListUsersRequestRequestTypeDef, _OptionalListUsersRequestRequestTypeDef
):
    pass

UserSummaryTypeDef = TypedDict(
    "UserSummaryTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Username": str,
    },
    total=False,
)

MetricFilterV2TypeDef = TypedDict(
    "MetricFilterV2TypeDef",
    {
        "MetricFilterKey": str,
        "MetricFilterValues": Sequence[str],
    },
    total=False,
)

ThresholdV2TypeDef = TypedDict(
    "ThresholdV2TypeDef",
    {
        "Comparison": str,
        "ThresholdValue": float,
    },
    total=False,
)

_RequiredMonitorContactRequestRequestTypeDef = TypedDict(
    "_RequiredMonitorContactRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
        "UserId": str,
    },
)
_OptionalMonitorContactRequestRequestTypeDef = TypedDict(
    "_OptionalMonitorContactRequestRequestTypeDef",
    {
        "AllowedMonitorCapabilities": Sequence[MonitorCapabilityType],
        "ClientToken": str,
    },
    total=False,
)

class MonitorContactRequestRequestTypeDef(
    _RequiredMonitorContactRequestRequestTypeDef, _OptionalMonitorContactRequestRequestTypeDef
):
    pass

NotificationRecipientTypeTypeDef = TypedDict(
    "NotificationRecipientTypeTypeDef",
    {
        "UserTags": Mapping[str, str],
        "UserIds": Sequence[str],
    },
    total=False,
)

NumberReferenceTypeDef = TypedDict(
    "NumberReferenceTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

ParticipantDetailsTypeDef = TypedDict(
    "ParticipantDetailsTypeDef",
    {
        "DisplayName": str,
    },
)

ParticipantTimerValueTypeDef = TypedDict(
    "ParticipantTimerValueTypeDef",
    {
        "ParticipantTimerAction": Literal["Unset"],
        "ParticipantTimerDurationInMinutes": int,
    },
    total=False,
)

PersistentChatTypeDef = TypedDict(
    "PersistentChatTypeDef",
    {
        "RehydrationType": RehydrationTypeType,
        "SourceContactId": str,
    },
    total=False,
)

PhoneNumberQuickConnectConfigTypeDef = TypedDict(
    "PhoneNumberQuickConnectConfigTypeDef",
    {
        "PhoneNumber": str,
    },
)

PutUserStatusRequestRequestTypeDef = TypedDict(
    "PutUserStatusRequestRequestTypeDef",
    {
        "UserId": str,
        "InstanceId": str,
        "AgentStatusId": str,
    },
)

QueueQuickConnectConfigTypeDef = TypedDict(
    "QueueQuickConnectConfigTypeDef",
    {
        "QueueId": str,
        "ContactFlowId": str,
    },
)

StringConditionTypeDef = TypedDict(
    "StringConditionTypeDef",
    {
        "FieldName": str,
        "Value": str,
        "ComparisonType": StringComparisonTypeType,
    },
    total=False,
)

UserQuickConnectConfigTypeDef = TypedDict(
    "UserQuickConnectConfigTypeDef",
    {
        "UserId": str,
        "ContactFlowId": str,
    },
)

StringReferenceTypeDef = TypedDict(
    "StringReferenceTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

UrlReferenceTypeDef = TypedDict(
    "UrlReferenceTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

ReferenceTypeDef = TypedDict(
    "ReferenceTypeDef",
    {
        "Value": str,
        "Type": ReferenceTypeType,
    },
)

_RequiredReleasePhoneNumberRequestRequestTypeDef = TypedDict(
    "_RequiredReleasePhoneNumberRequestRequestTypeDef",
    {
        "PhoneNumberId": str,
    },
)
_OptionalReleasePhoneNumberRequestRequestTypeDef = TypedDict(
    "_OptionalReleasePhoneNumberRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)

class ReleasePhoneNumberRequestRequestTypeDef(
    _RequiredReleasePhoneNumberRequestRequestTypeDef,
    _OptionalReleasePhoneNumberRequestRequestTypeDef,
):
    pass

_RequiredReplicateInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredReplicateInstanceRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ReplicaRegion": str,
        "ReplicaAlias": str,
    },
)
_OptionalReplicateInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalReplicateInstanceRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)

class ReplicateInstanceRequestRequestTypeDef(
    _RequiredReplicateInstanceRequestRequestTypeDef, _OptionalReplicateInstanceRequestRequestTypeDef
):
    pass

ResumeContactRecordingRequestRequestTypeDef = TypedDict(
    "ResumeContactRecordingRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
        "InitialContactId": str,
    },
)

_RequiredSearchAvailablePhoneNumbersRequestRequestTypeDef = TypedDict(
    "_RequiredSearchAvailablePhoneNumbersRequestRequestTypeDef",
    {
        "TargetArn": str,
        "PhoneNumberCountryCode": PhoneNumberCountryCodeType,
        "PhoneNumberType": PhoneNumberTypeType,
    },
)
_OptionalSearchAvailablePhoneNumbersRequestRequestTypeDef = TypedDict(
    "_OptionalSearchAvailablePhoneNumbersRequestRequestTypeDef",
    {
        "PhoneNumberPrefix": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class SearchAvailablePhoneNumbersRequestRequestTypeDef(
    _RequiredSearchAvailablePhoneNumbersRequestRequestTypeDef,
    _OptionalSearchAvailablePhoneNumbersRequestRequestTypeDef,
):
    pass

SecurityProfileSearchSummaryTypeDef = TypedDict(
    "SecurityProfileSearchSummaryTypeDef",
    {
        "Id": str,
        "OrganizationResourceId": str,
        "Arn": str,
        "SecurityProfileName": str,
        "Description": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

_RequiredSearchVocabulariesRequestRequestTypeDef = TypedDict(
    "_RequiredSearchVocabulariesRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalSearchVocabulariesRequestRequestTypeDef = TypedDict(
    "_OptionalSearchVocabulariesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "State": VocabularyStateType,
        "NameStartsWith": str,
        "LanguageCode": VocabularyLanguageCodeType,
    },
    total=False,
)

class SearchVocabulariesRequestRequestTypeDef(
    _RequiredSearchVocabulariesRequestRequestTypeDef,
    _OptionalSearchVocabulariesRequestRequestTypeDef,
):
    pass

_RequiredVocabularySummaryTypeDef = TypedDict(
    "_RequiredVocabularySummaryTypeDef",
    {
        "Name": str,
        "Id": str,
        "Arn": str,
        "LanguageCode": VocabularyLanguageCodeType,
        "State": VocabularyStateType,
        "LastModifiedTime": datetime,
    },
)
_OptionalVocabularySummaryTypeDef = TypedDict(
    "_OptionalVocabularySummaryTypeDef",
    {
        "FailureReason": str,
    },
    total=False,
)

class VocabularySummaryTypeDef(
    _RequiredVocabularySummaryTypeDef, _OptionalVocabularySummaryTypeDef
):
    pass

VoiceRecordingConfigurationTypeDef = TypedDict(
    "VoiceRecordingConfigurationTypeDef",
    {
        "VoiceRecordingTrack": VoiceRecordingTrackType,
    },
    total=False,
)

StopContactRecordingRequestRequestTypeDef = TypedDict(
    "StopContactRecordingRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
        "InitialContactId": str,
    },
)

StopContactRequestRequestTypeDef = TypedDict(
    "StopContactRequestRequestTypeDef",
    {
        "ContactId": str,
        "InstanceId": str,
    },
)

StopContactStreamingRequestRequestTypeDef = TypedDict(
    "StopContactStreamingRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
        "StreamingId": str,
    },
)

SuspendContactRecordingRequestRequestTypeDef = TypedDict(
    "SuspendContactRecordingRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
        "InitialContactId": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

_RequiredTransferContactRequestRequestTypeDef = TypedDict(
    "_RequiredTransferContactRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
        "ContactFlowId": str,
    },
)
_OptionalTransferContactRequestRequestTypeDef = TypedDict(
    "_OptionalTransferContactRequestRequestTypeDef",
    {
        "QueueId": str,
        "UserId": str,
        "ClientToken": str,
    },
    total=False,
)

class TransferContactRequestRequestTypeDef(
    _RequiredTransferContactRequestRequestTypeDef, _OptionalTransferContactRequestRequestTypeDef
):
    pass

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateAgentStatusRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAgentStatusRequestRequestTypeDef",
    {
        "InstanceId": str,
        "AgentStatusId": str,
    },
)
_OptionalUpdateAgentStatusRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAgentStatusRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "State": AgentStatusStateType,
        "DisplayOrder": int,
        "ResetOrderNumber": bool,
    },
    total=False,
)

class UpdateAgentStatusRequestRequestTypeDef(
    _RequiredUpdateAgentStatusRequestRequestTypeDef, _OptionalUpdateAgentStatusRequestRequestTypeDef
):
    pass

UpdateContactAttributesRequestRequestTypeDef = TypedDict(
    "UpdateContactAttributesRequestRequestTypeDef",
    {
        "InitialContactId": str,
        "InstanceId": str,
        "Attributes": Mapping[str, str],
    },
)

UpdateContactFlowContentRequestRequestTypeDef = TypedDict(
    "UpdateContactFlowContentRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactFlowId": str,
        "Content": str,
    },
)

_RequiredUpdateContactFlowMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContactFlowMetadataRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactFlowId": str,
    },
)
_OptionalUpdateContactFlowMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContactFlowMetadataRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "ContactFlowState": ContactFlowStateType,
    },
    total=False,
)

class UpdateContactFlowMetadataRequestRequestTypeDef(
    _RequiredUpdateContactFlowMetadataRequestRequestTypeDef,
    _OptionalUpdateContactFlowMetadataRequestRequestTypeDef,
):
    pass

UpdateContactFlowModuleContentRequestRequestTypeDef = TypedDict(
    "UpdateContactFlowModuleContentRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactFlowModuleId": str,
        "Content": str,
    },
)

_RequiredUpdateContactFlowModuleMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContactFlowModuleMetadataRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactFlowModuleId": str,
    },
)
_OptionalUpdateContactFlowModuleMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContactFlowModuleMetadataRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "State": ContactFlowModuleStateType,
    },
    total=False,
)

class UpdateContactFlowModuleMetadataRequestRequestTypeDef(
    _RequiredUpdateContactFlowModuleMetadataRequestRequestTypeDef,
    _OptionalUpdateContactFlowModuleMetadataRequestRequestTypeDef,
):
    pass

_RequiredUpdateContactFlowNameRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContactFlowNameRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactFlowId": str,
    },
)
_OptionalUpdateContactFlowNameRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContactFlowNameRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
    },
    total=False,
)

class UpdateContactFlowNameRequestRequestTypeDef(
    _RequiredUpdateContactFlowNameRequestRequestTypeDef,
    _OptionalUpdateContactFlowNameRequestRequestTypeDef,
):
    pass

UpdateContactScheduleRequestRequestTypeDef = TypedDict(
    "UpdateContactScheduleRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
        "ScheduledTime": Union[datetime, str],
    },
)

UpdateInstanceAttributeRequestRequestTypeDef = TypedDict(
    "UpdateInstanceAttributeRequestRequestTypeDef",
    {
        "InstanceId": str,
        "AttributeType": InstanceAttributeTypeType,
        "Value": str,
    },
)

_RequiredUpdatePhoneNumberRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePhoneNumberRequestRequestTypeDef",
    {
        "PhoneNumberId": str,
        "TargetArn": str,
    },
)
_OptionalUpdatePhoneNumberRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePhoneNumberRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)

class UpdatePhoneNumberRequestRequestTypeDef(
    _RequiredUpdatePhoneNumberRequestRequestTypeDef, _OptionalUpdatePhoneNumberRequestRequestTypeDef
):
    pass

UpdateQueueHoursOfOperationRequestRequestTypeDef = TypedDict(
    "UpdateQueueHoursOfOperationRequestRequestTypeDef",
    {
        "InstanceId": str,
        "QueueId": str,
        "HoursOfOperationId": str,
    },
)

_RequiredUpdateQueueMaxContactsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateQueueMaxContactsRequestRequestTypeDef",
    {
        "InstanceId": str,
        "QueueId": str,
    },
)
_OptionalUpdateQueueMaxContactsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateQueueMaxContactsRequestRequestTypeDef",
    {
        "MaxContacts": int,
    },
    total=False,
)

class UpdateQueueMaxContactsRequestRequestTypeDef(
    _RequiredUpdateQueueMaxContactsRequestRequestTypeDef,
    _OptionalUpdateQueueMaxContactsRequestRequestTypeDef,
):
    pass

_RequiredUpdateQueueNameRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateQueueNameRequestRequestTypeDef",
    {
        "InstanceId": str,
        "QueueId": str,
    },
)
_OptionalUpdateQueueNameRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateQueueNameRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
    },
    total=False,
)

class UpdateQueueNameRequestRequestTypeDef(
    _RequiredUpdateQueueNameRequestRequestTypeDef, _OptionalUpdateQueueNameRequestRequestTypeDef
):
    pass

UpdateQueueStatusRequestRequestTypeDef = TypedDict(
    "UpdateQueueStatusRequestRequestTypeDef",
    {
        "InstanceId": str,
        "QueueId": str,
        "Status": QueueStatusType,
    },
)

_RequiredUpdateQuickConnectNameRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateQuickConnectNameRequestRequestTypeDef",
    {
        "InstanceId": str,
        "QuickConnectId": str,
    },
)
_OptionalUpdateQuickConnectNameRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateQuickConnectNameRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
    },
    total=False,
)

class UpdateQuickConnectNameRequestRequestTypeDef(
    _RequiredUpdateQuickConnectNameRequestRequestTypeDef,
    _OptionalUpdateQuickConnectNameRequestRequestTypeDef,
):
    pass

UpdateRoutingProfileDefaultOutboundQueueRequestRequestTypeDef = TypedDict(
    "UpdateRoutingProfileDefaultOutboundQueueRequestRequestTypeDef",
    {
        "InstanceId": str,
        "RoutingProfileId": str,
        "DefaultOutboundQueueId": str,
    },
)

_RequiredUpdateRoutingProfileNameRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRoutingProfileNameRequestRequestTypeDef",
    {
        "InstanceId": str,
        "RoutingProfileId": str,
    },
)
_OptionalUpdateRoutingProfileNameRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRoutingProfileNameRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
    },
    total=False,
)

class UpdateRoutingProfileNameRequestRequestTypeDef(
    _RequiredUpdateRoutingProfileNameRequestRequestTypeDef,
    _OptionalUpdateRoutingProfileNameRequestRequestTypeDef,
):
    pass

_RequiredUpdateSecurityProfileRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSecurityProfileRequestRequestTypeDef",
    {
        "SecurityProfileId": str,
        "InstanceId": str,
    },
)
_OptionalUpdateSecurityProfileRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSecurityProfileRequestRequestTypeDef",
    {
        "Description": str,
        "Permissions": Sequence[str],
        "AllowedAccessControlTags": Mapping[str, str],
        "TagRestrictedResources": Sequence[str],
    },
    total=False,
)

class UpdateSecurityProfileRequestRequestTypeDef(
    _RequiredUpdateSecurityProfileRequestRequestTypeDef,
    _OptionalUpdateSecurityProfileRequestRequestTypeDef,
):
    pass

UpdateUserHierarchyGroupNameRequestRequestTypeDef = TypedDict(
    "UpdateUserHierarchyGroupNameRequestRequestTypeDef",
    {
        "Name": str,
        "HierarchyGroupId": str,
        "InstanceId": str,
    },
)

_RequiredUpdateUserHierarchyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUserHierarchyRequestRequestTypeDef",
    {
        "UserId": str,
        "InstanceId": str,
    },
)
_OptionalUpdateUserHierarchyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUserHierarchyRequestRequestTypeDef",
    {
        "HierarchyGroupId": str,
    },
    total=False,
)

class UpdateUserHierarchyRequestRequestTypeDef(
    _RequiredUpdateUserHierarchyRequestRequestTypeDef,
    _OptionalUpdateUserHierarchyRequestRequestTypeDef,
):
    pass

UpdateUserRoutingProfileRequestRequestTypeDef = TypedDict(
    "UpdateUserRoutingProfileRequestRequestTypeDef",
    {
        "RoutingProfileId": str,
        "UserId": str,
        "InstanceId": str,
    },
)

UpdateUserSecurityProfilesRequestRequestTypeDef = TypedDict(
    "UpdateUserSecurityProfilesRequestRequestTypeDef",
    {
        "SecurityProfileIds": Sequence[str],
        "UserId": str,
        "InstanceId": str,
    },
)

UserReferenceTypeDef = TypedDict(
    "UserReferenceTypeDef",
    {
        "Id": str,
        "Arn": str,
    },
    total=False,
)

UserIdentityInfoLiteTypeDef = TypedDict(
    "UserIdentityInfoLiteTypeDef",
    {
        "FirstName": str,
        "LastName": str,
    },
    total=False,
)

RuleSummaryTypeDef = TypedDict(
    "RuleSummaryTypeDef",
    {
        "Name": str,
        "RuleId": str,
        "RuleArn": str,
        "EventSourceName": EventSourceNameType,
        "PublishStatus": RulePublishStatusType,
        "ActionSummaries": List[ActionSummaryTypeDef],
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
)

AgentContactReferenceTypeDef = TypedDict(
    "AgentContactReferenceTypeDef",
    {
        "ContactId": str,
        "Channel": ChannelType,
        "InitiationMethod": ContactInitiationMethodType,
        "AgentContactState": ContactStateType,
        "StateStartTimestamp": datetime,
        "ConnectedToAgentTimestamp": datetime,
        "Queue": QueueReferenceTypeDef,
    },
    total=False,
)

_RequiredStartOutboundVoiceContactRequestRequestTypeDef = TypedDict(
    "_RequiredStartOutboundVoiceContactRequestRequestTypeDef",
    {
        "DestinationPhoneNumber": str,
        "ContactFlowId": str,
        "InstanceId": str,
    },
)
_OptionalStartOutboundVoiceContactRequestRequestTypeDef = TypedDict(
    "_OptionalStartOutboundVoiceContactRequestRequestTypeDef",
    {
        "ClientToken": str,
        "SourcePhoneNumber": str,
        "QueueId": str,
        "Attributes": Mapping[str, str],
        "AnswerMachineDetectionConfig": AnswerMachineDetectionConfigTypeDef,
        "CampaignId": str,
        "TrafficType": TrafficTypeType,
    },
    total=False,
)

class StartOutboundVoiceContactRequestRequestTypeDef(
    _RequiredStartOutboundVoiceContactRequestRequestTypeDef,
    _OptionalStartOutboundVoiceContactRequestRequestTypeDef,
):
    pass

AssociateLexBotRequestRequestTypeDef = TypedDict(
    "AssociateLexBotRequestRequestTypeDef",
    {
        "InstanceId": str,
        "LexBot": LexBotTypeDef,
    },
)

_RequiredAssociateBotRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateBotRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalAssociateBotRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateBotRequestRequestTypeDef",
    {
        "LexBot": LexBotTypeDef,
        "LexV2Bot": LexV2BotTypeDef,
    },
    total=False,
)

class AssociateBotRequestRequestTypeDef(
    _RequiredAssociateBotRequestRequestTypeDef, _OptionalAssociateBotRequestRequestTypeDef
):
    pass

_RequiredDisassociateBotRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateBotRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalDisassociateBotRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateBotRequestRequestTypeDef",
    {
        "LexBot": LexBotTypeDef,
        "LexV2Bot": LexV2BotTypeDef,
    },
    total=False,
)

class DisassociateBotRequestRequestTypeDef(
    _RequiredDisassociateBotRequestRequestTypeDef, _OptionalDisassociateBotRequestRequestTypeDef
):
    pass

LexBotConfigTypeDef = TypedDict(
    "LexBotConfigTypeDef",
    {
        "LexBot": LexBotTypeDef,
        "LexV2Bot": LexV2BotTypeDef,
    },
    total=False,
)

AssociateInstanceStorageConfigResponseTypeDef = TypedDict(
    "AssociateInstanceStorageConfigResponseTypeDef",
    {
        "AssociationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateSecurityKeyResponseTypeDef = TypedDict(
    "AssociateSecurityKeyResponseTypeDef",
    {
        "AssociationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClaimPhoneNumberResponseTypeDef = TypedDict(
    "ClaimPhoneNumberResponseTypeDef",
    {
        "PhoneNumberId": str,
        "PhoneNumberArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAgentStatusResponseTypeDef = TypedDict(
    "CreateAgentStatusResponseTypeDef",
    {
        "AgentStatusARN": str,
        "AgentStatusId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateContactFlowModuleResponseTypeDef = TypedDict(
    "CreateContactFlowModuleResponseTypeDef",
    {
        "Id": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateContactFlowResponseTypeDef = TypedDict(
    "CreateContactFlowResponseTypeDef",
    {
        "ContactFlowId": str,
        "ContactFlowArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateHoursOfOperationResponseTypeDef = TypedDict(
    "CreateHoursOfOperationResponseTypeDef",
    {
        "HoursOfOperationId": str,
        "HoursOfOperationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateInstanceResponseTypeDef = TypedDict(
    "CreateInstanceResponseTypeDef",
    {
        "Id": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateIntegrationAssociationResponseTypeDef = TypedDict(
    "CreateIntegrationAssociationResponseTypeDef",
    {
        "IntegrationAssociationId": str,
        "IntegrationAssociationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateQueueResponseTypeDef = TypedDict(
    "CreateQueueResponseTypeDef",
    {
        "QueueArn": str,
        "QueueId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateQuickConnectResponseTypeDef = TypedDict(
    "CreateQuickConnectResponseTypeDef",
    {
        "QuickConnectARN": str,
        "QuickConnectId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRoutingProfileResponseTypeDef = TypedDict(
    "CreateRoutingProfileResponseTypeDef",
    {
        "RoutingProfileArn": str,
        "RoutingProfileId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRuleResponseTypeDef = TypedDict(
    "CreateRuleResponseTypeDef",
    {
        "RuleArn": str,
        "RuleId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSecurityProfileResponseTypeDef = TypedDict(
    "CreateSecurityProfileResponseTypeDef",
    {
        "SecurityProfileId": str,
        "SecurityProfileArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTaskTemplateResponseTypeDef = TypedDict(
    "CreateTaskTemplateResponseTypeDef",
    {
        "Id": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTrafficDistributionGroupResponseTypeDef = TypedDict(
    "CreateTrafficDistributionGroupResponseTypeDef",
    {
        "Id": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUseCaseResponseTypeDef = TypedDict(
    "CreateUseCaseResponseTypeDef",
    {
        "UseCaseId": str,
        "UseCaseArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUserHierarchyGroupResponseTypeDef = TypedDict(
    "CreateUserHierarchyGroupResponseTypeDef",
    {
        "HierarchyGroupId": str,
        "HierarchyGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUserResponseTypeDef = TypedDict(
    "CreateUserResponseTypeDef",
    {
        "UserId": str,
        "UserArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVocabularyResponseTypeDef = TypedDict(
    "CreateVocabularyResponseTypeDef",
    {
        "VocabularyArn": str,
        "VocabularyId": str,
        "State": VocabularyStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVocabularyResponseTypeDef = TypedDict(
    "DeleteVocabularyResponseTypeDef",
    {
        "VocabularyArn": str,
        "VocabularyId": str,
        "State": VocabularyStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAgentStatusResponseTypeDef = TypedDict(
    "DescribeAgentStatusResponseTypeDef",
    {
        "AgentStatus": AgentStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContactAttributesResponseTypeDef = TypedDict(
    "GetContactAttributesResponseTypeDef",
    {
        "Attributes": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAgentStatusResponseTypeDef = TypedDict(
    "ListAgentStatusResponseTypeDef",
    {
        "NextToken": str,
        "AgentStatusSummaryList": List[AgentStatusSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApprovedOriginsResponseTypeDef = TypedDict(
    "ListApprovedOriginsResponseTypeDef",
    {
        "Origins": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLambdaFunctionsResponseTypeDef = TypedDict(
    "ListLambdaFunctionsResponseTypeDef",
    {
        "LambdaFunctions": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLexBotsResponseTypeDef = TypedDict(
    "ListLexBotsResponseTypeDef",
    {
        "LexBots": List[LexBotTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSecurityProfilePermissionsResponseTypeDef = TypedDict(
    "ListSecurityProfilePermissionsResponseTypeDef",
    {
        "Permissions": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MonitorContactResponseTypeDef = TypedDict(
    "MonitorContactResponseTypeDef",
    {
        "ContactId": str,
        "ContactArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReplicateInstanceResponseTypeDef = TypedDict(
    "ReplicateInstanceResponseTypeDef",
    {
        "Id": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartChatContactResponseTypeDef = TypedDict(
    "StartChatContactResponseTypeDef",
    {
        "ContactId": str,
        "ParticipantId": str,
        "ParticipantToken": str,
        "ContinuedFromContactId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartContactStreamingResponseTypeDef = TypedDict(
    "StartContactStreamingResponseTypeDef",
    {
        "StreamingId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartOutboundVoiceContactResponseTypeDef = TypedDict(
    "StartOutboundVoiceContactResponseTypeDef",
    {
        "ContactId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartTaskContactResponseTypeDef = TypedDict(
    "StartTaskContactResponseTypeDef",
    {
        "ContactId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TransferContactResponseTypeDef = TypedDict(
    "TransferContactResponseTypeDef",
    {
        "ContactId": str,
        "ContactArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePhoneNumberResponseTypeDef = TypedDict(
    "UpdatePhoneNumberResponseTypeDef",
    {
        "PhoneNumberId": str,
        "PhoneNumberArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeInstanceAttributeResponseTypeDef = TypedDict(
    "DescribeInstanceAttributeResponseTypeDef",
    {
        "Attribute": AttributeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInstanceAttributesResponseTypeDef = TypedDict(
    "ListInstanceAttributesResponseTypeDef",
    {
        "Attributes": List[AttributeTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchAvailablePhoneNumbersResponseTypeDef = TypedDict(
    "SearchAvailablePhoneNumbersResponseTypeDef",
    {
        "NextToken": str,
        "AvailableNumbersList": List[AvailableNumberSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartContactStreamingRequestRequestTypeDef = TypedDict(
    "StartContactStreamingRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
        "ChatStreamingConfiguration": ChatStreamingConfigurationTypeDef,
        "ClientToken": str,
    },
)

ClaimedPhoneNumberSummaryTypeDef = TypedDict(
    "ClaimedPhoneNumberSummaryTypeDef",
    {
        "PhoneNumberId": str,
        "PhoneNumberArn": str,
        "PhoneNumber": str,
        "PhoneNumberCountryCode": PhoneNumberCountryCodeType,
        "PhoneNumberType": PhoneNumberTypeType,
        "PhoneNumberDescription": str,
        "TargetArn": str,
        "Tags": Dict[str, str],
        "PhoneNumberStatus": PhoneNumberStatusTypeDef,
    },
    total=False,
)

UserDataFiltersTypeDef = TypedDict(
    "UserDataFiltersTypeDef",
    {
        "Queues": Sequence[str],
        "ContactFilter": ContactFilterTypeDef,
        "RoutingProfiles": Sequence[str],
        "Agents": Sequence[str],
        "UserHierarchyGroups": Sequence[str],
    },
    total=False,
)

ListContactFlowModulesResponseTypeDef = TypedDict(
    "ListContactFlowModulesResponseTypeDef",
    {
        "ContactFlowModulesSummaryList": List[ContactFlowModuleSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeContactFlowModuleResponseTypeDef = TypedDict(
    "DescribeContactFlowModuleResponseTypeDef",
    {
        "ContactFlowModule": ContactFlowModuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListContactFlowsResponseTypeDef = TypedDict(
    "ListContactFlowsResponseTypeDef",
    {
        "ContactFlowSummaryList": List[ContactFlowSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeContactFlowResponseTypeDef = TypedDict(
    "DescribeContactFlowResponseTypeDef",
    {
        "ContactFlow": ContactFlowTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ContactTypeDef = TypedDict(
    "ContactTypeDef",
    {
        "Arn": str,
        "Id": str,
        "InitialContactId": str,
        "PreviousContactId": str,
        "InitiationMethod": ContactInitiationMethodType,
        "Name": str,
        "Description": str,
        "Channel": ChannelType,
        "QueueInfo": QueueInfoTypeDef,
        "AgentInfo": AgentInfoTypeDef,
        "InitiationTimestamp": datetime,
        "DisconnectTimestamp": datetime,
        "LastUpdateTimestamp": datetime,
        "ScheduledTimestamp": datetime,
        "RelatedContactId": str,
        "WisdomInfo": WisdomInfoTypeDef,
    },
    total=False,
)

ControlPlaneTagFilterTypeDef = TypedDict(
    "ControlPlaneTagFilterTypeDef",
    {
        "OrConditions": Sequence[Sequence[TagConditionTypeDef]],
        "AndConditions": Sequence[TagConditionTypeDef],
        "TagCondition": TagConditionTypeDef,
    },
    total=False,
)

_RequiredCreateParticipantRequestRequestTypeDef = TypedDict(
    "_RequiredCreateParticipantRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
        "ParticipantDetails": ParticipantDetailsToAddTypeDef,
    },
)
_OptionalCreateParticipantRequestRequestTypeDef = TypedDict(
    "_OptionalCreateParticipantRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)

class CreateParticipantRequestRequestTypeDef(
    _RequiredCreateParticipantRequestRequestTypeDef, _OptionalCreateParticipantRequestRequestTypeDef
):
    pass

CreateParticipantResponseTypeDef = TypedDict(
    "CreateParticipantResponseTypeDef",
    {
        "ParticipantCredentials": ParticipantTokenCredentialsTypeDef,
        "ParticipantId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateQueueRequestRequestTypeDef = TypedDict(
    "_RequiredCreateQueueRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Name": str,
        "HoursOfOperationId": str,
    },
)
_OptionalCreateQueueRequestRequestTypeDef = TypedDict(
    "_OptionalCreateQueueRequestRequestTypeDef",
    {
        "Description": str,
        "OutboundCallerConfig": OutboundCallerConfigTypeDef,
        "MaxContacts": int,
        "QuickConnectIds": Sequence[str],
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateQueueRequestRequestTypeDef(
    _RequiredCreateQueueRequestRequestTypeDef, _OptionalCreateQueueRequestRequestTypeDef
):
    pass

QueueTypeDef = TypedDict(
    "QueueTypeDef",
    {
        "Name": str,
        "QueueArn": str,
        "QueueId": str,
        "Description": str,
        "OutboundCallerConfig": OutboundCallerConfigTypeDef,
        "HoursOfOperationId": str,
        "MaxContacts": int,
        "Status": QueueStatusType,
        "Tags": Dict[str, str],
    },
    total=False,
)

UpdateQueueOutboundCallerConfigRequestRequestTypeDef = TypedDict(
    "UpdateQueueOutboundCallerConfigRequestRequestTypeDef",
    {
        "InstanceId": str,
        "QueueId": str,
        "OutboundCallerConfig": OutboundCallerConfigTypeDef,
    },
)

UpdateUserIdentityInfoRequestRequestTypeDef = TypedDict(
    "UpdateUserIdentityInfoRequestRequestTypeDef",
    {
        "IdentityInfo": UserIdentityInfoTypeDef,
        "UserId": str,
        "InstanceId": str,
    },
)

_RequiredCreateUserRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserRequestRequestTypeDef",
    {
        "Username": str,
        "PhoneConfig": UserPhoneConfigTypeDef,
        "SecurityProfileIds": Sequence[str],
        "RoutingProfileId": str,
        "InstanceId": str,
    },
)
_OptionalCreateUserRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserRequestRequestTypeDef",
    {
        "Password": str,
        "IdentityInfo": UserIdentityInfoTypeDef,
        "DirectoryUserId": str,
        "HierarchyGroupId": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateUserRequestRequestTypeDef(
    _RequiredCreateUserRequestRequestTypeDef, _OptionalCreateUserRequestRequestTypeDef
):
    pass

UpdateUserPhoneConfigRequestRequestTypeDef = TypedDict(
    "UpdateUserPhoneConfigRequestRequestTypeDef",
    {
        "PhoneConfig": UserPhoneConfigTypeDef,
        "UserId": str,
        "InstanceId": str,
    },
)

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Username": str,
        "IdentityInfo": UserIdentityInfoTypeDef,
        "PhoneConfig": UserPhoneConfigTypeDef,
        "DirectoryUserId": str,
        "SecurityProfileIds": List[str],
        "RoutingProfileId": str,
        "HierarchyGroupId": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

GetFederationTokenResponseTypeDef = TypedDict(
    "GetFederationTokenResponseTypeDef",
    {
        "Credentials": CredentialsTypeDef,
        "SignInUrl": str,
        "UserArn": str,
        "UserId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredMediaConcurrencyTypeDef = TypedDict(
    "_RequiredMediaConcurrencyTypeDef",
    {
        "Channel": ChannelType,
        "Concurrency": int,
    },
)
_OptionalMediaConcurrencyTypeDef = TypedDict(
    "_OptionalMediaConcurrencyTypeDef",
    {
        "CrossChannelBehavior": CrossChannelBehaviorTypeDef,
    },
    total=False,
)

class MediaConcurrencyTypeDef(_RequiredMediaConcurrencyTypeDef, _OptionalMediaConcurrencyTypeDef):
    pass

CurrentMetricDataTypeDef = TypedDict(
    "CurrentMetricDataTypeDef",
    {
        "Metric": CurrentMetricTypeDef,
        "Value": float,
    },
    total=False,
)

ListDefaultVocabulariesResponseTypeDef = TypedDict(
    "ListDefaultVocabulariesResponseTypeDef",
    {
        "DefaultVocabularyList": List[DefaultVocabularyTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSecurityProfileResponseTypeDef = TypedDict(
    "DescribeSecurityProfileResponseTypeDef",
    {
        "SecurityProfile": SecurityProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTrafficDistributionGroupResponseTypeDef = TypedDict(
    "DescribeTrafficDistributionGroupResponseTypeDef",
    {
        "TrafficDistributionGroup": TrafficDistributionGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVocabularyResponseTypeDef = TypedDict(
    "DescribeVocabularyResponseTypeDef",
    {
        "Vocabulary": VocabularyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DimensionsTypeDef = TypedDict(
    "DimensionsTypeDef",
    {
        "Queue": QueueReferenceTypeDef,
        "Channel": ChannelType,
        "RoutingProfile": RoutingProfileReferenceTypeDef,
    },
    total=False,
)

DisassociateRoutingProfileQueuesRequestRequestTypeDef = TypedDict(
    "DisassociateRoutingProfileQueuesRequestRequestTypeDef",
    {
        "InstanceId": str,
        "RoutingProfileId": str,
        "QueueReferences": Sequence[RoutingProfileQueueReferenceTypeDef],
    },
)

RoutingProfileQueueConfigTypeDef = TypedDict(
    "RoutingProfileQueueConfigTypeDef",
    {
        "QueueReference": RoutingProfileQueueReferenceTypeDef,
        "Priority": int,
        "Delay": int,
    },
)

TelephonyConfigTypeDef = TypedDict(
    "TelephonyConfigTypeDef",
    {
        "Distributions": List[DistributionTypeDef],
    },
)

KinesisVideoStreamConfigTypeDef = TypedDict(
    "KinesisVideoStreamConfigTypeDef",
    {
        "Prefix": str,
        "RetentionPeriodHours": int,
        "EncryptionConfig": EncryptionConfigTypeDef,
    },
)

_RequiredS3ConfigTypeDef = TypedDict(
    "_RequiredS3ConfigTypeDef",
    {
        "BucketName": str,
        "BucketPrefix": str,
    },
)
_OptionalS3ConfigTypeDef = TypedDict(
    "_OptionalS3ConfigTypeDef",
    {
        "EncryptionConfig": EncryptionConfigTypeDef,
    },
    total=False,
)

class S3ConfigTypeDef(_RequiredS3ConfigTypeDef, _OptionalS3ConfigTypeDef):
    pass

_RequiredGetCurrentMetricDataRequestRequestTypeDef = TypedDict(
    "_RequiredGetCurrentMetricDataRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Filters": FiltersTypeDef,
        "CurrentMetrics": Sequence[CurrentMetricTypeDef],
    },
)
_OptionalGetCurrentMetricDataRequestRequestTypeDef = TypedDict(
    "_OptionalGetCurrentMetricDataRequestRequestTypeDef",
    {
        "Groupings": Sequence[GroupingType],
        "NextToken": str,
        "MaxResults": int,
        "SortCriteria": Sequence[CurrentMetricSortCriteriaTypeDef],
    },
    total=False,
)

class GetCurrentMetricDataRequestRequestTypeDef(
    _RequiredGetCurrentMetricDataRequestRequestTypeDef,
    _OptionalGetCurrentMetricDataRequestRequestTypeDef,
):
    pass

_RequiredListAgentStatusRequestListAgentStatusesPaginateTypeDef = TypedDict(
    "_RequiredListAgentStatusRequestListAgentStatusesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListAgentStatusRequestListAgentStatusesPaginateTypeDef = TypedDict(
    "_OptionalListAgentStatusRequestListAgentStatusesPaginateTypeDef",
    {
        "AgentStatusTypes": Sequence[AgentStatusTypeType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListAgentStatusRequestListAgentStatusesPaginateTypeDef(
    _RequiredListAgentStatusRequestListAgentStatusesPaginateTypeDef,
    _OptionalListAgentStatusRequestListAgentStatusesPaginateTypeDef,
):
    pass

_RequiredListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef = TypedDict(
    "_RequiredListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef = TypedDict(
    "_OptionalListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef(
    _RequiredListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef,
    _OptionalListApprovedOriginsRequestListApprovedOriginsPaginateTypeDef,
):
    pass

_RequiredListBotsRequestListBotsPaginateTypeDef = TypedDict(
    "_RequiredListBotsRequestListBotsPaginateTypeDef",
    {
        "InstanceId": str,
        "LexVersion": LexVersionType,
    },
)
_OptionalListBotsRequestListBotsPaginateTypeDef = TypedDict(
    "_OptionalListBotsRequestListBotsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListBotsRequestListBotsPaginateTypeDef(
    _RequiredListBotsRequestListBotsPaginateTypeDef, _OptionalListBotsRequestListBotsPaginateTypeDef
):
    pass

_RequiredListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef = TypedDict(
    "_RequiredListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef = TypedDict(
    "_OptionalListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef",
    {
        "ContactFlowModuleState": ContactFlowModuleStateType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef(
    _RequiredListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef,
    _OptionalListContactFlowModulesRequestListContactFlowModulesPaginateTypeDef,
):
    pass

_RequiredListContactFlowsRequestListContactFlowsPaginateTypeDef = TypedDict(
    "_RequiredListContactFlowsRequestListContactFlowsPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListContactFlowsRequestListContactFlowsPaginateTypeDef = TypedDict(
    "_OptionalListContactFlowsRequestListContactFlowsPaginateTypeDef",
    {
        "ContactFlowTypes": Sequence[ContactFlowTypeType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListContactFlowsRequestListContactFlowsPaginateTypeDef(
    _RequiredListContactFlowsRequestListContactFlowsPaginateTypeDef,
    _OptionalListContactFlowsRequestListContactFlowsPaginateTypeDef,
):
    pass

_RequiredListContactReferencesRequestListContactReferencesPaginateTypeDef = TypedDict(
    "_RequiredListContactReferencesRequestListContactReferencesPaginateTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
        "ReferenceTypes": Sequence[ReferenceTypeType],
    },
)
_OptionalListContactReferencesRequestListContactReferencesPaginateTypeDef = TypedDict(
    "_OptionalListContactReferencesRequestListContactReferencesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListContactReferencesRequestListContactReferencesPaginateTypeDef(
    _RequiredListContactReferencesRequestListContactReferencesPaginateTypeDef,
    _OptionalListContactReferencesRequestListContactReferencesPaginateTypeDef,
):
    pass

_RequiredListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef = TypedDict(
    "_RequiredListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef = TypedDict(
    "_OptionalListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef",
    {
        "LanguageCode": VocabularyLanguageCodeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef(
    _RequiredListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef,
    _OptionalListDefaultVocabulariesRequestListDefaultVocabulariesPaginateTypeDef,
):
    pass

_RequiredListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef = TypedDict(
    "_RequiredListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef = TypedDict(
    "_OptionalListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef(
    _RequiredListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef,
    _OptionalListHoursOfOperationsRequestListHoursOfOperationsPaginateTypeDef,
):
    pass

_RequiredListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef = TypedDict(
    "_RequiredListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef = TypedDict(
    "_OptionalListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef(
    _RequiredListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef,
    _OptionalListInstanceAttributesRequestListInstanceAttributesPaginateTypeDef,
):
    pass

_RequiredListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef = TypedDict(
    "_RequiredListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef",
    {
        "InstanceId": str,
        "ResourceType": InstanceStorageResourceTypeType,
    },
)
_OptionalListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef = TypedDict(
    "_OptionalListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef(
    _RequiredListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef,
    _OptionalListInstanceStorageConfigsRequestListInstanceStorageConfigsPaginateTypeDef,
):
    pass

ListInstancesRequestListInstancesPaginateTypeDef = TypedDict(
    "ListInstancesRequestListInstancesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef = TypedDict(
    "_RequiredListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef = TypedDict(
    "_OptionalListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef",
    {
        "IntegrationType": IntegrationTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef(
    _RequiredListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef,
    _OptionalListIntegrationAssociationsRequestListIntegrationAssociationsPaginateTypeDef,
):
    pass

_RequiredListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef = TypedDict(
    "_RequiredListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef = TypedDict(
    "_OptionalListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef(
    _RequiredListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef,
    _OptionalListLambdaFunctionsRequestListLambdaFunctionsPaginateTypeDef,
):
    pass

_RequiredListLexBotsRequestListLexBotsPaginateTypeDef = TypedDict(
    "_RequiredListLexBotsRequestListLexBotsPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListLexBotsRequestListLexBotsPaginateTypeDef = TypedDict(
    "_OptionalListLexBotsRequestListLexBotsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListLexBotsRequestListLexBotsPaginateTypeDef(
    _RequiredListLexBotsRequestListLexBotsPaginateTypeDef,
    _OptionalListLexBotsRequestListLexBotsPaginateTypeDef,
):
    pass

_RequiredListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef = TypedDict(
    "_RequiredListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef = TypedDict(
    "_OptionalListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef",
    {
        "PhoneNumberTypes": Sequence[PhoneNumberTypeType],
        "PhoneNumberCountryCodes": Sequence[PhoneNumberCountryCodeType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef(
    _RequiredListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef,
    _OptionalListPhoneNumbersRequestListPhoneNumbersPaginateTypeDef,
):
    pass

ListPhoneNumbersV2RequestListPhoneNumbersV2PaginateTypeDef = TypedDict(
    "ListPhoneNumbersV2RequestListPhoneNumbersV2PaginateTypeDef",
    {
        "TargetArn": str,
        "PhoneNumberCountryCodes": Sequence[PhoneNumberCountryCodeType],
        "PhoneNumberTypes": Sequence[PhoneNumberTypeType],
        "PhoneNumberPrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListPromptsRequestListPromptsPaginateTypeDef = TypedDict(
    "_RequiredListPromptsRequestListPromptsPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListPromptsRequestListPromptsPaginateTypeDef = TypedDict(
    "_OptionalListPromptsRequestListPromptsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListPromptsRequestListPromptsPaginateTypeDef(
    _RequiredListPromptsRequestListPromptsPaginateTypeDef,
    _OptionalListPromptsRequestListPromptsPaginateTypeDef,
):
    pass

_RequiredListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef = TypedDict(
    "_RequiredListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef",
    {
        "InstanceId": str,
        "QueueId": str,
    },
)
_OptionalListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef = TypedDict(
    "_OptionalListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef(
    _RequiredListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef,
    _OptionalListQueueQuickConnectsRequestListQueueQuickConnectsPaginateTypeDef,
):
    pass

_RequiredListQueuesRequestListQueuesPaginateTypeDef = TypedDict(
    "_RequiredListQueuesRequestListQueuesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListQueuesRequestListQueuesPaginateTypeDef = TypedDict(
    "_OptionalListQueuesRequestListQueuesPaginateTypeDef",
    {
        "QueueTypes": Sequence[QueueTypeType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListQueuesRequestListQueuesPaginateTypeDef(
    _RequiredListQueuesRequestListQueuesPaginateTypeDef,
    _OptionalListQueuesRequestListQueuesPaginateTypeDef,
):
    pass

_RequiredListQuickConnectsRequestListQuickConnectsPaginateTypeDef = TypedDict(
    "_RequiredListQuickConnectsRequestListQuickConnectsPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListQuickConnectsRequestListQuickConnectsPaginateTypeDef = TypedDict(
    "_OptionalListQuickConnectsRequestListQuickConnectsPaginateTypeDef",
    {
        "QuickConnectTypes": Sequence[QuickConnectTypeType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListQuickConnectsRequestListQuickConnectsPaginateTypeDef(
    _RequiredListQuickConnectsRequestListQuickConnectsPaginateTypeDef,
    _OptionalListQuickConnectsRequestListQuickConnectsPaginateTypeDef,
):
    pass

_RequiredListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef = TypedDict(
    "_RequiredListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef",
    {
        "InstanceId": str,
        "RoutingProfileId": str,
    },
)
_OptionalListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef = TypedDict(
    "_OptionalListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef(
    _RequiredListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef,
    _OptionalListRoutingProfileQueuesRequestListRoutingProfileQueuesPaginateTypeDef,
):
    pass

_RequiredListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef = TypedDict(
    "_RequiredListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef = TypedDict(
    "_OptionalListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef(
    _RequiredListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef,
    _OptionalListRoutingProfilesRequestListRoutingProfilesPaginateTypeDef,
):
    pass

_RequiredListRulesRequestListRulesPaginateTypeDef = TypedDict(
    "_RequiredListRulesRequestListRulesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListRulesRequestListRulesPaginateTypeDef = TypedDict(
    "_OptionalListRulesRequestListRulesPaginateTypeDef",
    {
        "PublishStatus": RulePublishStatusType,
        "EventSourceName": EventSourceNameType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListRulesRequestListRulesPaginateTypeDef(
    _RequiredListRulesRequestListRulesPaginateTypeDef,
    _OptionalListRulesRequestListRulesPaginateTypeDef,
):
    pass

_RequiredListSecurityKeysRequestListSecurityKeysPaginateTypeDef = TypedDict(
    "_RequiredListSecurityKeysRequestListSecurityKeysPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListSecurityKeysRequestListSecurityKeysPaginateTypeDef = TypedDict(
    "_OptionalListSecurityKeysRequestListSecurityKeysPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListSecurityKeysRequestListSecurityKeysPaginateTypeDef(
    _RequiredListSecurityKeysRequestListSecurityKeysPaginateTypeDef,
    _OptionalListSecurityKeysRequestListSecurityKeysPaginateTypeDef,
):
    pass

_RequiredListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef = TypedDict(
    "_RequiredListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef",
    {
        "SecurityProfileId": str,
        "InstanceId": str,
    },
)
_OptionalListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef = TypedDict(
    "_OptionalListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef(
    _RequiredListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef,
    _OptionalListSecurityProfilePermissionsRequestListSecurityProfilePermissionsPaginateTypeDef,
):
    pass

_RequiredListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef = TypedDict(
    "_RequiredListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef = TypedDict(
    "_OptionalListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef(
    _RequiredListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef,
    _OptionalListSecurityProfilesRequestListSecurityProfilesPaginateTypeDef,
):
    pass

_RequiredListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef = TypedDict(
    "_RequiredListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef = TypedDict(
    "_OptionalListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef",
    {
        "Status": TaskTemplateStatusType,
        "Name": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef(
    _RequiredListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef,
    _OptionalListTaskTemplatesRequestListTaskTemplatesPaginateTypeDef,
):
    pass

ListTrafficDistributionGroupsRequestListTrafficDistributionGroupsPaginateTypeDef = TypedDict(
    "ListTrafficDistributionGroupsRequestListTrafficDistributionGroupsPaginateTypeDef",
    {
        "InstanceId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListUseCasesRequestListUseCasesPaginateTypeDef = TypedDict(
    "_RequiredListUseCasesRequestListUseCasesPaginateTypeDef",
    {
        "InstanceId": str,
        "IntegrationAssociationId": str,
    },
)
_OptionalListUseCasesRequestListUseCasesPaginateTypeDef = TypedDict(
    "_OptionalListUseCasesRequestListUseCasesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListUseCasesRequestListUseCasesPaginateTypeDef(
    _RequiredListUseCasesRequestListUseCasesPaginateTypeDef,
    _OptionalListUseCasesRequestListUseCasesPaginateTypeDef,
):
    pass

_RequiredListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef = TypedDict(
    "_RequiredListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef = TypedDict(
    "_OptionalListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef(
    _RequiredListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef,
    _OptionalListUserHierarchyGroupsRequestListUserHierarchyGroupsPaginateTypeDef,
):
    pass

_RequiredListUsersRequestListUsersPaginateTypeDef = TypedDict(
    "_RequiredListUsersRequestListUsersPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalListUsersRequestListUsersPaginateTypeDef = TypedDict(
    "_OptionalListUsersRequestListUsersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListUsersRequestListUsersPaginateTypeDef(
    _RequiredListUsersRequestListUsersPaginateTypeDef,
    _OptionalListUsersRequestListUsersPaginateTypeDef,
):
    pass

_RequiredSearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef = TypedDict(
    "_RequiredSearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef",
    {
        "TargetArn": str,
        "PhoneNumberCountryCode": PhoneNumberCountryCodeType,
        "PhoneNumberType": PhoneNumberTypeType,
    },
)
_OptionalSearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef = TypedDict(
    "_OptionalSearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef",
    {
        "PhoneNumberPrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class SearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef(
    _RequiredSearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef,
    _OptionalSearchAvailablePhoneNumbersRequestSearchAvailablePhoneNumbersPaginateTypeDef,
):
    pass

_RequiredSearchVocabulariesRequestSearchVocabulariesPaginateTypeDef = TypedDict(
    "_RequiredSearchVocabulariesRequestSearchVocabulariesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalSearchVocabulariesRequestSearchVocabulariesPaginateTypeDef = TypedDict(
    "_OptionalSearchVocabulariesRequestSearchVocabulariesPaginateTypeDef",
    {
        "State": VocabularyStateType,
        "NameStartsWith": str,
        "LanguageCode": VocabularyLanguageCodeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class SearchVocabulariesRequestSearchVocabulariesPaginateTypeDef(
    _RequiredSearchVocabulariesRequestSearchVocabulariesPaginateTypeDef,
    _OptionalSearchVocabulariesRequestSearchVocabulariesPaginateTypeDef,
):
    pass

HierarchyPathReferenceTypeDef = TypedDict(
    "HierarchyPathReferenceTypeDef",
    {
        "LevelOne": HierarchyGroupSummaryReferenceTypeDef,
        "LevelTwo": HierarchyGroupSummaryReferenceTypeDef,
        "LevelThree": HierarchyGroupSummaryReferenceTypeDef,
        "LevelFour": HierarchyGroupSummaryReferenceTypeDef,
        "LevelFive": HierarchyGroupSummaryReferenceTypeDef,
    },
    total=False,
)

HierarchyPathTypeDef = TypedDict(
    "HierarchyPathTypeDef",
    {
        "LevelOne": HierarchyGroupSummaryTypeDef,
        "LevelTwo": HierarchyGroupSummaryTypeDef,
        "LevelThree": HierarchyGroupSummaryTypeDef,
        "LevelFour": HierarchyGroupSummaryTypeDef,
        "LevelFive": HierarchyGroupSummaryTypeDef,
    },
    total=False,
)

ListUserHierarchyGroupsResponseTypeDef = TypedDict(
    "ListUserHierarchyGroupsResponseTypeDef",
    {
        "UserHierarchyGroupSummaryList": List[HierarchyGroupSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

HierarchyStructureTypeDef = TypedDict(
    "HierarchyStructureTypeDef",
    {
        "LevelOne": HierarchyLevelTypeDef,
        "LevelTwo": HierarchyLevelTypeDef,
        "LevelThree": HierarchyLevelTypeDef,
        "LevelFour": HierarchyLevelTypeDef,
        "LevelFive": HierarchyLevelTypeDef,
    },
    total=False,
)

HierarchyStructureUpdateTypeDef = TypedDict(
    "HierarchyStructureUpdateTypeDef",
    {
        "LevelOne": HierarchyLevelUpdateTypeDef,
        "LevelTwo": HierarchyLevelUpdateTypeDef,
        "LevelThree": HierarchyLevelUpdateTypeDef,
        "LevelFour": HierarchyLevelUpdateTypeDef,
        "LevelFive": HierarchyLevelUpdateTypeDef,
    },
    total=False,
)

HistoricalMetricTypeDef = TypedDict(
    "HistoricalMetricTypeDef",
    {
        "Name": HistoricalMetricNameType,
        "Threshold": ThresholdTypeDef,
        "Statistic": StatisticType,
        "Unit": UnitType,
    },
    total=False,
)

HoursOfOperationConfigTypeDef = TypedDict(
    "HoursOfOperationConfigTypeDef",
    {
        "Day": HoursOfOperationDaysType,
        "StartTime": HoursOfOperationTimeSliceTypeDef,
        "EndTime": HoursOfOperationTimeSliceTypeDef,
    },
)

ListHoursOfOperationsResponseTypeDef = TypedDict(
    "ListHoursOfOperationsResponseTypeDef",
    {
        "HoursOfOperationSummaryList": List[HoursOfOperationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstanceTypeDef = TypedDict(
    "InstanceTypeDef",
    {
        "Id": str,
        "Arn": str,
        "IdentityManagementType": DirectoryTypeType,
        "InstanceAlias": str,
        "CreatedTime": datetime,
        "ServiceRole": str,
        "InstanceStatus": InstanceStatusType,
        "StatusReason": InstanceStatusReasonTypeDef,
        "InboundCallsEnabled": bool,
        "OutboundCallsEnabled": bool,
    },
    total=False,
)

ListInstancesResponseTypeDef = TypedDict(
    "ListInstancesResponseTypeDef",
    {
        "InstanceSummaryList": List[InstanceSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIntegrationAssociationsResponseTypeDef = TypedDict(
    "ListIntegrationAssociationsResponseTypeDef",
    {
        "IntegrationAssociationSummaryList": List[IntegrationAssociationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InvisibleFieldInfoTypeDef = TypedDict(
    "InvisibleFieldInfoTypeDef",
    {
        "Id": TaskTemplateFieldIdentifierTypeDef,
    },
    total=False,
)

ReadOnlyFieldInfoTypeDef = TypedDict(
    "ReadOnlyFieldInfoTypeDef",
    {
        "Id": TaskTemplateFieldIdentifierTypeDef,
    },
    total=False,
)

RequiredFieldInfoTypeDef = TypedDict(
    "RequiredFieldInfoTypeDef",
    {
        "Id": TaskTemplateFieldIdentifierTypeDef,
    },
    total=False,
)

TaskTemplateDefaultFieldValueTypeDef = TypedDict(
    "TaskTemplateDefaultFieldValueTypeDef",
    {
        "Id": TaskTemplateFieldIdentifierTypeDef,
        "DefaultValue": str,
    },
    total=False,
)

_RequiredTaskTemplateFieldTypeDef = TypedDict(
    "_RequiredTaskTemplateFieldTypeDef",
    {
        "Id": TaskTemplateFieldIdentifierTypeDef,
    },
)
_OptionalTaskTemplateFieldTypeDef = TypedDict(
    "_OptionalTaskTemplateFieldTypeDef",
    {
        "Description": str,
        "Type": TaskTemplateFieldTypeType,
        "SingleSelectOptions": Sequence[str],
    },
    total=False,
)

class TaskTemplateFieldTypeDef(
    _RequiredTaskTemplateFieldTypeDef, _OptionalTaskTemplateFieldTypeDef
):
    pass

ListPhoneNumbersResponseTypeDef = TypedDict(
    "ListPhoneNumbersResponseTypeDef",
    {
        "PhoneNumberSummaryList": List[PhoneNumberSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPhoneNumbersV2ResponseTypeDef = TypedDict(
    "ListPhoneNumbersV2ResponseTypeDef",
    {
        "NextToken": str,
        "ListPhoneNumbersSummaryList": List[ListPhoneNumbersSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPromptsResponseTypeDef = TypedDict(
    "ListPromptsResponseTypeDef",
    {
        "PromptSummaryList": List[PromptSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListQueueQuickConnectsResponseTypeDef = TypedDict(
    "ListQueueQuickConnectsResponseTypeDef",
    {
        "NextToken": str,
        "QuickConnectSummaryList": List[QuickConnectSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListQuickConnectsResponseTypeDef = TypedDict(
    "ListQuickConnectsResponseTypeDef",
    {
        "QuickConnectSummaryList": List[QuickConnectSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListQueuesResponseTypeDef = TypedDict(
    "ListQueuesResponseTypeDef",
    {
        "QueueSummaryList": List[QueueSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRoutingProfileQueuesResponseTypeDef = TypedDict(
    "ListRoutingProfileQueuesResponseTypeDef",
    {
        "NextToken": str,
        "RoutingProfileQueueConfigSummaryList": List[RoutingProfileQueueConfigSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRoutingProfilesResponseTypeDef = TypedDict(
    "ListRoutingProfilesResponseTypeDef",
    {
        "RoutingProfileSummaryList": List[RoutingProfileSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSecurityKeysResponseTypeDef = TypedDict(
    "ListSecurityKeysResponseTypeDef",
    {
        "SecurityKeys": List[SecurityKeyTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSecurityProfilesResponseTypeDef = TypedDict(
    "ListSecurityProfilesResponseTypeDef",
    {
        "SecurityProfileSummaryList": List[SecurityProfileSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTaskTemplatesResponseTypeDef = TypedDict(
    "ListTaskTemplatesResponseTypeDef",
    {
        "TaskTemplates": List[TaskTemplateMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTrafficDistributionGroupsResponseTypeDef = TypedDict(
    "ListTrafficDistributionGroupsResponseTypeDef",
    {
        "NextToken": str,
        "TrafficDistributionGroupSummaryList": List[TrafficDistributionGroupSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUseCasesResponseTypeDef = TypedDict(
    "ListUseCasesResponseTypeDef",
    {
        "UseCaseSummaryList": List[UseCaseTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef",
    {
        "UserSummaryList": List[UserSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MetricV2TypeDef = TypedDict(
    "MetricV2TypeDef",
    {
        "Name": str,
        "Threshold": Sequence[ThresholdV2TypeDef],
        "MetricFilters": Sequence[MetricFilterV2TypeDef],
    },
    total=False,
)

_RequiredSendNotificationActionDefinitionTypeDef = TypedDict(
    "_RequiredSendNotificationActionDefinitionTypeDef",
    {
        "DeliveryMethod": Literal["EMAIL"],
        "Content": str,
        "ContentType": Literal["PLAIN_TEXT"],
        "Recipient": NotificationRecipientTypeTypeDef,
    },
)
_OptionalSendNotificationActionDefinitionTypeDef = TypedDict(
    "_OptionalSendNotificationActionDefinitionTypeDef",
    {
        "Subject": str,
    },
    total=False,
)

class SendNotificationActionDefinitionTypeDef(
    _RequiredSendNotificationActionDefinitionTypeDef,
    _OptionalSendNotificationActionDefinitionTypeDef,
):
    pass

ParticipantTimerConfigurationTypeDef = TypedDict(
    "ParticipantTimerConfigurationTypeDef",
    {
        "ParticipantRole": TimerEligibleParticipantRolesType,
        "TimerType": ParticipantTimerTypeType,
        "TimerValue": ParticipantTimerValueTypeDef,
    },
)

_RequiredStartChatContactRequestRequestTypeDef = TypedDict(
    "_RequiredStartChatContactRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactFlowId": str,
        "ParticipantDetails": ParticipantDetailsTypeDef,
    },
)
_OptionalStartChatContactRequestRequestTypeDef = TypedDict(
    "_OptionalStartChatContactRequestRequestTypeDef",
    {
        "Attributes": Mapping[str, str],
        "InitialMessage": ChatMessageTypeDef,
        "ClientToken": str,
        "ChatDurationInMinutes": int,
        "SupportedMessagingContentTypes": Sequence[str],
        "PersistentChat": PersistentChatTypeDef,
        "RelatedContactId": str,
    },
    total=False,
)

class StartChatContactRequestRequestTypeDef(
    _RequiredStartChatContactRequestRequestTypeDef, _OptionalStartChatContactRequestRequestTypeDef
):
    pass

QueueSearchCriteriaTypeDef = TypedDict(
    "QueueSearchCriteriaTypeDef",
    {
        "OrConditions": Sequence[Dict[str, Any]],
        "AndConditions": Sequence[Dict[str, Any]],
        "StringCondition": StringConditionTypeDef,
        "QueueTypeCondition": Literal["STANDARD"],
    },
    total=False,
)

RoutingProfileSearchCriteriaTypeDef = TypedDict(
    "RoutingProfileSearchCriteriaTypeDef",
    {
        "OrConditions": Sequence[Dict[str, Any]],
        "AndConditions": Sequence[Dict[str, Any]],
        "StringCondition": StringConditionTypeDef,
    },
    total=False,
)

SecurityProfileSearchCriteriaTypeDef = TypedDict(
    "SecurityProfileSearchCriteriaTypeDef",
    {
        "OrConditions": Sequence[Dict[str, Any]],
        "AndConditions": Sequence[Dict[str, Any]],
        "StringCondition": StringConditionTypeDef,
    },
    total=False,
)

UserSearchCriteriaTypeDef = TypedDict(
    "UserSearchCriteriaTypeDef",
    {
        "OrConditions": Sequence[Dict[str, Any]],
        "AndConditions": Sequence[Dict[str, Any]],
        "StringCondition": StringConditionTypeDef,
        "HierarchyGroupCondition": HierarchyGroupConditionTypeDef,
    },
    total=False,
)

_RequiredQuickConnectConfigTypeDef = TypedDict(
    "_RequiredQuickConnectConfigTypeDef",
    {
        "QuickConnectType": QuickConnectTypeType,
    },
)
_OptionalQuickConnectConfigTypeDef = TypedDict(
    "_OptionalQuickConnectConfigTypeDef",
    {
        "UserConfig": UserQuickConnectConfigTypeDef,
        "QueueConfig": QueueQuickConnectConfigTypeDef,
        "PhoneConfig": PhoneNumberQuickConnectConfigTypeDef,
    },
    total=False,
)

class QuickConnectConfigTypeDef(
    _RequiredQuickConnectConfigTypeDef, _OptionalQuickConnectConfigTypeDef
):
    pass

ReferenceSummaryTypeDef = TypedDict(
    "ReferenceSummaryTypeDef",
    {
        "Url": UrlReferenceTypeDef,
        "Attachment": AttachmentReferenceTypeDef,
        "String": StringReferenceTypeDef,
        "Number": NumberReferenceTypeDef,
        "Date": DateReferenceTypeDef,
        "Email": EmailReferenceTypeDef,
    },
    total=False,
)

_RequiredStartTaskContactRequestRequestTypeDef = TypedDict(
    "_RequiredStartTaskContactRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Name": str,
    },
)
_OptionalStartTaskContactRequestRequestTypeDef = TypedDict(
    "_OptionalStartTaskContactRequestRequestTypeDef",
    {
        "PreviousContactId": str,
        "ContactFlowId": str,
        "Attributes": Mapping[str, str],
        "References": Mapping[str, ReferenceTypeDef],
        "Description": str,
        "ClientToken": str,
        "ScheduledTime": Union[datetime, str],
        "TaskTemplateId": str,
        "QuickConnectId": str,
        "RelatedContactId": str,
    },
    total=False,
)

class StartTaskContactRequestRequestTypeDef(
    _RequiredStartTaskContactRequestRequestTypeDef, _OptionalStartTaskContactRequestRequestTypeDef
):
    pass

_RequiredTaskActionDefinitionTypeDef = TypedDict(
    "_RequiredTaskActionDefinitionTypeDef",
    {
        "Name": str,
        "ContactFlowId": str,
    },
)
_OptionalTaskActionDefinitionTypeDef = TypedDict(
    "_OptionalTaskActionDefinitionTypeDef",
    {
        "Description": str,
        "References": Mapping[str, ReferenceTypeDef],
    },
    total=False,
)

class TaskActionDefinitionTypeDef(
    _RequiredTaskActionDefinitionTypeDef, _OptionalTaskActionDefinitionTypeDef
):
    pass

_RequiredUpdateContactRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContactRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
    },
)
_OptionalUpdateContactRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContactRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "References": Mapping[str, ReferenceTypeDef],
    },
    total=False,
)

class UpdateContactRequestRequestTypeDef(
    _RequiredUpdateContactRequestRequestTypeDef, _OptionalUpdateContactRequestRequestTypeDef
):
    pass

SearchSecurityProfilesResponseTypeDef = TypedDict(
    "SearchSecurityProfilesResponseTypeDef",
    {
        "SecurityProfiles": List[SecurityProfileSearchSummaryTypeDef],
        "NextToken": str,
        "ApproximateTotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchVocabulariesResponseTypeDef = TypedDict(
    "SearchVocabulariesResponseTypeDef",
    {
        "VocabularySummaryList": List[VocabularySummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartContactRecordingRequestRequestTypeDef = TypedDict(
    "StartContactRecordingRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
        "InitialContactId": str,
        "VoiceRecordingConfiguration": VoiceRecordingConfigurationTypeDef,
    },
)

UserSearchSummaryTypeDef = TypedDict(
    "UserSearchSummaryTypeDef",
    {
        "Arn": str,
        "DirectoryUserId": str,
        "HierarchyGroupId": str,
        "Id": str,
        "IdentityInfo": UserIdentityInfoLiteTypeDef,
        "PhoneConfig": UserPhoneConfigTypeDef,
        "RoutingProfileId": str,
        "SecurityProfileIds": List[str],
        "Tags": Dict[str, str],
        "Username": str,
    },
    total=False,
)

ListRulesResponseTypeDef = TypedDict(
    "ListRulesResponseTypeDef",
    {
        "RuleSummaryList": List[RuleSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBotsResponseTypeDef = TypedDict(
    "ListBotsResponseTypeDef",
    {
        "LexBots": List[LexBotConfigTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePhoneNumberResponseTypeDef = TypedDict(
    "DescribePhoneNumberResponseTypeDef",
    {
        "ClaimedPhoneNumberSummary": ClaimedPhoneNumberSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetCurrentUserDataRequestRequestTypeDef = TypedDict(
    "_RequiredGetCurrentUserDataRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Filters": UserDataFiltersTypeDef,
    },
)
_OptionalGetCurrentUserDataRequestRequestTypeDef = TypedDict(
    "_OptionalGetCurrentUserDataRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class GetCurrentUserDataRequestRequestTypeDef(
    _RequiredGetCurrentUserDataRequestRequestTypeDef,
    _OptionalGetCurrentUserDataRequestRequestTypeDef,
):
    pass

DescribeContactResponseTypeDef = TypedDict(
    "DescribeContactResponseTypeDef",
    {
        "Contact": ContactTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

QueueSearchFilterTypeDef = TypedDict(
    "QueueSearchFilterTypeDef",
    {
        "TagFilter": ControlPlaneTagFilterTypeDef,
    },
    total=False,
)

RoutingProfileSearchFilterTypeDef = TypedDict(
    "RoutingProfileSearchFilterTypeDef",
    {
        "TagFilter": ControlPlaneTagFilterTypeDef,
    },
    total=False,
)

SecurityProfilesSearchFilterTypeDef = TypedDict(
    "SecurityProfilesSearchFilterTypeDef",
    {
        "TagFilter": ControlPlaneTagFilterTypeDef,
    },
    total=False,
)

UserSearchFilterTypeDef = TypedDict(
    "UserSearchFilterTypeDef",
    {
        "TagFilter": ControlPlaneTagFilterTypeDef,
    },
    total=False,
)

DescribeQueueResponseTypeDef = TypedDict(
    "DescribeQueueResponseTypeDef",
    {
        "Queue": QueueTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchQueuesResponseTypeDef = TypedDict(
    "SearchQueuesResponseTypeDef",
    {
        "Queues": List[QueueTypeDef],
        "NextToken": str,
        "ApproximateTotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUserResponseTypeDef = TypedDict(
    "DescribeUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RoutingProfileTypeDef = TypedDict(
    "RoutingProfileTypeDef",
    {
        "InstanceId": str,
        "Name": str,
        "RoutingProfileArn": str,
        "RoutingProfileId": str,
        "Description": str,
        "MediaConcurrencies": List[MediaConcurrencyTypeDef],
        "DefaultOutboundQueueId": str,
        "Tags": Dict[str, str],
        "NumberOfAssociatedQueues": int,
        "NumberOfAssociatedUsers": int,
    },
    total=False,
)

UpdateRoutingProfileConcurrencyRequestRequestTypeDef = TypedDict(
    "UpdateRoutingProfileConcurrencyRequestRequestTypeDef",
    {
        "InstanceId": str,
        "RoutingProfileId": str,
        "MediaConcurrencies": Sequence[MediaConcurrencyTypeDef],
    },
)

CurrentMetricResultTypeDef = TypedDict(
    "CurrentMetricResultTypeDef",
    {
        "Dimensions": DimensionsTypeDef,
        "Collections": List[CurrentMetricDataTypeDef],
    },
    total=False,
)

AssociateRoutingProfileQueuesRequestRequestTypeDef = TypedDict(
    "AssociateRoutingProfileQueuesRequestRequestTypeDef",
    {
        "InstanceId": str,
        "RoutingProfileId": str,
        "QueueConfigs": Sequence[RoutingProfileQueueConfigTypeDef],
    },
)

_RequiredCreateRoutingProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRoutingProfileRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Name": str,
        "Description": str,
        "DefaultOutboundQueueId": str,
        "MediaConcurrencies": Sequence[MediaConcurrencyTypeDef],
    },
)
_OptionalCreateRoutingProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRoutingProfileRequestRequestTypeDef",
    {
        "QueueConfigs": Sequence[RoutingProfileQueueConfigTypeDef],
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateRoutingProfileRequestRequestTypeDef(
    _RequiredCreateRoutingProfileRequestRequestTypeDef,
    _OptionalCreateRoutingProfileRequestRequestTypeDef,
):
    pass

UpdateRoutingProfileQueuesRequestRequestTypeDef = TypedDict(
    "UpdateRoutingProfileQueuesRequestRequestTypeDef",
    {
        "InstanceId": str,
        "RoutingProfileId": str,
        "QueueConfigs": Sequence[RoutingProfileQueueConfigTypeDef],
    },
)

GetTrafficDistributionResponseTypeDef = TypedDict(
    "GetTrafficDistributionResponseTypeDef",
    {
        "TelephonyConfig": TelephonyConfigTypeDef,
        "Id": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateTrafficDistributionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTrafficDistributionRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalUpdateTrafficDistributionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTrafficDistributionRequestRequestTypeDef",
    {
        "TelephonyConfig": TelephonyConfigTypeDef,
    },
    total=False,
)

class UpdateTrafficDistributionRequestRequestTypeDef(
    _RequiredUpdateTrafficDistributionRequestRequestTypeDef,
    _OptionalUpdateTrafficDistributionRequestRequestTypeDef,
):
    pass

_RequiredInstanceStorageConfigTypeDef = TypedDict(
    "_RequiredInstanceStorageConfigTypeDef",
    {
        "StorageType": StorageTypeType,
    },
)
_OptionalInstanceStorageConfigTypeDef = TypedDict(
    "_OptionalInstanceStorageConfigTypeDef",
    {
        "AssociationId": str,
        "S3Config": S3ConfigTypeDef,
        "KinesisVideoStreamConfig": KinesisVideoStreamConfigTypeDef,
        "KinesisStreamConfig": KinesisStreamConfigTypeDef,
        "KinesisFirehoseConfig": KinesisFirehoseConfigTypeDef,
    },
    total=False,
)

class InstanceStorageConfigTypeDef(
    _RequiredInstanceStorageConfigTypeDef, _OptionalInstanceStorageConfigTypeDef
):
    pass

UserDataTypeDef = TypedDict(
    "UserDataTypeDef",
    {
        "User": UserReferenceTypeDef,
        "RoutingProfile": RoutingProfileReferenceTypeDef,
        "HierarchyPath": HierarchyPathReferenceTypeDef,
        "Status": AgentStatusReferenceTypeDef,
        "AvailableSlotsByChannel": Dict[ChannelType, int],
        "MaxSlotsByChannel": Dict[ChannelType, int],
        "ActiveSlotsByChannel": Dict[ChannelType, int],
        "Contacts": List[AgentContactReferenceTypeDef],
        "NextStatus": str,
    },
    total=False,
)

HierarchyGroupTypeDef = TypedDict(
    "HierarchyGroupTypeDef",
    {
        "Id": str,
        "Arn": str,
        "Name": str,
        "LevelId": str,
        "HierarchyPath": HierarchyPathTypeDef,
        "Tags": Dict[str, str],
    },
    total=False,
)

DescribeUserHierarchyStructureResponseTypeDef = TypedDict(
    "DescribeUserHierarchyStructureResponseTypeDef",
    {
        "HierarchyStructure": HierarchyStructureTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateUserHierarchyStructureRequestRequestTypeDef = TypedDict(
    "UpdateUserHierarchyStructureRequestRequestTypeDef",
    {
        "HierarchyStructure": HierarchyStructureUpdateTypeDef,
        "InstanceId": str,
    },
)

_RequiredGetMetricDataRequestGetMetricDataPaginateTypeDef = TypedDict(
    "_RequiredGetMetricDataRequestGetMetricDataPaginateTypeDef",
    {
        "InstanceId": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Filters": FiltersTypeDef,
        "HistoricalMetrics": Sequence[HistoricalMetricTypeDef],
    },
)
_OptionalGetMetricDataRequestGetMetricDataPaginateTypeDef = TypedDict(
    "_OptionalGetMetricDataRequestGetMetricDataPaginateTypeDef",
    {
        "Groupings": Sequence[GroupingType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class GetMetricDataRequestGetMetricDataPaginateTypeDef(
    _RequiredGetMetricDataRequestGetMetricDataPaginateTypeDef,
    _OptionalGetMetricDataRequestGetMetricDataPaginateTypeDef,
):
    pass

_RequiredGetMetricDataRequestRequestTypeDef = TypedDict(
    "_RequiredGetMetricDataRequestRequestTypeDef",
    {
        "InstanceId": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Filters": FiltersTypeDef,
        "HistoricalMetrics": Sequence[HistoricalMetricTypeDef],
    },
)
_OptionalGetMetricDataRequestRequestTypeDef = TypedDict(
    "_OptionalGetMetricDataRequestRequestTypeDef",
    {
        "Groupings": Sequence[GroupingType],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class GetMetricDataRequestRequestTypeDef(
    _RequiredGetMetricDataRequestRequestTypeDef, _OptionalGetMetricDataRequestRequestTypeDef
):
    pass

HistoricalMetricDataTypeDef = TypedDict(
    "HistoricalMetricDataTypeDef",
    {
        "Metric": HistoricalMetricTypeDef,
        "Value": float,
    },
    total=False,
)

_RequiredCreateHoursOfOperationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateHoursOfOperationRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Name": str,
        "TimeZone": str,
        "Config": Sequence[HoursOfOperationConfigTypeDef],
    },
)
_OptionalCreateHoursOfOperationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateHoursOfOperationRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateHoursOfOperationRequestRequestTypeDef(
    _RequiredCreateHoursOfOperationRequestRequestTypeDef,
    _OptionalCreateHoursOfOperationRequestRequestTypeDef,
):
    pass

HoursOfOperationTypeDef = TypedDict(
    "HoursOfOperationTypeDef",
    {
        "HoursOfOperationId": str,
        "HoursOfOperationArn": str,
        "Name": str,
        "Description": str,
        "TimeZone": str,
        "Config": List[HoursOfOperationConfigTypeDef],
        "Tags": Dict[str, str],
    },
    total=False,
)

_RequiredUpdateHoursOfOperationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateHoursOfOperationRequestRequestTypeDef",
    {
        "InstanceId": str,
        "HoursOfOperationId": str,
    },
)
_OptionalUpdateHoursOfOperationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateHoursOfOperationRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "TimeZone": str,
        "Config": Sequence[HoursOfOperationConfigTypeDef],
    },
    total=False,
)

class UpdateHoursOfOperationRequestRequestTypeDef(
    _RequiredUpdateHoursOfOperationRequestRequestTypeDef,
    _OptionalUpdateHoursOfOperationRequestRequestTypeDef,
):
    pass

DescribeInstanceResponseTypeDef = TypedDict(
    "DescribeInstanceResponseTypeDef",
    {
        "Instance": InstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TaskTemplateConstraintsTypeDef = TypedDict(
    "TaskTemplateConstraintsTypeDef",
    {
        "RequiredFields": Sequence[RequiredFieldInfoTypeDef],
        "ReadOnlyFields": Sequence[ReadOnlyFieldInfoTypeDef],
        "InvisibleFields": Sequence[InvisibleFieldInfoTypeDef],
    },
    total=False,
)

TaskTemplateDefaultsTypeDef = TypedDict(
    "TaskTemplateDefaultsTypeDef",
    {
        "DefaultFieldValues": Sequence[TaskTemplateDefaultFieldValueTypeDef],
    },
    total=False,
)

_RequiredGetMetricDataV2RequestRequestTypeDef = TypedDict(
    "_RequiredGetMetricDataV2RequestRequestTypeDef",
    {
        "ResourceArn": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Filters": Sequence[FilterV2TypeDef],
        "Metrics": Sequence[MetricV2TypeDef],
    },
)
_OptionalGetMetricDataV2RequestRequestTypeDef = TypedDict(
    "_OptionalGetMetricDataV2RequestRequestTypeDef",
    {
        "Groupings": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class GetMetricDataV2RequestRequestTypeDef(
    _RequiredGetMetricDataV2RequestRequestTypeDef, _OptionalGetMetricDataV2RequestRequestTypeDef
):
    pass

MetricDataV2TypeDef = TypedDict(
    "MetricDataV2TypeDef",
    {
        "Metric": MetricV2TypeDef,
        "Value": float,
    },
    total=False,
)

ChatParticipantRoleConfigTypeDef = TypedDict(
    "ChatParticipantRoleConfigTypeDef",
    {
        "ParticipantTimerConfigList": Sequence[ParticipantTimerConfigurationTypeDef],
    },
)

_RequiredCreateQuickConnectRequestRequestTypeDef = TypedDict(
    "_RequiredCreateQuickConnectRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Name": str,
        "QuickConnectConfig": QuickConnectConfigTypeDef,
    },
)
_OptionalCreateQuickConnectRequestRequestTypeDef = TypedDict(
    "_OptionalCreateQuickConnectRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateQuickConnectRequestRequestTypeDef(
    _RequiredCreateQuickConnectRequestRequestTypeDef,
    _OptionalCreateQuickConnectRequestRequestTypeDef,
):
    pass

QuickConnectTypeDef = TypedDict(
    "QuickConnectTypeDef",
    {
        "QuickConnectARN": str,
        "QuickConnectId": str,
        "Name": str,
        "Description": str,
        "QuickConnectConfig": QuickConnectConfigTypeDef,
        "Tags": Dict[str, str],
    },
    total=False,
)

UpdateQuickConnectConfigRequestRequestTypeDef = TypedDict(
    "UpdateQuickConnectConfigRequestRequestTypeDef",
    {
        "InstanceId": str,
        "QuickConnectId": str,
        "QuickConnectConfig": QuickConnectConfigTypeDef,
    },
)

ListContactReferencesResponseTypeDef = TypedDict(
    "ListContactReferencesResponseTypeDef",
    {
        "ReferenceSummaryList": List[ReferenceSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRuleActionTypeDef = TypedDict(
    "_RequiredRuleActionTypeDef",
    {
        "ActionType": ActionTypeType,
    },
)
_OptionalRuleActionTypeDef = TypedDict(
    "_OptionalRuleActionTypeDef",
    {
        "TaskAction": TaskActionDefinitionTypeDef,
        "EventBridgeAction": EventBridgeActionDefinitionTypeDef,
        "AssignContactCategoryAction": Mapping[str, Any],
        "SendNotificationAction": SendNotificationActionDefinitionTypeDef,
    },
    total=False,
)

class RuleActionTypeDef(_RequiredRuleActionTypeDef, _OptionalRuleActionTypeDef):
    pass

SearchUsersResponseTypeDef = TypedDict(
    "SearchUsersResponseTypeDef",
    {
        "Users": List[UserSearchSummaryTypeDef],
        "NextToken": str,
        "ApproximateTotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSearchQueuesRequestRequestTypeDef = TypedDict(
    "_RequiredSearchQueuesRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalSearchQueuesRequestRequestTypeDef = TypedDict(
    "_OptionalSearchQueuesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "SearchFilter": QueueSearchFilterTypeDef,
        "SearchCriteria": "QueueSearchCriteriaTypeDef",
    },
    total=False,
)

class SearchQueuesRequestRequestTypeDef(
    _RequiredSearchQueuesRequestRequestTypeDef, _OptionalSearchQueuesRequestRequestTypeDef
):
    pass

_RequiredSearchQueuesRequestSearchQueuesPaginateTypeDef = TypedDict(
    "_RequiredSearchQueuesRequestSearchQueuesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalSearchQueuesRequestSearchQueuesPaginateTypeDef = TypedDict(
    "_OptionalSearchQueuesRequestSearchQueuesPaginateTypeDef",
    {
        "SearchFilter": QueueSearchFilterTypeDef,
        "SearchCriteria": "QueueSearchCriteriaTypeDef",
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class SearchQueuesRequestSearchQueuesPaginateTypeDef(
    _RequiredSearchQueuesRequestSearchQueuesPaginateTypeDef,
    _OptionalSearchQueuesRequestSearchQueuesPaginateTypeDef,
):
    pass

_RequiredSearchRoutingProfilesRequestRequestTypeDef = TypedDict(
    "_RequiredSearchRoutingProfilesRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalSearchRoutingProfilesRequestRequestTypeDef = TypedDict(
    "_OptionalSearchRoutingProfilesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "SearchFilter": RoutingProfileSearchFilterTypeDef,
        "SearchCriteria": "RoutingProfileSearchCriteriaTypeDef",
    },
    total=False,
)

class SearchRoutingProfilesRequestRequestTypeDef(
    _RequiredSearchRoutingProfilesRequestRequestTypeDef,
    _OptionalSearchRoutingProfilesRequestRequestTypeDef,
):
    pass

_RequiredSearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef = TypedDict(
    "_RequiredSearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalSearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef = TypedDict(
    "_OptionalSearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef",
    {
        "SearchFilter": RoutingProfileSearchFilterTypeDef,
        "SearchCriteria": "RoutingProfileSearchCriteriaTypeDef",
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class SearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef(
    _RequiredSearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef,
    _OptionalSearchRoutingProfilesRequestSearchRoutingProfilesPaginateTypeDef,
):
    pass

_RequiredSearchSecurityProfilesRequestRequestTypeDef = TypedDict(
    "_RequiredSearchSecurityProfilesRequestRequestTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalSearchSecurityProfilesRequestRequestTypeDef = TypedDict(
    "_OptionalSearchSecurityProfilesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "SearchCriteria": "SecurityProfileSearchCriteriaTypeDef",
        "SearchFilter": SecurityProfilesSearchFilterTypeDef,
    },
    total=False,
)

class SearchSecurityProfilesRequestRequestTypeDef(
    _RequiredSearchSecurityProfilesRequestRequestTypeDef,
    _OptionalSearchSecurityProfilesRequestRequestTypeDef,
):
    pass

_RequiredSearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef = TypedDict(
    "_RequiredSearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef",
    {
        "InstanceId": str,
    },
)
_OptionalSearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef = TypedDict(
    "_OptionalSearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef",
    {
        "SearchCriteria": "SecurityProfileSearchCriteriaTypeDef",
        "SearchFilter": SecurityProfilesSearchFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class SearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef(
    _RequiredSearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef,
    _OptionalSearchSecurityProfilesRequestSearchSecurityProfilesPaginateTypeDef,
):
    pass

SearchUsersRequestRequestTypeDef = TypedDict(
    "SearchUsersRequestRequestTypeDef",
    {
        "InstanceId": str,
        "NextToken": str,
        "MaxResults": int,
        "SearchFilter": UserSearchFilterTypeDef,
        "SearchCriteria": "UserSearchCriteriaTypeDef",
    },
    total=False,
)

SearchUsersRequestSearchUsersPaginateTypeDef = TypedDict(
    "SearchUsersRequestSearchUsersPaginateTypeDef",
    {
        "InstanceId": str,
        "SearchFilter": UserSearchFilterTypeDef,
        "SearchCriteria": "UserSearchCriteriaTypeDef",
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeRoutingProfileResponseTypeDef = TypedDict(
    "DescribeRoutingProfileResponseTypeDef",
    {
        "RoutingProfile": RoutingProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchRoutingProfilesResponseTypeDef = TypedDict(
    "SearchRoutingProfilesResponseTypeDef",
    {
        "RoutingProfiles": List[RoutingProfileTypeDef],
        "NextToken": str,
        "ApproximateTotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCurrentMetricDataResponseTypeDef = TypedDict(
    "GetCurrentMetricDataResponseTypeDef",
    {
        "NextToken": str,
        "MetricResults": List[CurrentMetricResultTypeDef],
        "DataSnapshotTime": datetime,
        "ApproximateTotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateInstanceStorageConfigRequestRequestTypeDef = TypedDict(
    "AssociateInstanceStorageConfigRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ResourceType": InstanceStorageResourceTypeType,
        "StorageConfig": InstanceStorageConfigTypeDef,
    },
)

DescribeInstanceStorageConfigResponseTypeDef = TypedDict(
    "DescribeInstanceStorageConfigResponseTypeDef",
    {
        "StorageConfig": InstanceStorageConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInstanceStorageConfigsResponseTypeDef = TypedDict(
    "ListInstanceStorageConfigsResponseTypeDef",
    {
        "StorageConfigs": List[InstanceStorageConfigTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateInstanceStorageConfigRequestRequestTypeDef = TypedDict(
    "UpdateInstanceStorageConfigRequestRequestTypeDef",
    {
        "InstanceId": str,
        "AssociationId": str,
        "ResourceType": InstanceStorageResourceTypeType,
        "StorageConfig": InstanceStorageConfigTypeDef,
    },
)

GetCurrentUserDataResponseTypeDef = TypedDict(
    "GetCurrentUserDataResponseTypeDef",
    {
        "NextToken": str,
        "UserDataList": List[UserDataTypeDef],
        "ApproximateTotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUserHierarchyGroupResponseTypeDef = TypedDict(
    "DescribeUserHierarchyGroupResponseTypeDef",
    {
        "HierarchyGroup": HierarchyGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

HistoricalMetricResultTypeDef = TypedDict(
    "HistoricalMetricResultTypeDef",
    {
        "Dimensions": DimensionsTypeDef,
        "Collections": List[HistoricalMetricDataTypeDef],
    },
    total=False,
)

DescribeHoursOfOperationResponseTypeDef = TypedDict(
    "DescribeHoursOfOperationResponseTypeDef",
    {
        "HoursOfOperation": HoursOfOperationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateTaskTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTaskTemplateRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Name": str,
        "Fields": Sequence[TaskTemplateFieldTypeDef],
    },
)
_OptionalCreateTaskTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTaskTemplateRequestRequestTypeDef",
    {
        "Description": str,
        "ContactFlowId": str,
        "Constraints": TaskTemplateConstraintsTypeDef,
        "Defaults": TaskTemplateDefaultsTypeDef,
        "Status": TaskTemplateStatusType,
        "ClientToken": str,
    },
    total=False,
)

class CreateTaskTemplateRequestRequestTypeDef(
    _RequiredCreateTaskTemplateRequestRequestTypeDef,
    _OptionalCreateTaskTemplateRequestRequestTypeDef,
):
    pass

GetTaskTemplateResponseTypeDef = TypedDict(
    "GetTaskTemplateResponseTypeDef",
    {
        "InstanceId": str,
        "Id": str,
        "Arn": str,
        "Name": str,
        "Description": str,
        "ContactFlowId": str,
        "Constraints": TaskTemplateConstraintsTypeDef,
        "Defaults": TaskTemplateDefaultsTypeDef,
        "Fields": List[TaskTemplateFieldTypeDef],
        "Status": TaskTemplateStatusType,
        "LastModifiedTime": datetime,
        "CreatedTime": datetime,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateTaskTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTaskTemplateRequestRequestTypeDef",
    {
        "TaskTemplateId": str,
        "InstanceId": str,
    },
)
_OptionalUpdateTaskTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTaskTemplateRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "ContactFlowId": str,
        "Constraints": TaskTemplateConstraintsTypeDef,
        "Defaults": TaskTemplateDefaultsTypeDef,
        "Status": TaskTemplateStatusType,
        "Fields": Sequence[TaskTemplateFieldTypeDef],
    },
    total=False,
)

class UpdateTaskTemplateRequestRequestTypeDef(
    _RequiredUpdateTaskTemplateRequestRequestTypeDef,
    _OptionalUpdateTaskTemplateRequestRequestTypeDef,
):
    pass

UpdateTaskTemplateResponseTypeDef = TypedDict(
    "UpdateTaskTemplateResponseTypeDef",
    {
        "InstanceId": str,
        "Id": str,
        "Arn": str,
        "Name": str,
        "Description": str,
        "ContactFlowId": str,
        "Constraints": TaskTemplateConstraintsTypeDef,
        "Defaults": TaskTemplateDefaultsTypeDef,
        "Fields": List[TaskTemplateFieldTypeDef],
        "Status": TaskTemplateStatusType,
        "LastModifiedTime": datetime,
        "CreatedTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MetricResultV2TypeDef = TypedDict(
    "MetricResultV2TypeDef",
    {
        "Dimensions": Dict[str, str],
        "Collections": List[MetricDataV2TypeDef],
    },
    total=False,
)

UpdateParticipantRoleConfigChannelInfoTypeDef = TypedDict(
    "UpdateParticipantRoleConfigChannelInfoTypeDef",
    {
        "Chat": ChatParticipantRoleConfigTypeDef,
    },
    total=False,
)

DescribeQuickConnectResponseTypeDef = TypedDict(
    "DescribeQuickConnectResponseTypeDef",
    {
        "QuickConnect": QuickConnectTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRuleRequestRequestTypeDef",
    {
        "InstanceId": str,
        "Name": str,
        "TriggerEventSource": RuleTriggerEventSourceTypeDef,
        "Function": str,
        "Actions": Sequence[RuleActionTypeDef],
        "PublishStatus": RulePublishStatusType,
    },
)
_OptionalCreateRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRuleRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)

class CreateRuleRequestRequestTypeDef(
    _RequiredCreateRuleRequestRequestTypeDef, _OptionalCreateRuleRequestRequestTypeDef
):
    pass

_RequiredRuleTypeDef = TypedDict(
    "_RequiredRuleTypeDef",
    {
        "Name": str,
        "RuleId": str,
        "RuleArn": str,
        "TriggerEventSource": RuleTriggerEventSourceTypeDef,
        "Function": str,
        "Actions": List[RuleActionTypeDef],
        "PublishStatus": RulePublishStatusType,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "LastUpdatedBy": str,
    },
)
_OptionalRuleTypeDef = TypedDict(
    "_OptionalRuleTypeDef",
    {
        "Tags": Dict[str, str],
    },
    total=False,
)

class RuleTypeDef(_RequiredRuleTypeDef, _OptionalRuleTypeDef):
    pass

UpdateRuleRequestRequestTypeDef = TypedDict(
    "UpdateRuleRequestRequestTypeDef",
    {
        "RuleId": str,
        "InstanceId": str,
        "Name": str,
        "Function": str,
        "Actions": Sequence[RuleActionTypeDef],
        "PublishStatus": RulePublishStatusType,
    },
)

GetMetricDataResponseTypeDef = TypedDict(
    "GetMetricDataResponseTypeDef",
    {
        "NextToken": str,
        "MetricResults": List[HistoricalMetricResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMetricDataV2ResponseTypeDef = TypedDict(
    "GetMetricDataV2ResponseTypeDef",
    {
        "NextToken": str,
        "MetricResults": List[MetricResultV2TypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateParticipantRoleConfigRequestRequestTypeDef = TypedDict(
    "UpdateParticipantRoleConfigRequestRequestTypeDef",
    {
        "InstanceId": str,
        "ContactId": str,
        "ChannelConfiguration": UpdateParticipantRoleConfigChannelInfoTypeDef,
    },
)

DescribeRuleResponseTypeDef = TypedDict(
    "DescribeRuleResponseTypeDef",
    {
        "Rule": RuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
