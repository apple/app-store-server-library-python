# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import calendar
import datetime
import re
from urllib.parse import quote
import warnings
from enum import IntEnum, Enum
from typing import Any, Dict, List, MutableMapping, Optional, Type, TypeVar, Union
from attr import define
import requests

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from appstoreserverlibrary.models.LibraryUtility import _get_cattrs_converter
from .models.AdvancedCommerceRequestRefundRequest import AdvancedCommerceRequestRefundRequest
from .models.AdvancedCommerceRequestRefundResponse import AdvancedCommerceRequestRefundResponse
from .models.AdvancedCommerceSubscriptionCancelRequest import AdvancedCommerceSubscriptionCancelRequest
from .models.AdvancedCommerceSubscriptionCancelResponse import AdvancedCommerceSubscriptionCancelResponse
from .models.AdvancedCommerceSubscriptionChangeMetadataRequest import AdvancedCommerceSubscriptionChangeMetadataRequest
from .models.AdvancedCommerceSubscriptionChangeMetadataResponse import AdvancedCommerceSubscriptionChangeMetadataResponse
from .models.AdvancedCommerceSubscriptionMigrateRequest import AdvancedCommerceSubscriptionMigrateRequest
from .models.AdvancedCommerceSubscriptionMigrateResponse import AdvancedCommerceSubscriptionMigrateResponse
from .models.AdvancedCommerceSubscriptionPriceChangeRequest import AdvancedCommerceSubscriptionPriceChangeRequest
from .models.AdvancedCommerceSubscriptionPriceChangeResponse import AdvancedCommerceSubscriptionPriceChangeResponse
from .models.AdvancedCommerceSubscriptionRevokeRequest import AdvancedCommerceSubscriptionRevokeRequest
from .models.AdvancedCommerceSubscriptionRevokeResponse import AdvancedCommerceSubscriptionRevokeResponse
from .models.CheckTestNotificationResponse import CheckTestNotificationResponse
from .models.ConsumptionRequest import ConsumptionRequest
from .models.ConsumptionRequestV1 import ConsumptionRequestV1
from .models.DefaultConfigurationRequest import DefaultConfigurationRequest
from .models.DefaultConfigurationResponse import DefaultConfigurationResponse
from .models.Environment import Environment
from .models.ExtendRenewalDateRequest import ExtendRenewalDateRequest
from .models.ExtendRenewalDateResponse import ExtendRenewalDateResponse
from .models.GetCustomerGroupsResponse import GetCustomerGroupsResponse
from .models.GetGroupMembersResponse import GetGroupMembersResponse
from .models.GetImageListResponse import GetImageListResponse
from .models.GetMessageListResponse import GetMessageListResponse
from .models.HistoryResponse import HistoryResponse
from .models.ImageSize import ImageSize
from .models.MassExtendRenewalDateRequest import MassExtendRenewalDateRequest
from .models.MassExtendRenewalDateResponse import MassExtendRenewalDateResponse
from .models.MassExtendRenewalDateStatusResponse import MassExtendRenewalDateStatusResponse
from .models.NotificationHistoryRequest import NotificationHistoryRequest
from .models.NotificationHistoryResponse import NotificationHistoryResponse
from .models.OrderLookupResponse import OrderLookupResponse
from .models.PerformanceTestRequest import PerformanceTestRequest
from .models.PerformanceTestResponse import PerformanceTestResponse
from .models.PerformanceTestResultResponse import PerformanceTestResultResponse
from .models.RealtimeUrlRequest import RealtimeUrlRequest
from .models.RealtimeUrlResponse import RealtimeUrlResponse
from .models.RefundHistoryResponse import RefundHistoryResponse
from .models.SendTestNotificationResponse import SendTestNotificationResponse
from .models.Status import Status
from .models.StatusResponse import StatusResponse
from .models.TransactionHistoryRequest import TransactionHistoryRequest
from .models.TransactionInfoResponse import TransactionInfoResponse
from .models.AppTransactionInfoResponse import AppTransactionInfoResponse
from .models.UpdateAppAccountTokenRequest import UpdateAppAccountTokenRequest
from .models.UploadMessageRequestBody import UploadMessageRequestBody
from uuid import UUID

T = TypeVar('T')

class APIError(IntEnum):
    """
    Understand the error codes that App Store Server API responses return.

    https://developer.apple.com/documentation/appstoreserverapi/error-codes
    """
    GENERAL_BAD_REQUEST = 4000000
    """
    An error that indicates an invalid request.

    https://developer.apple.com/documentation/appstoreserverapi/generalbadrequesterror
    """

    INVALID_APP_IDENTIFIER = 4000002
    """
    An error that indicates an invalid app identifier.

    https://developer.apple.com/documentation/appstoreserverapi/invalidappidentifiererror
    """

    INVALID_LIMIT = 4000004
    """
    An error that indicates the request limit is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidlimiterror
    """

    INVALID_REQUEST_REVISION = 4000005
    """
    An error that indicates an invalid request revision.

    https://developer.apple.com/documentation/appstoreserverapi/invalidrequestrevisionerror
    """

    INVALID_TRANSACTION_ID = 4000006
    """
    An error that indicates an invalid transaction identifier.

    https://developer.apple.com/documentation/appstoreserverapi/invalidtransactioniderror
    """

    INVALID_ORIGINAL_TRANSACTION_ID = 4000008
    """
    An error that indicates an invalid original transaction identifier.

    https://developer.apple.com/documentation/appstoreserverapi/invalidoriginaltransactioniderror
    """

    INVALID_EXTEND_BY_DAYS = 4000009
    """
    An error that indicates an invalid extend-by-days value.

    https://developer.apple.com/documentation/appstoreserverapi/invalidextendbydayserror
    """

    INVALID_EXTEND_REASON_CODE = 4000010
    """
    An error that indicates an invalid reason code.

    https://developer.apple.com/documentation/appstoreserverapi/invalidextendreasoncodeerror
    """

    INVALID_REQUEST_IDENTIFIER = 4000011
    """
    An error that indicates an invalid request identifier.

    https://developer.apple.com/documentation/appstoreserverapi/invalidrequestidentifiererror
    """

    START_DATE_TOO_FAR_IN_PAST = 4000012
    """
    An error that indicates the start date is earlier than the earliest allowed date.

    https://developer.apple.com/documentation/appstoreserverapi/startdatetoofarinpasterror
    """

    START_DATE_AFTER_END_DATE = 4000013
    """
    An error that indicates the end date precedes the start date, or the two dates are equal.

    https://developer.apple.com/documentation/appstoreserverapi/startdateafterenddateerror
    """

    INVALID_PAGINATION_TOKEN = 4000014
    """
    An error that indicates the pagination token is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidpaginationtokenerror
    """

    INVALID_START_DATE = 4000015
    """
    An error that indicates the start date is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidstartdateerror
    """

    INVALID_END_DATE = 4000016
    """
    An error that indicates the end date is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidenddateerror
    """

    PAGINATION_TOKEN_EXPIRED = 4000017
    """
    An error that indicates the pagination token expired.

    https://developer.apple.com/documentation/appstoreserverapi/paginationtokenexpirederror
    """

    INVALID_NOTIFICATION_TYPE = 4000018
    """
    An error that indicates the notification type or subtype is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidnotificationtypeerror
    """

    MULTIPLE_FILTERS_SUPPLIED = 4000019
    """
    An error that indicates the request is invalid because it has too many applied constraints.

    https://developer.apple.com/documentation/appstoreserverapi/multiplefilterssuppliederror
    """

    INVALID_TEST_NOTIFICATION_TOKEN = 4000020
    """
    An error that indicates the test notification token is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidtestnotificationtokenerror
    """

    INVALID_SORT = 4000021
    """
    An error that indicates the sort parameter is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidsorterror
    """

    INVALID_PRODUCT_TYPE = 4000022
    """
    An error that indicates the product type parameter is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidproducttypeerror
    """

    INVALID_PRODUCT_ID = 4000023
    """
    An error that indicates the product ID parameter is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidproductiderror
    """

    INVALID_SUBSCRIPTION_GROUP_IDENTIFIER = 4000024
    """
    An error that indicates the subscription group identifier is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidsubscriptiongroupidentifiererror
    """

    INVALID_EXCLUDE_REVOKED = 4000025
    """
    An error that indicates the query parameter exclude-revoked is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidexcluderevokederror

    .. deprecated:: 1.0.0
        Use :attr:`INVALID_REVOKED` instead.
    """

    INVALID_IN_APP_OWNERSHIP_TYPE = 4000026
    """
    An error that indicates an invalid in-app ownership type parameter.

    https://developer.apple.com/documentation/appstoreserverapi/invalidinappownershiptypeerror
    """

    INVALID_EMPTY_STOREFRONT_COUNTRY_CODE_LIST = 4000027
    """
    An error that indicates a required storefront country code is empty.

    https://developer.apple.com/documentation/appstoreserverapi/invalidemptystorefrontcountrycodelisterror
    """

    INVALID_STOREFRONT_COUNTRY_CODE = 4000028
    """
    An error that indicates a storefront code is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidstorefrontcountrycodeerror
    """

    INVALID_REVOKED = 4000030
    """
    An error that indicates the revoked parameter contains an invalid value.

    https://developer.apple.com/documentation/appstoreserverapi/invalidrevokederror
    """

    INVALID_STATUS = 4000031
    """
    An error that indicates the status parameter is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidstatuserror
    """

    INVALID_ACCOUNT_TENURE = 4000032
    """
    An error that indicates the value of the account tenure field is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidaccounttenureerror
    """

    INVALID_APP_ACCOUNT_TOKEN = 4000033
    """
    An error that indicates the value of the app account token field is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidappaccounttokenerror
    """

    INVALID_CONSUMPTION_STATUS = 4000034
    """
    An error that indicates the value of the consumption status field is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidconsumptionstatuserror
    """

    INVALID_CUSTOMER_CONSENTED = 4000035
    """
    An error that indicates the customer consented field is invalid or doesn’t indicate that the customer consented.

    https://developer.apple.com/documentation/appstoreserverapi/invalidcustomerconsentederror
    """

    INVALID_DELIVERY_STATUS = 4000036
    """
    An error that indicates the value in the delivery status field is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invaliddeliverystatuserror
    """

    INVALID_LIFETIME_DOLLARS_PURCHASED = 4000037
    """
    An error that indicates the value in the lifetime dollars purchased field is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidlifetimedollarspurchasederror
    """

    INVALID_LIFETIME_DOLLARS_REFUNDED = 4000038
    """
    An error that indicates the value in the lifetime dollars refunded field is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidlifetimedollarsrefundederror
    """

    INVALID_PLATFORM = 4000039
    """
    An error that indicates the value in the platform field is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidplatformerror
    """

    INVALID_PLAY_TIME = 4000040
    """
    An error that indicates the value in the playtime field is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidplaytimeerror
    """

    INVALID_SAMPLE_CONTENT_PROVIDED = 4000041
    """
    An error that indicates the value in the sample content provided field is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidsamplecontentprovidederror
    """

    INVALID_USER_STATUS = 4000042
    """
    An error that indicates the value in the user status field is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invaliduserstatuserror
    """

    INVALID_TRANSACTION_NOT_CONSUMABLE = 4000043
    """
    An error that indicates the transaction identifier doesn’t represent a consumable In-App Purchase.

    https://developer.apple.com/documentation/appstoreserverapi/invalidtransactionnotconsumableerror

    .. deprecated:: 1.2.0
        Use :attr:`INVALID_TRANSACTION_TYPE_NOT_SUPPORTED` instead.
    """

    INVALID_REFUND_PREFERENCE = 4000044
    """
    An error that indicates an invalid refund preference value.

    https://developer.apple.com/documentation/appstoreserverapi/invalidrefundpreferenceerror
    """

    INVALID_TRANSACTION_TYPE_NOT_SUPPORTED = 4000047
    """
    An error that indicates the transaction identifier represents an unsupported In-App Purchase type.

    https://developer.apple.com/documentation/appstoreserverapi/invalidtransactiontypenotsupportederror
    """

    APP_TRANSACTION_ID_NOT_SUPPORTED = 4000048
    """
    An error that indicates the endpoint doesn’t support an app transaction ID.

    https://developer.apple.com/documentation/appstoreserverapi/apptransactionidnotsupportederror
    """

    INVALID_CURRENCY = 4000053
    """
    The currency value is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidcurrencyerror
    """

    ONE_ITEM_NEEDED_IN_MODIFY = 4000063
    """
    At least one type of change must be provided in a modify subscription request.

    https://developer.apple.com/documentation/advancedcommerceapi/oneitemneededinmodifyerror
    """

    NULL_REQUEST_INFO = 4000079
    """
    The required field, requestInfo, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullrequestinfoerror
    """

    NULL_REQUEST_REFERENCE_ID = 4000080
    """
    The required field, requestReferenceId, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullrequestreferenceiderror
    """

    INVALID_REQUEST_REFERENCE_ID = 4000081
    """
    The requestReferenceId value is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidrequestreferenceiderror
    """

    INVALID_CONSISTENCY_TOKEN = 4000082
    """
    The consistencyToken value is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidconsistencytokenerror
    """

    NULL_VERSION = 4000083
    """
    The required field, version, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullversionerror
    """

    UNEXPECTED_VERSION = 4000084
    """
    The value of version is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/unexpectedversionerror
    """

    NULL_TRANSACTION_ID = 4000085
    """
    The required field, transactionId, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nulltransactioniderror
    """

    NEGATIVE_PRICE = 4000086
    """
    The price field must contain a positive number.

    https://developer.apple.com/documentation/advancedcommerceapi/negativepriceerror
    """

    SKU_LENGTH_EXCEEDED = 4000087
    """
    Exceeds the maximum length of the SKU field.

    https://developer.apple.com/documentation/advancedcommerceapi/skulengthexceedederror
    """

    DESCRIPTION_LENGTH_EXCEEDED = 4000088
    """
    Exceeds the maximum length of the description field.

    https://developer.apple.com/documentation/advancedcommerceapi/descriptionlengthexceedederror
    """

    DISPLAY_NAME_LENGTH_EXCEEDED = 4000089
    """
    Exceeds the maximum length of the displayName field.

    https://developer.apple.com/documentation/advancedcommerceapi/displaynamelengthexceedederror
    """

    NEGATIVE_PRORATED_PRICE = 4000091
    """
    The proratedPrice field must contain a positive number.

    https://developer.apple.com/documentation/advancedcommerceapi/negativeproratedpriceerror
    """

    NULL_OFFER_PERIOD = 4000092
    """
    The required field, offer period, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullofferperioderror
    """

    NULL_PERIOD_COUNT = 4000093
    """
    The required field, periodCount, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullperiodcounterror
    """

    PERIOD_COUNT_NOT_POSITIVE = 4000094
    """
    Period count must be a positive number.

    https://developer.apple.com/documentation/advancedcommerceapi/periodcountnotpositiveerror
    """

    NULL_REASON = 4000095
    """
    The required field, reason, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullreasonerror
    """

    INVALID_PREVIOUS_TRANSACTION_ID = 4000096
    """
    Previous original transaction id is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidprevioustransactioniderror
    """

    REPEATED_REQUEST_REFERENCE_ID = 4000097
    """
    The requestReferenceId was repeated.

    https://developer.apple.com/documentation/advancedcommerceapi/repeatedrequestreferenceiderror
    """

    NULL_CURRENCY = 4000098
    """
    The required field, currency, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullcurrencyerror
    """

    NULL_TAX_CODE = 4000099
    """
    The required field, taxCode, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nulltaxcodeerror
    """

    NULL_STOREFRONT = 4000100
    """
    The required field, storefront, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullstorefronterror
    """

    NULL_ITEMS = 4000101
    """
    The required field, items, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullitemserror
    """

    NULL_ITEM = 4000102
    """
    The required field, item, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullitemerror
    """

    NULL_DESCRIPTORS = 4000103
    """
    The required field, descriptors, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nulldescriptorserror
    """

    NULL_PERIOD = 4000104
    """
    The required field, period, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullperioderror
    """

    NULL_SKU = 4000105
    """
    The required field, SKU, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullskuerror
    """

    NULL_DISPLAY_NAME = 4000106
    """
    The required field, displayName, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nulldisplaynameerror
    """

    NULL_DESCRIPTION = 4000107
    """
    The required field, description, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nulldescriptionerror
    """

    NULL_PRICE = 4000109
    """
    The required field, price, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullpriceerror
    """

    NULL_RETAIN_BILLING_CYCLE = 4000110
    """
    The required field, retainBillingCycle, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullretainbillingcycleerror
    """

    NULL_EFFECTIVE = 4000111
    """
    The required field, effective, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nulleffectiveerror
    """

    NULL_NEW_SKU = 4000112
    """
    The required field, SKU in changeItems, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullnewskuerror
    """

    INVALID_PREVIOUS_SUBSCRIPTION = 4000113
    """
    The previous subscription targeted is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidprevioussubscriptionerror
    """

    PRODUCT_ALREADY_EXISTS = 4000114
    """
    Provided SKU is already owned.

    https://developer.apple.com/documentation/advancedcommerceapi/productalreadyexistserror
    """

    INVALID_PRODUCT_CHANGES = 4000115
    """
    Product changes are invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidproductchangeserror
    """

    INVALID_SALABLE = 4000116
    """
    The targeted salable isn't configured as a generic salable.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidsalableerror
    """

    INVALID_SALABLE_DURATION = 4000117
    """
    The salable duration is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidsalabledurationerror
    """

    INVALID_DISPLAY_NAME = 4000118
    """
    The displayName is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invaliddisplaynameerror
    """

    INVALID_DESCRIPTION = 4000119
    """
    The description is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invaliddescriptionerror
    """

    INVALID_PRODUCT = 4000121
    """
    The requested product to change doesn't exist.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidproducterror
    """

    INVALID_SKU = 4000122
    """
    The SKU was invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidskuerror
    """

    INVALID_REFUND_TYPE = 4000123
    """
    The refundType is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidrefundtypeerror
    """

    INVALID_REFUND_REASON = 4000124
    """
    The refundReason is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidrefundreasonerror
    """

    INVALID_CHANGE_REASON = 4000125
    """
    The change reason is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidchangereasonerror
    """

    INVALID_OFFER_REASON = 4000126
    """
    The offer reason is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidofferreasonerror
    """

    INVALID_TAX_PRODUCT_CODE = 4000127
    """
    The taxCode is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidtaxproductcodeerror
    """

    INVALID_OFFER_PERIOD = 4000128
    """
    The offer period is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidofferperioderror
    """

    INVALID_OFFER_PERIOD_COUNT = 4000129
    """
    The offer periodCount is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidofferperiodcounterror
    """

    INVALID_RENEWAL_PERIOD = 4000130
    """
    The renewal period is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidrenewalperioderror
    """

    INVALID_RENEWAL_PRICE = 4000131
    """
    The renewal price is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidrenewalpriceerror
    """

    INVALID_AMOUNT = 4000132
    """
    The amount is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidamounterror
    """

    MISMATCHED_STOREFRONT = 4000133
    """
    The storefronts mismatch.

    https://developer.apple.com/documentation/advancedcommerceapi/mismatchedstorefronterror
    """

    MISSING_PRICING_CONFIG_FOR_STOREFRONT = 4000134
    """
    Pricing isn't configured for the storefront.

    https://developer.apple.com/documentation/advancedcommerceapi/missingpricingconfigforstorefronterror
    """

    OPERATION_NOT_ALLOWED = 4000135
    """
    The operation isn't allowed.

    https://developer.apple.com/documentation/advancedcommerceapi/operationnotallowederror
    """

    MORE_ITEMS_THAN_ALLOWED = 4000136
    """
    More items were provided than allowed.

    https://developer.apple.com/documentation/advancedcommerceapi/moreitemsthanallowederror
    """

    MORE_OFFERS_THAN_ALLOWED = 4000137
    """
    More offers were provided than allowed.

    https://developer.apple.com/documentation/advancedcommerceapi/moreoffersthanallowederror
    """

    EMPTY_ADD_CHANGE_ITEMS = 4000139
    """
    The addItems and changeItems entries cannot be empty.

    https://developer.apple.com/documentation/advancedcommerceapi/emptyaddchangeitemserror
    """

    MISSING_UPDATED_ITEMS_WITH_PERIOD_CHANGE = 4000140
    """
    All items must be updated on a period change.

    https://developer.apple.com/documentation/advancedcommerceapi/missingupdateditemswithperiodchangeerror
    """

    PERIOD_RESET_WITH_RETAIN_BILLING_CYCLE = 4000141
    """
    Period reset conflicts with retaining billing cycle.

    https://developer.apple.com/documentation/advancedcommerceapi/periodresetwithretainbillingcycleerror
    """

    PERIOD_CHANGE_EFFECTIVE_CONFLICT = 4000142
    """
    A period change at next cycle conflicts with addition at the current period.

    https://developer.apple.com/documentation/advancedcommerceapi/periodchangeeffectiveconflicterror
    """

    MULTIPLE_OPERATIONS_ON_SINGLE_SKU = 4000143
    """
    Multiple operations on a single SKU isn't allowed.

    https://developer.apple.com/documentation/advancedcommerceapi/multipleoperationsonsingleskuerror
    """

    REMOVE_ITEMS_WITHOUT_ADD_OR_CHANGE_ITEMS = 4000144
    """
    The removeItems object was present without addItems or changeItems.

    https://developer.apple.com/documentation/advancedcommerceapi/removeitemswithoutaddorchangeitemserror
    """

    REMOVE_ITEM_NOT_FOUND = 4000145
    """
    A product in removeItems wasn't found for the given subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/removeitemnotfounderror
    """

    CHANGE_ITEM_NOT_FOUND = 4000146
    """
    The targeted item in changeItems wasn't found.

    https://developer.apple.com/documentation/advancedcommerceapi/changeitemnotfounderror
    """

    MISALIGNED_BILLING_CYCLE = 4000147
    """
    The request contains a billing period that doesn't align with the subscription's billing cycle.

    https://developer.apple.com/documentation/advancedcommerceapi/misalignedbillingcycleerror
    """

    BILLING_CYCLE_RESET_WITH_EFFECTIVE_LATER = 4000148
    """
    Bill cycle reset with effective later.

    https://developer.apple.com/documentation/advancedcommerceapi/billingcycleresetwitheffectivelatererror
    """

    PERIOD_CHANGE_IMMEDIATE_WITH_EFFECTIVE_AT_NEXT_BILLING_CYCLE = 4000149
    """
    Period change immediately with effective later.

    https://developer.apple.com/documentation/advancedcommerceapi/periodchangeimmediatewitheffectiveatnextbillingcycleerror
    """

    MULTIPLE_PRICES = 4000150
    """
    Prorated price and offer price are mutually exclusive.

    https://developer.apple.com/documentation/advancedcommerceapi/multiplepriceserror
    """

    INVALID_PRORATED_PRICE = 4000151
    """
    The prorated price was invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidproratedpriceerror
    """

    INVALID_OFFER_PRICE = 4000152
    """
    The subscription offer price is higher than the regular subscription price.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidofferpriceerror
    """

    NULL_REFUND_AMOUNT = 4000153
    """
    The refundAmount value is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/nullrefundamounterror
    """

    NEGATIVE_REFUND_AMOUNT = 4000154
    """
    The refundAmount must be a positive number.

    https://developer.apple.com/documentation/advancedcommerceapi/negativerefundamounterror
    """

    REFUND_AMOUNT_WITHOUT_CUSTOM = 4000155
    """
    Can't provide the refund amount because the refundType isn't CUSTOM.

    https://developer.apple.com/documentation/advancedcommerceapi/refundamountwithoutcustomerror
    """

    NULL_REFUND_REASON = 4000156
    """
    The required field, refundReason, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullrefundreasonerror
    """

    NULL_REFUND_TYPE = 4000157
    """
    The required field, refundType, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullrefundtypeerror
    """

    SIMULATE_REFUND_DECLINE_ONLY_IN_SANDBOX = 4000158
    """
    The type SIMULATE_REFUND_DECLINE is only valid in Sandbox.

    https://developer.apple.com/documentation/advancedcommerceapi/simulaterefunddeclineonlyinsandboxerror
    """

    NULL_REFUND_RISKING = 4000159
    """
    The required field, refundRiskingPreference, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullrefundriskingerror
    """

    AT_LEAST_ONE_ITEM = 4000160
    """
    When included, provide at least one item in items.

    https://developer.apple.com/documentation/advancedcommerceapi/atleastoneitemerror
    """

    INVALID_IMAGE = 4000161
    """
    An error that indicates the image that’s uploading is invalid.

    https://developer.apple.com/documentation/retentionmessaging/invalidimageerror
    """

    HEADER_TOO_LONG = 4000162
    """
    An error that indicates the header text is too long.

    https://developer.apple.com/documentation/retentionmessaging/headertoolongerror
    """

    BODY_TOO_LONG = 4000163
    """
    An error that indicates the body text is too long.

    https://developer.apple.com/documentation/retentionmessaging/bodytoolongerror
    """

    INVALID_LOCALE = 4000164
    """
    An error that indicates the locale is invalid.

    https://developer.apple.com/documentation/retentionmessaging/invalidlocaleerror
    """

    AT_LEAST_ONE_OF_DISPLAY_NAME_OR_DESCRIPTION = 4000165
    """
    Provide either the displayName or a description.

    https://developer.apple.com/documentation/advancedcommerceapi/atleastoneofdisplaynameordescriptionerror
    """

    NULL_TARGET_PRODUCT_ID = 4000166
    """
    The required field, targetProductID, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nulltargetproductiderror
    """

    INVALID_TARGET_PRODUCT_ID = 4000167
    """
    The targetProductID value is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidtargetproductiderror
    """

    REMOVAL_ALL_NOT_ALLOWED = 4000168
    """
    The active subscription must contain at least one item and cannot be completely empty.

    https://developer.apple.com/documentation/advancedcommerceapi/removalallnotallowederror
    """

    NULL_CURRENT_SKU = 4000169
    """
    The required field, currentSKU, is missing.

    https://developer.apple.com/documentation/advancedcommerceapi/nullcurrentskuerror
    """

    CURRENT_SKU_LENGTH_EXCEEDED = 4000170
    """
    Exceeds the maximum length of the currentSKU field.

    https://developer.apple.com/documentation/advancedcommerceapi/currentskulengthexceedederror
    """

    NULL_ADVANCED_COMMERCE_DATA = 4000171
    """
    The required field, advancedCommerceData, was null.

    https://developer.apple.com/documentation/advancedcommerceapi/nulladvancedcommercedataerror
    """

    INVALID_OPERATION = 4000172
    """
    The operation is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidoperationerror
    """

    MALFORMED_PAYLOAD = 4000173
    """
    The payload is malformed.

    https://developer.apple.com/documentation/advancedcommerceapi/malformedpayloaderror
    """

    INVALID_SIGNATURE = 4000174
    """
    The signature is invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidsignatureerror
    """

    ALT_TEXT_TOO_LONG = 4000175
    """
    An error that indicates the alternative text for an image is too long.

    https://developer.apple.com/documentation/retentionmessaging/alttexttoolongerror
    """

    SUBSCRIPTION_ALREADY_MIGRATED = 4000176
    """
    The subscription was already migrated.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionalreadymigratederror
    """

    OFFER_PREVENTS_ITEM_MID_CYCLE_CHANGE = 4000177
    """
    An active or pending offer prevents changes to the item mid-cycle.

    https://developer.apple.com/documentation/advancedcommerceapi/offerpreventsitemmidcyclechangeerror
    """

    PRICE_CHANGE_NOT_SUPPORTED_THROUGH_MODIFY_ITEMS = 4000178
    """
    Price change is not allowed through plan modification.

    https://developer.apple.com/documentation/advancedcommerceapi/pricechangenotsupportedthroughmodifyitemserror
    """

    ITEM_LIMIT_EXCEEDED = 4000179
    """
    The number of items in subscription exceeds the limit.

    https://developer.apple.com/documentation/advancedcommerceapi/itemlimitexceedederror
    """

    PENDING_CHANGES_MISMATCH = 4000180
    """
    Pending subscription changes must specify a renewalItem, and if there are no pending changes, a renewalItem cannot be specified.

    https://developer.apple.com/documentation/advancedcommerceapi/pendingchangesmismatcherror
    """

    PENDING_REFUND = 4000181
    """
    The transaction has pending refunds.

    https://developer.apple.com/documentation/advancedcommerceapi/pendingrefunderror
    """

    PRORATED_ONLY_LATEST_TRANSACTION = 4000182
    """
    Only requests against the latest transaction can have a PRORATED refundType value.

    https://developer.apple.com/documentation/advancedcommerceapi/proratedonlylatesttransactionerror
    """

    INVALID_APP_ACCOUNT_TOKEN_UUID = 4000183
    """
    An error that indicates the app account token value is not a valid UUID.

    https://developer.apple.com/documentation/appstoreserverapi/invalidappaccounttokenuuiderror
    """

    PARTIAL_SIMULATE_REFUND_DECLINE = 4000184
    """
    If one item has a refundReason value of SIMULATE_REFUND_DECLINE, all items must have a refundReason value of SIMULATE_REFUND_DECLINE.

    https://developer.apple.com/documentation/advancedcommerceapi/partialsimulaterefunddeclineerror
    """

    FAMILY_TRANSACTION_NOT_SUPPORTED = 4000185
    """
    An error that indicates the transaction is for a product the customer obtains through Family Sharing, which the endpoint doesn’t support.

    https://developer.apple.com/documentation/appstoreserverapi/familytransactionnotsupportederror
    """

    REVOKE_ON_INACTIVE_SUBSCRIPTION = 4000186
    """
    Only active subscriptions are revocable.

    https://developer.apple.com/documentation/advancedcommerceapi/revokeoninactivesubscriptionerror
    """

    TRANSACTION_ID_IS_NOT_ORIGINAL_TRANSACTION_ID = 4000187
    """
    An error that indicates the endpoint expects an original transaction identifier.

    https://developer.apple.com/documentation/appstoreserverapi/transactionidisnotoriginaltransactioniderror
    """

    DEPENDENT_SKUS_CANNOT_BE_SHARED = 4000192
    """
    Invalid request. dependentSKUs can't be shared between multiple SKUs.

    https://developer.apple.com/documentation/advancedcommerceapi/dependentskuscannotbesharederror
    """

    DEPENDENT_SKUS_CANNOT_BE_CHAINED = 4000193
    """
    Invalid request. dependentSKUs can't be chained.

    https://developer.apple.com/documentation/advancedcommerceapi/dependentskuscannotbechainederror
    """

    ITEM_CANNOT_BE_SPECIFIED_MULTIPLE_TIMES = 4000194
    """
    Invalid request. The same SKU can't be repeated in this request.

    https://developer.apple.com/documentation/advancedcommerceapi/itemcannotbespecifiedmultipletimeserror
    """

    PRICE_CHANGE_CANNOT_BE_ISSUED_WHEN_ALREADY_COMMUNICATED = 4000205
    """
    Invalid request. A price change can't be issued when the price increase has already been communicated.

    https://developer.apple.com/documentation/advancedcommerceapi/pricechangecannotbeissuedwhenalreadycommunicatederror
    """

    CONSUMPTION_PERCENTAGE_OUT_OF_RANGE = 4000207
    """
    An error that indicates the consumption percentage is outside the valid range.

    https://developer.apple.com/documentation/appstoreserverapi/consumptionpercentageoutofrangeerror
    """

    UNDELIVERED_CONSUMPTION_PERCENTAGE_NON_ZERO = 4000208
    """
    An error that indicates the consumption percentage must be zero for the provided delivery status.

    https://developer.apple.com/documentation/appstoreserverapi/undeliveredconsumptionpercentagenonzeroerror
    """

    CONSUMPTION_PERCENTAGE_AUTO_RENEWABLE_SUBSCRIPTION = 4000209
    """
    An error that indicates the consumption percentage field is unsupported for auto-renewable subscription transactions.

    https://developer.apple.com/documentation/appstoreserverapi/consumptionpercentageautorenewablesubscriptionerror
    """

    ADVANCED_COMMERCE_TRANSACTION_NOT_SUPPORTED = 4000210
    """
    An error that indicates Advanced Commerce API transactions are not supported by the endpoint.

    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercetransactionnotsupportederror
    """

    INVALID_PERFORMANCE_TEST_REQUEST = 4000211
    """
    An error the API returns that indicates the performance test request is invalid.

    https://developer.apple.com/documentation/retentionmessaging/invalidperformancetestrequesterror
    """

    INVALID_REQUEST_ID = 4000212
    """
    An error that indicates the request ID is invalid.

    https://developer.apple.com/documentation/retentionmessaging/invalidrequestiderror
    """

    EXISTING_PERFORMANCE_TEST_RUN = 4000213
    """
    An error that indicates an error with an existing test.

    https://developer.apple.com/documentation/retentionmessaging/existingperformancetestrunerror
    """

    INVALID_PRICE_FOR_CHANGE_ITEM_IN_PRICE_INCREASE = 4000214
    """
    Invalid request. Price provided for a changed item with an offer while subject to a price increase was invalid.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidpriceforchangeiteminpriceincreaseerror
    """

    BAD_REQUEST_REALTIME_URL = 4000215
    """
    An error that indicates the URL is invalid.

    https://developer.apple.com/documentation/retentionmessaging/badrequestrealtimeurlerror
    """

    BAD_REQUEST_IMAGE_SIZE = 4000216
    """
    An error that indicates the image size provided is invalid.

    https://developer.apple.com/documentation/retentionmessaging/badrequestimagesizeerror
    """

    BAD_REQUEST_TOO_MANY_BULLET_POINTS = 4000218
    """
    An error that indicates there are too many bullet points.

    https://developer.apple.com/documentation/retentionmessaging/badrequesttoomanybulletpointserror
    """

    BAD_REQUEST_BULLET_POINT_TEXT_TOO_LONG = 4000219
    """
    An error that indicates the text for a bullet point is too long.

    https://developer.apple.com/documentation/retentionmessaging/badrequestbulletpointtexttoolongerror
    """

    INVALID_SKU_PROVIDED_MUST_BE_CURRENT_SKU_SET_TO_RENEW = 4000220
    """
    Invalid request. SKU values provided in request must be a SKU that will renew.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidskuprovidedmustbecurrentskusettorenewerror
    """

    ACA_PRICE_INCREASE_IS_NOT_CURRENTLY_SUPPORTED_IN_INDIA = 4000221
    """
    Advanced Commerce API Price Increase mechanism is not currently supported in India.

    https://developer.apple.com/documentation/advancedcommerceapi/acapriceincreaseisnotcurrentlysupportedinindiaerror
    """

    INVALID_PRORATED_PRICE_FOR_CHANGE_ITEM_WITH_EFFECTIVE_LATER = 4000222
    """
    Invalid request. A prorated price shouldn't be present to change items with the change taking effect later.

    https://developer.apple.com/documentation/advancedcommerceapi/invalidproratedpriceforchangeitemwitheffectivelatererror
    """

    FREE_TRIAL_OFFER_MUST_USE_PERIOD_COUNT_OF_ONE = 4000223
    """
    Invalid request. The subscription offer configuration is invalid; free trial offers must use a period count of 1.

    https://developer.apple.com/documentation/advancedcommerceapi/freetrialoffermustuseperiodcountofoneerror
    """

    BAD_REQUEST_ABOVE_IMAGE_REQUIRES_AN_IMAGE = 4000224
    """
    An error that indicates that no image object is included, but the request indicates that the header should be placed above the image.

    https://developer.apple.com/documentation/retentionmessaging/badrequestaboveimagerequiresanimageerror
    """

    INVALID_GROUP_ID = 4000225
    """
    An error that indicates the group identifier is invalid.

    https://developer.apple.com/documentation/appstoreserverapi/invalidgroupiderror
    """

    INVALID_ASSIGNED_TRANSACTION_NOT_SUPPORTED = 4000227
    """
    An error that indicates the transaction is one that an organization or group assigns to the customer, which the endpoint doesn’t support.

    https://developer.apple.com/documentation/appstoreserverapi/invalidassignedtransactionnotsupportederror
    """

    UNAUTHORIZED = 4010000
    """
    Unauthorized.

    https://developer.apple.com/documentation/advancedcommerceapi/unauthorizederror
    """

    SUBSCRIPTION_EXTENSION_INELIGIBLE = 4030004
    """
    An error that indicates the subscription doesn’t qualify for a renewal-date extension due to its subscription state.

    https://developer.apple.com/documentation/appstoreserverapi/subscriptionextensionineligibleerror
    """

    SUBSCRIPTION_MAX_EXTENSION = 4030005
    """
    An error that indicates the subscription doesn’t qualify for a renewal-date extension because it has already received the maximum extensions.

    https://developer.apple.com/documentation/appstoreserverapi/subscriptionmaxextensionerror
    """

    FAMILY_SHARED_SUBSCRIPTION_EXTENSION_INELIGIBLE = 4030007
    """
    An error that indicates a subscription isn’t directly eligible for a renewal date extension because the customer obtained it through Family Sharing.

    https://developer.apple.com/documentation/appstoreserverapi/familysharedsubscriptionextensionineligibleerror
    """

    SUBSCRIPTION_DOES_NOT_EXIST = 4030008
    """
    The subscription doesn't exist.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptiondoesnotexisterror
    """

    SUBSCRIPTION_ALREADY_EXISTS = 4030009
    """
    The subscription already exists.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionalreadyexistserror
    """

    SUBSCRIPTION_NOT_ELIGIBLE = 4030010
    """
    The subscription isn't eligible for the requested changes.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionnoteligibleerror
    """

    SUBSCRIPTION_ALREADY_ACTIVE = 4030011
    """
    The subscription is already active, and cannot be reactivated or renewed at this time.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionalreadyactiveerror
    """

    PRODUCT_NOT_OWNED = 4030013
    """
    The customer doesn't own the product.

    https://developer.apple.com/documentation/advancedcommerceapi/productnotownederror
    """

    MAXIMUM_NUMBER_OF_IMAGES_REACHED = 4030014
    """
    An error that indicates when you reach the maximum number of uploaded images.

    https://developer.apple.com/documentation/retentionmessaging/maximumnumberofimagesreachederror
    """

    INACTIVE_ACA_SUB = 4030015
    """
    The subscription is not active.

    https://developer.apple.com/documentation/advancedcommerceapi/inactiveacasuberror
    """

    MAXIMUM_NUMBER_OF_MESSAGES_REACHED = 4030016
    """
    An error that indicates when you reach the maximum number of uploaded messages.

    https://developer.apple.com/documentation/retentionmessaging/maximumnumberofmessagesreachederror
    """

    MESSAGE_NOT_APPROVED = 4030017
    """
    An error that indicates the message isn’t in the approved state, so you can’t configure it as a default message.

    https://developer.apple.com/documentation/retentionmessaging/messagenotapprovederror
    """

    IMAGE_NOT_APPROVED = 4030018
    """
    An error that indicates the image isn’t in the approved state, so you can’t configure it as part of a default message.

    https://developer.apple.com/documentation/retentionmessaging/imagenotapprovederror
    """

    IMAGE_IN_USE = 4030019
    """
    An error that indicates the image is currently in use as part of a message, so you can’t delete it.

    https://developer.apple.com/documentation/retentionmessaging/imageinuseerror
    """

    INSUFFICIENT_FUNDS = 4030020
    """
    Insufficient funds for refund.

    https://developer.apple.com/documentation/advancedcommerceapi/insufficientfundserror
    """

    ALREADY_REFUNDED = 4030021
    """
    The transaction was already refunded.

    https://developer.apple.com/documentation/advancedcommerceapi/alreadyrefundederror
    """

    STOREFRONT_CHANGE = 4030022
    """
    The storefront changed.

    https://developer.apple.com/documentation/advancedcommerceapi/storefrontchangeerror
    """

    PRODUCT_NOT_ELIGIBLE = 4030023
    """
    The product isn't eligible for the requested operation.

    https://developer.apple.com/documentation/advancedcommerceapi/productnoteligibleerror
    """

    TRANSACTION_NOT_REFUNDABLE = 4030024
    """
    The transaction is not refundable.

    https://developer.apple.com/documentation/advancedcommerceapi/transactionnotrefundableerror
    """

    TRANSACTION_CANNOT_BE_REFUNDED_CONTACT_SUPPORT = 4030025
    """
    The transaction can't be refunded; customer can contact Apple Support for assistance.

    https://developer.apple.com/documentation/advancedcommerceapi/transactioncannotberefundedcontactsupporterror
    """

    FORBIDDEN_NO_PASSING_TEST = 4030026
    """
    An error that indicates that passing a performance test is required before you can set a URL for the production environment.

    https://developer.apple.com/documentation/retentionmessaging/forbiddennopassingtesterror
    """

    MIGRATION_NOT_ALLOWED_WHEN_PRICE_INCREASE_COMMUNICATED = 4030027
    """
    The subscription isn't eligible for migration because a price increase has already been communicated to the customer.

    https://developer.apple.com/documentation/advancedcommerceapi/migrationnotallowedwhenpriceincreasecommunicatederror
    """

    ASSIGNED_SUBSCRIPTION_EXTENSION_INELIGIBLE = 4030028
    """
    An error that indicates a subscription isn’t eligible for a renewal date extension because the customer has access through an organization or group.

    https://developer.apple.com/documentation/appstoreserverapi/assignedsubscriptionextensionineligibleerror
    """

    ACCOUNT_NOT_FOUND = 4040001
    """
    An error that indicates the App Store account wasn’t found.

    https://developer.apple.com/documentation/appstoreserverapi/accountnotfounderror
    """

    ACCOUNT_NOT_FOUND_RETRYABLE = 4040002
    """
    An error response that indicates the App Store account wasn’t found, but you can try again.

    https://developer.apple.com/documentation/appstoreserverapi/accountnotfoundretryableerror
    """

    APP_NOT_FOUND = 4040003
    """
    An error that indicates the app wasn’t found.

    https://developer.apple.com/documentation/appstoreserverapi/appnotfounderror
    """

    APP_NOT_FOUND_RETRYABLE = 4040004
    """
    An error response that indicates the app wasn’t found, but you can try again.

    https://developer.apple.com/documentation/appstoreserverapi/appnotfoundretryableerror
    """

    ORIGINAL_TRANSACTION_ID_NOT_FOUND = 4040005
    """
    An error that indicates an original transaction identifier wasn’t found.

    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionidnotfounderror
    """

    ORIGINAL_TRANSACTION_ID_NOT_FOUND_RETRYABLE = 4040006
    """
    An error response that indicates the original transaction identifier wasn’t found, but you can try again.

    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionidnotfoundretryableerror
    """

    SERVER_NOTIFICATION_URL_NOT_FOUND = 4040007
    """
    An error that indicates the App Store server couldn’t find a notifications URL for your app in the environment.

    https://developer.apple.com/documentation/appstoreserverapi/servernotificationurlnotfounderror
    """

    TEST_NOTIFICATION_NOT_FOUND = 4040008
    """
    An error that indicates the test notification token is expired or the test notification status isn’t available.

    https://developer.apple.com/documentation/appstoreserverapi/testnotificationnotfounderror
    """

    STATUS_REQUEST_NOT_FOUND = 4040009
    """
    An error that indicates the server didn’t find a subscription-renewal-date extension request for the request identifier and product identifier you provided.

    https://developer.apple.com/documentation/appstoreserverapi/statusrequestnotfounderror
    """

    TRANSACTION_ID_NOT_FOUND = 4040010
    """
    An error that indicates a transaction identifier wasn’t found.

    https://developer.apple.com/documentation/appstoreserverapi/transactionidnotfounderror
    """

    IMAGE_NOT_FOUND = 4040014
    """
    An error that indicates the system can’t find the image identifier.

    https://developer.apple.com/documentation/retentionmessaging/imagenotfounderror
    """

    MESSAGE_NOT_FOUND = 4040015
    """
    An error that indicates the system can’t find the message identifier.

    https://developer.apple.com/documentation/retentionmessaging/messagenotfounderror
    """

    PRODUCT_NOT_FOUND = 4040016
    """
    Product not found.

    https://developer.apple.com/documentation/advancedcommerceapi/productnotfounderror
    """

    PERFORMANCE_TEST_RUN_NOT_FOUND = 4040018
    """
    An error the API returns if the service can’t find the specified test run.

    https://developer.apple.com/documentation/retentionmessaging/performancetestrunnotfounderror
    """

    APP_TRANSACTION_DOES_NOT_EXIST = 4040019
    """
    An error response that indicates an app transaction doesn’t exist for the specified customer.

    https://developer.apple.com/documentation/appstoreserverapi/apptransactiondoesnotexisterror
    """

    DEFAULT_MESSAGE_NOT_FOUND = 4040020
    """
    An error that indicates a default message isn’t configured.

    https://developer.apple.com/documentation/retentionmessaging/defaultmessagenotfounderror
    """

    REALTIME_URL_NOT_FOUND = 4040021
    """
    An error that indicates that the URL for your endpoint isn’t configured.

    https://developer.apple.com/documentation/retentionmessaging/realtimeurlnotfounderror
    """

    GROUP_NOT_FOUND = 4040022
    """
    An error that indicates the group wasn’t found.

    https://developer.apple.com/documentation/appstoreserverapi/groupnotfounderror
    """

    IMAGE_ALREADY_EXISTS = 4090000
    """
    An error that indicates the image identifier already exists.

    https://developer.apple.com/documentation/retentionmessaging/imagealreadyexistserror
    """

    MESSAGE_ALREADY_EXISTS = 4090001
    """
    An error that indicates the message identifier already exists.

    https://developer.apple.com/documentation/retentionmessaging/messagealreadyexistserror
    """

    RATE_LIMIT_EXCEEDED = 4290000
    """
    An error that indicates the request exceeded the rate limit.

    https://developer.apple.com/documentation/appstoreserverapi/ratelimitexceedederror
    """

    GENERAL_INTERNAL = 5000000
    """
    An error that indicates a general internal error.

    https://developer.apple.com/documentation/appstoreserverapi/generalinternalerror
    """

    GENERAL_INTERNAL_RETRYABLE = 5000001
    """
    An error response that indicates an unknown error occurred, but you can try again.

    https://developer.apple.com/documentation/appstoreserverapi/generalinternalretryableerror
    """


@define
class APIException(Exception):
    http_status_code: int
    api_error: Optional[APIError]
    raw_api_error: Optional[int]
    error_message: Optional[str]
    headers: Dict[str, List[str]]
    """
    The response headers, keyed by lowercased header name.
    """

    retry_after: Optional[int]
    """
    A UNIX time, in milliseconds, that informs you when you can next send a request.

    https://developer.apple.com/documentation/appstoreserverapi/identifying-rate-limits
    """

    def __init__(self, http_status_code: int, raw_api_error: Optional[int] = None, error_message: Optional[str] = None, headers: Optional[Dict[str, List[str]]] = None):
        self.http_status_code = http_status_code
        self.raw_api_error = raw_api_error
        self.api_error = None
        self.error_message = error_message
        self.headers = headers if headers is not None else {}
        self.retry_after = _parse_retry_after(self.headers.get('retry-after'))
        try:
            if raw_api_error is not None:
                self.api_error = APIError(raw_api_error)
        except ValueError:
            pass


_RETRY_AFTER_PATTERN = re.compile(r'[0-9]+')


def _parse_retry_after(retry_after_values: Optional[List[str]]) -> Optional[int]:
    if not retry_after_values:
        return None
    stripped_retry_after = retry_after_values[0].strip()
    if _RETRY_AFTER_PATTERN.fullmatch(stripped_retry_after) is None:
        return None
    return int(stripped_retry_after)

def _encode_path_segment(path_segment: str) -> str:
    encoded = quote(str(path_segment), safe='')
    if encoded in ('', '.', '..'):
        raise ValueError()
    return encoded

def _path(template: str, *path_parameters: str) -> str:
    parts = template.split('{}')
    if len(parts) != len(path_parameters) + 1:
        raise ValueError()
    return parts[0] + ''.join(_encode_path_segment(path_parameter) + part for path_parameter, part in zip(path_parameters, parts[1:]))

class GetTransactionHistoryVersion(str, Enum):
    V1 = "v1"
    """
    .. deprecated:: 1.3.0
    """

    V2 = "v2"

class BaseAppStoreServerAPIClient:
    def __init__(self, signing_key: bytes, key_id: str, issuer_id: str, bundle_id: str, environment: Environment):
        if environment == Environment.XCODE:
            raise ValueError("Xcode is not a supported environment for an AppStoreServerAPIClient")
        if environment == Environment.PRODUCTION:
            self._base_url = "https://api.storekit.apple.com"
        elif environment == Environment.LOCAL_TESTING:
            self._base_url = "https://local-testing-base-url"
        elif environment == Environment.SANDBOX:
            self._base_url = "https://api.storekit-sandbox.apple.com"
        else:
            raise ValueError("Invalid environment provided")
        self._signing_key = serialization.load_pem_private_key(signing_key, password=None, backend=default_backend())
        self._key_id = key_id
        self._issuer_id = issuer_id
        self._bundle_id = bundle_id

    def _generate_token(self) -> str:
        current_time = datetime.datetime.now(datetime.timezone.utc)
        future_time = current_time + datetime.timedelta(minutes=5)
        return jwt.encode(
            {
                "bid": self._bundle_id,
                "iss": self._issuer_id,
                "aud": "appstoreconnect-v1",
                "iat": calendar.timegm(current_time.timetuple()),
                "exp": calendar.timegm(future_time.timetuple()),
            },
            self._signing_key,
            algorithm="ES256",
            headers={"kid": self._key_id},
        )
    
    def _get_full_url(self, path) -> str:
        return self._base_url + path
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            'User-Agent': "app-store-server-library/python/3.1.2",
            'Authorization': f'Bearer {self._generate_token()}',
            'Accept': 'application/json'
        }
    
    def _get_request_json(self, body) -> Dict[str, Any]:
        c = _get_cattrs_converter(type(body)) if body is not None else None
        return c.unstructure(body) if body is not None else None

    def _normalize_headers(self, headers: MutableMapping) -> Dict[str, List[str]]:
        normalized_headers: Dict[str, List[str]] = {}
        for name, value in headers.items():
            normalized_headers.setdefault(name.lower(), []).append(value)
        return normalized_headers

    def _parse_response(self, status_code: int, headers: MutableMapping, json_supplier, destination_class: Type[T]) -> T:
        if 200 <= status_code < 300:
            if destination_class is None:
                return
            c = _get_cattrs_converter(destination_class)
            response_body = json_supplier()
            return c.structure(response_body, destination_class)
        else:
            normalized_headers = self._normalize_headers(headers)
            # Best effort parsing of the response body
            if not 'content-type' in headers or headers['content-type'].split(';')[0].strip().lower() != 'application/json':
                raise APIException(status_code, headers=normalized_headers)
            try:
                response_body = json_supplier()
                raise APIException(status_code, response_body.get('errorCode'), response_body.get('errorMessage'), headers=normalized_headers)
            except APIException as e:
                raise e
            except Exception as e:
                raise APIException(status_code, headers=normalized_headers) from e


class AppStoreServerAPIClient(BaseAppStoreServerAPIClient):
    def __init__(self, signing_key: bytes, key_id: str, issuer_id: str, bundle_id: str, environment: Environment):
        super().__init__(signing_key=signing_key, key_id=key_id, issuer_id=issuer_id, bundle_id=bundle_id, environment=environment)
    
    def _make_request(self, path: str, method: str, queryParameters: Dict[str, Union[str, List[str]]], body, destination_class: Type[T], content_type: Optional[str] = None) -> T:
        url = self._get_full_url(path)
        headers = self._get_headers()

        if isinstance(body, bytes):
            if content_type:
                headers['Content-Type'] = content_type
            response = self._execute_request(method, url, queryParameters, headers, None, body)
        else:
            json = self._get_request_json(body)
            response = self._execute_request(method, url, queryParameters, headers, json, None)

        return self._parse_response(response.status_code, response.headers, lambda: response.json(), destination_class)

    def _execute_request(self, method: str, url: str, params: Dict[str, Union[str, List[str]]], headers: Dict[str, str], json: Optional[Dict[str, Any]], data: Optional[bytes]) -> requests.Response:
        return requests.request(method, url, params=params, headers=headers, json=json, data=data, timeout=30)

    def extend_renewal_date_for_all_active_subscribers(self, mass_extend_renewal_date_request: MassExtendRenewalDateRequest) -> MassExtendRenewalDateResponse: 
        """
        Uses a subscription's product identifier to extend the renewal date for all of its eligible active subscribers.
        https://developer.apple.com/documentation/appstoreserverapi/extend-subscription-renewal-dates-for-all-active-subscribers
        
        :param mass_extend_renewal_date_request: The request body for extending a subscription renewal date for all of its active subscribers.
        :return: A response that indicates the server successfully received the subscription-renewal-date extension request.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return self._make_request("/inApps/v1/subscriptions/extend/mass", "POST", {}, mass_extend_renewal_date_request, MassExtendRenewalDateResponse, None)

    def extend_subscription_renewal_date(self, original_transaction_id: str, extend_renewal_date_request: ExtendRenewalDateRequest) -> ExtendRenewalDateResponse:
        """
        Extends the renewal date of a customer's active subscription using the original transaction identifier.
        https://developer.apple.com/documentation/appstoreserverapi/extend-a-subscription-renewal-date
        
        :param original_transaction_id:    The original transaction identifier of the subscription receiving a renewal date extension.
        :param extend_renewal_date_request: The request body containing subscription-renewal-extension data.
        :return: A response that indicates whether an individual renewal-date extension succeeded, and related details.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return self._make_request(_path("/inApps/v1/subscriptions/extend/{}", original_transaction_id), "PUT", {}, extend_renewal_date_request, ExtendRenewalDateResponse, None)
    
    def get_all_subscription_statuses(self, any_transaction_id: str, status: Optional[List[Status]] = None) -> StatusResponse:
        """
        Get the statuses for all of a customer's auto-renewable subscriptions in your app.
        https://developer.apple.com/documentation/appstoreserverapi/get-all-subscription-statuses

        :param any_transaction_id: Any transactionId, originalTransactionId, or appTransactionId that belongs to the customer for your app.
        :param status: An optional filter that indicates the status of subscriptions to include in the response. Your query may specify more than one status query parameter.
        :return: A response that contains status information for all of a customer's auto-renewable subscriptions in your app.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        queryParameters: Dict[str, List[str]] = dict()
        if status is not None:
            queryParameters["status"] = [s.value for s in status]

        return self._make_request(_path("/inApps/v1/subscriptions/{}", any_transaction_id), "GET", queryParameters, None, StatusResponse, None)
    
    def get_refund_history(self, any_transaction_id: str, revision: Optional[str]) -> RefundHistoryResponse:
        """
        Get a paginated list of all of a customer's refunded in-app purchases for your app.
        https://developer.apple.com/documentation/appstoreserverapi/get-refund-history

        :param any_transaction_id: Any transactionId, originalTransactionId, or appTransactionId that belongs to the customer for your app.
        :param revision: A token you provide to get the next set of up to 20 transactions. All responses include a revision token. Use the revision token from the previous RefundHistoryResponse.
        :return: A response that contains an array of signed JSON Web Signature (JWS) refunded transactions, and paging information.
        :throws APIException: If a response was returned indicating the request could not be processed
        """

        queryParameters: Dict[str, List[str]] = dict()
        if revision is not None:
            queryParameters["revision"] = [revision]

        return self._make_request(_path("/inApps/v2/refund/lookup/{}", any_transaction_id), "GET", queryParameters, None, RefundHistoryResponse, None)
    
    def get_status_of_subscription_renewal_date_extensions(self, request_identifier: str, product_id: str) -> MassExtendRenewalDateStatusResponse:
        """
        Checks whether a renewal date extension request completed, and provides the final count of successful or failed extensions.
        https://developer.apple.com/documentation/appstoreserverapi/get-status-of-subscription-renewal-date-extensions

        :param request_identifier: The UUID that represents your request to the Extend Subscription Renewal Dates for All Active Subscribers endpoint.
        :param product_id: The product identifier of the auto-renewable subscription that you request a renewal-date extension for.
        :return: A response that indicates the current status of a request to extend the subscription renewal date to all eligible subscribers.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return self._make_request(_path("/inApps/v1/subscriptions/extend/mass/{}/{}", product_id, request_identifier), "GET", {}, None, MassExtendRenewalDateStatusResponse, None)
    
    def get_test_notification_status(self, test_notification_token: str) -> CheckTestNotificationResponse:
        """
        Check the status of the test App Store server notification sent to your server.
        https://developer.apple.com/documentation/appstoreserverapi/get-test-notification-status

        :param test_notification_token: The test notification token received from the Request a Test Notification endpoint
        :return: A response that contains the contents of the test notification sent by the App Store server and the result from your server.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return self._make_request(_path("/inApps/v1/notifications/test/{}", test_notification_token), "GET", {}, None, CheckTestNotificationResponse, None)
    
    def get_notification_history(self, pagination_token: Optional[str], notification_history_request: NotificationHistoryRequest) -> NotificationHistoryResponse:
        """
        Get a list of notifications that the App Store server attempted to send to your server.
        https://developer.apple.com/documentation/appstoreserverapi/get-notification-history

        :param pagination_token: An optional token you use to get the next set of up to 20 notification history records. All responses that have more records available include a paginationToken. Omit this parameter the first time you call this endpoint.
        :param notification_history_request: The request body that includes the start and end dates, and optional query constraints.
        :return: A response that contains the App Store Server Notifications history for your app.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        queryParameters: Dict[str, List[str]] = dict()
        if pagination_token is not None:
            queryParameters["paginationToken"] = [pagination_token]
        
        return self._make_request("/inApps/v1/notifications/history", "POST", queryParameters, notification_history_request, NotificationHistoryResponse, None)

    def get_transaction_history(self, any_transaction_id: str, revision: Optional[str], transaction_history_request: TransactionHistoryRequest, version: GetTransactionHistoryVersion = GetTransactionHistoryVersion.V1) -> HistoryResponse:
        """
        Get a customer's in-app purchase transaction history for your app.
        https://developer.apple.com/documentation/appstoreserverapi/get-transaction-history

        :param any_transaction_id: Any transactionId, originalTransactionId, or appTransactionId that belongs to the customer for your app.
        :param revision: A token you provide to get the next set of up to 20 transactions. All responses include a revision token. Note: For requests that use the revision token, include the same query parameters from the initial request. Use the revision token from the previous HistoryResponse.
        :param transaction_history_request: The request parameters that includes the startDate,endDate,productIds,productTypes and optional query constraints.
        :param version: The version of the Get Transaction History endpoint to use. V2 is recommended.
        :return: A response that contains the customer's transaction history for an app.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        version = GetTransactionHistoryVersion(version)
        if version == GetTransactionHistoryVersion.V1:
            warnings.warn("GetTransactionHistoryVersion.V1 is deprecated, use GetTransactionHistoryVersion.V2 instead", DeprecationWarning, stacklevel=2)

        queryParameters: Dict[str, List[str]] = dict()
        if revision is not None:
            queryParameters["revision"] = [revision]
        
        if transaction_history_request.startDate is not None:
            queryParameters["startDate"] = [str(transaction_history_request.startDate)]
        
        if transaction_history_request.endDate is not None:
            queryParameters["endDate"] = [str(transaction_history_request.endDate)]
        
        if transaction_history_request.productIds is not None:
            queryParameters["productId"] = transaction_history_request.productIds
        
        if transaction_history_request.productTypes is not None:
            queryParameters["productType"] = [product_type.value for product_type in transaction_history_request.productTypes]
        
        if transaction_history_request.sort is not None:
            queryParameters["sort"] = [transaction_history_request.sort.value]
        
        if transaction_history_request.subscriptionGroupIdentifiers is not None:
            queryParameters["subscriptionGroupIdentifier"] = transaction_history_request.subscriptionGroupIdentifiers
        
        if transaction_history_request.inAppOwnershipType is not None:
            queryParameters["inAppOwnershipType"] = [transaction_history_request.inAppOwnershipType.value]
        
        if transaction_history_request.revoked is not None:
            queryParameters["revoked"] = ["true" if transaction_history_request.revoked else "false"]
        
        return self._make_request(_path("/inApps/{}/history/{}", version.value, any_transaction_id), "GET", queryParameters, None, HistoryResponse, None)

    def get_transaction_info(self, transaction_id: str) -> TransactionInfoResponse:
        """
        Get information about a single transaction for your app.
        https://developer.apple.com/documentation/appstoreserverapi/get-transaction-info
        
        :param transaction_id: The identifier of a transaction that belongs to the customer, and which may be an original transaction identifier.
        :return: A response that contains signed transaction information for a single transaction.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return self._make_request(_path("/inApps/v1/transactions/{}", transaction_id), "GET", {}, None, TransactionInfoResponse, None)

    def look_up_order_id(self, order_id: str) -> OrderLookupResponse:
        """
        Get a customer's in-app purchases from a receipt using the order ID.
        https://developer.apple.com/documentation/appstoreserverapi/look-up-order-id
        
        :param order_id: The order ID for in-app purchases that belong to the customer.
        :return: A response that includes the order lookup status and an array of signed transactions for the in-app purchases in the order.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return self._make_request(_path("/inApps/v1/lookup/{}", order_id), "GET", {}, None, OrderLookupResponse, None)
    
    def request_test_notification(self) -> SendTestNotificationResponse:
        """
        Ask App Store Server Notifications to send a test notification to your server.
        https://developer.apple.com/documentation/appstoreserverapi/request-a-test-notification

        :return: A response that contains the test notification token.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return self._make_request("/inApps/v1/notifications/test", "POST", {}, None, SendTestNotificationResponse, None)

    def send_consumption_data(self, transaction_id: str, consumption_request: ConsumptionRequestV1):
        """
        Send consumption information about a consumable in-app purchase to the App Store after your server receives a consumption request notification.
        https://developer.apple.com/documentation/appstoreserverapi/send-consumption-information-v1

        .. deprecated::
            Use :func:`send_consumption_information` instead.

        :param transaction_id: The transaction identifier for which you're providing consumption information. You receive this identifier in the CONSUMPTION_REQUEST notification the App Store sends to your server.
        :param consumption_request:    The request body containing consumption information.
        :raises APIException: If a response was returned indicating the request could not be processed
        """
        warnings.warn("send_consumption_data is deprecated, use send_consumption_information instead", DeprecationWarning, stacklevel=2)
        self._make_request(_path("/inApps/v1/transactions/consumption/{}", transaction_id), "PUT", {}, consumption_request, None, None)

    def send_consumption_information(self, transaction_id: str, consumption_request: ConsumptionRequest):
        """
        Send consumption information about an In-App Purchase to the App Store after your server receives a consumption request notification.
        https://developer.apple.com/documentation/appstoreserverapi/send-consumption-information

        :param transaction_id: The transaction identifier for which you're providing consumption information. You receive this identifier in the CONSUMPTION_REQUEST notification the App Store sends to your server's App Store Server Notifications V2 endpoint.
        :param consumption_request:    The request body containing consumption information.
        :raises APIException: If a response was returned indicating the request could not be processed
        """
        self._make_request(_path("/inApps/v2/transactions/consumption/{}", transaction_id), "PUT", {}, consumption_request, None, None)

    def set_app_account_token(self, original_transaction_id: str, update_app_account_token_request: UpdateAppAccountTokenRequest):
        """
        Sets the app account token value for a purchase the customer makes outside your app, or updates its value in an existing transaction.
        https://developer.apple.com/documentation/appstoreserverapi/set-app-account-token

        :param original_transaction_id: The original transaction identifier of the transaction to receive the app account token update.
        :param update_app_account_token_request: The request body that contains a valid app account token value.
        :raises APIException: If a response was returned indicating the request could not be processed
        """
        self._make_request(_path("/inApps/v1/transactions/{}/appAccountToken", original_transaction_id), "PUT", {}, update_app_account_token_request, None, None)

    def upload_image(self, image_identifier: UUID, image: bytes, image_size: Optional[ImageSize] = None):
        """
        Upload an image to use for retention messaging.

        :param image_identifier: A UUID you provide to uniquely identify the image you upload.
        :param image: The image file to upload.
        :param image_size: The size of the image you upload.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/upload-image
        """
        query_parameters = {}
        if image_size is not None:
            query_parameters["imageSize"] = [image_size.value]
        self._make_request(_path("/inApps/v1/messaging/image/{}", image_identifier), "PUT", query_parameters, image, None, "image/png")

    def delete_image(self, image_identifier: UUID):
        """
        Delete a previously uploaded image.

        :param image_identifier: The identifier of the image to delete.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/delete-image
        """
        self._make_request(_path("/inApps/v1/messaging/image/{}", image_identifier), "DELETE", {}, None, None, None)

    def get_image_list(self) -> GetImageListResponse:
        """
        Get the image identifier and state for all uploaded images.

        :return: A response that contains status information for all images.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/get-image-list
        """
        return self._make_request("/inApps/v1/messaging/image/list", "GET", {}, None, GetImageListResponse, None)

    def upload_message(self, message_identifier: UUID, upload_message_request_body: UploadMessageRequestBody):
        """
        Upload a message to use for retention messaging.

        :param message_identifier: A UUID you provide to uniquely identify the message you upload.
        :param upload_message_request_body: The message text to upload.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/upload-message
        """
        self._make_request(_path("/inApps/v1/messaging/message/{}", message_identifier), "PUT", {}, upload_message_request_body, None, None)

    def delete_message(self, message_identifier: UUID):
        """
        Delete a previously uploaded message.

        :param message_identifier: The identifier of the message to delete.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/delete-message
        """
        self._make_request(_path("/inApps/v1/messaging/message/{}", message_identifier), "DELETE", {}, None, None, None)

    def get_message_list(self) -> GetMessageListResponse:
        """
        Get the message identifier and state of all uploaded messages.

        :return: A response that contains status information for all messages.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/get-message-list
        """
        return self._make_request("/inApps/v1/messaging/message/list", "GET", {}, None, GetMessageListResponse, None)

    def configure_default_message(self, product_id: str, locale: str, default_configuration_request: DefaultConfigurationRequest):
        """
        Configure a default message for a specific product in a specific locale.

        :param product_id: The product identifier for the default configuration.
        :param locale: The locale for the default configuration.
        :param default_configuration_request: The request body that includes the message identifier to configure as the default message.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/configure-default-message
        """
        self._make_request(_path("/inApps/v1/messaging/default/{}/{}", product_id, locale), "PUT", {}, default_configuration_request, None, None)

    def delete_default_message(self, product_id: str, locale: str):
        """
        Delete a default message for a product in a locale.

        :param product_id: The product ID of the default message configuration.
        :param locale: The locale of the default message configuration.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/delete-default-message
        """
        self._make_request(_path("/inApps/v1/messaging/default/{}/{}", product_id, locale), "DELETE", {}, None, None, None)

    def get_default_message(self, product_id: str, locale: str) -> DefaultConfigurationResponse:
        """
        Gets the default message for a specific product in a specific locale, if it’s configured.

        :param product_id: The product identifier of the message.
        :param locale: The locale of the message.
        :return: The response body that contains the default configuration information.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/get-default-message
        """
        return self._make_request(_path("/inApps/v1/messaging/default/{}/{}", product_id, locale), "GET", {}, None, DefaultConfigurationResponse, None)

    def configure_realtime_url(self, realtime_url_request: RealtimeUrlRequest):
        """
        Configures the URL for your Get Retention Message endpoint in the sandbox and production environments.

        :param realtime_url_request: The request body that includes your endpoint’s URL.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/configure-realtime-url
        """
        self._make_request("/inApps/v1/messaging/realtime/url", "PUT", {}, realtime_url_request, None, None)

    def delete_realtime_url(self):
        """
        Deletes the URL for your Get Retention Message endpoint, in the sandbox or production environments.

        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/delete-realtime-url
        """
        self._make_request("/inApps/v1/messaging/realtime/url", "DELETE", {}, None, None, None)

    def get_realtime_url(self) -> RealtimeUrlResponse:
        """
        Gets the URL for real-time messages that points to your Get Retention Message endpoint, which you previously configured.

        :return: The response body that contains the URL for your Get Retention Message endpoint.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/get-realtime-url
        """
        return self._make_request("/inApps/v1/messaging/realtime/url", "GET", {}, None, RealtimeUrlResponse, None)

    def initiate_performance_test(self, performance_test_request: PerformanceTestRequest) -> PerformanceTestResponse:
        """
        Initiates a performance test of your Get Retention Message endpoint in the sandbox environment.

        :param performance_test_request: The request body which specifies a transaction identifier of an In-App Purchase to use for this test.
        :return: The performance test response object.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/initiate-performance-test
        """
        return self._make_request("/inApps/v1/messaging/performanceTest", "POST", {}, performance_test_request, PerformanceTestResponse, None)

    def get_performance_test_results(self, request_id: UUID) -> PerformanceTestResultResponse:
        """
        Gets the results of the performance test for the specified identifier.

        :param request_id: The ID of the performance test to return, which you receive in the PerformanceTestResponse when you call Initiate Performance Test.
        :return: An object the API returns that describes the performance test results.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/get-performance-test-results
        """
        return self._make_request(_path("/inApps/v1/messaging/performanceTest/result/{}", str(request_id).lower()), "GET", {}, None, PerformanceTestResultResponse, None)

    def get_app_transaction_info(self, any_transaction_id: str) -> AppTransactionInfoResponse:
        """
        Get a customer's app transaction information for your app.

        :param any_transaction_id: Any transactionId, originalTransactionId, or appTransactionId that belongs to the customer for your app.
        :return: A response that contains signed app transaction information for a customer.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/appstoreserverapi/get-app-transaction-info
        """
        return self._make_request(_path("/inApps/v1/transactions/appTransactions/{}", any_transaction_id), "GET", {}, None, AppTransactionInfoResponse, None)

    def finish_transaction(self, transaction_id: str):
        """
        Notifies the App Store server that your system has finished processing the customer's transaction.
        https://developer.apple.com/documentation/appstoreserverapi/finish-transaction

        :param transaction_id: The transaction identifier of the transaction to mark as finished.
        :raises APIException: If a response was returned indicating the request could not be processed
        """
        self._make_request(_path("/inApps/v1/transactions/{}/finish", transaction_id), "POST", {}, None, None, None)

    def change_subscription_price(self, transaction_id: str, subscription_price_change_request: AdvancedCommerceSubscriptionPriceChangeRequest) -> AdvancedCommerceSubscriptionPriceChangeResponse:
        """
        Increase or decrease the price of an auto-renewable subscription, a bundle, or individual items within a subscription at the next renewal.

        :param transaction_id: A transaction identifier of the auto-renewable subscription that is subject to the price change.
        :param subscription_price_change_request: The request body that contains the details of the price change.
        :return: A response that contains signed JWS renewal and JWS transaction information after a subscription price change request.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/advancedcommerceapi/change-subscription-price
        """
        return self._make_request(_path("/advancedCommerce/v1/subscription/changePrice/{}", transaction_id), "POST", {}, subscription_price_change_request, AdvancedCommerceSubscriptionPriceChangeResponse, None)

    def cancel_subscription(self, transaction_id: str, subscription_cancel_request: AdvancedCommerceSubscriptionCancelRequest) -> AdvancedCommerceSubscriptionCancelResponse:
        """
        Turn off automatic renewal to cancel a customer's auto-renewable subscription.

        :param transaction_id: The transaction identifier of the auto-renewable subscription to cancel.
        :param subscription_cancel_request: The request body that includes information about the subscription to cancel.
        :return: The response body for a successful subscription cancellation.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/advancedcommerceapi/cancel-a-subscription
        """
        return self._make_request(_path("/advancedCommerce/v1/subscription/cancel/{}", transaction_id), "POST", {}, subscription_cancel_request, AdvancedCommerceSubscriptionCancelResponse, None)

    def revoke_subscription(self, transaction_id: str, subscription_revoke_request: AdvancedCommerceSubscriptionRevokeRequest) -> AdvancedCommerceSubscriptionRevokeResponse:
        """
        Immediately cancel a customer's subscription and all the items that are included in the subscription, and request a full or prorated refund.

        :param transaction_id: The transaction identifier of the auto-renewable subscription to revoke.
        :param subscription_revoke_request: The request body you provide to terminate a subscription and all its items immediately.
        :return: The response body for a successful revoke-subscription request.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/advancedcommerceapi/revoke-subscription
        """
        return self._make_request(_path("/advancedCommerce/v1/subscription/revoke/{}", transaction_id), "POST", {}, subscription_revoke_request, AdvancedCommerceSubscriptionRevokeResponse, None)

    def request_transaction_refund(self, transaction_id: str, request_refund_request: AdvancedCommerceRequestRefundRequest) -> AdvancedCommerceRequestRefundResponse:
        """
        Request a refund for a one-time charge or subscription transaction.

        :param transaction_id: The transaction identifier for which you request a refund.
        :param request_refund_request: The request body for requesting a refund for a transaction.
        :return: The response body for a transaction refund request.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/advancedcommerceapi/request-transaction-refund
        """
        return self._make_request(_path("/advancedCommerce/v1/transaction/requestRefund/{}", transaction_id), "POST", {}, request_refund_request, AdvancedCommerceRequestRefundResponse, None)

    def change_subscription_metadata(self, transaction_id: str, subscription_change_metadata_request: AdvancedCommerceSubscriptionChangeMetadataRequest) -> AdvancedCommerceSubscriptionChangeMetadataResponse:
        """
        Update the SKU, display name, and description associated with a subscription, without affecting the subscription's billing or its service.

        :param transaction_id: The transaction identifier of the auto-renewable subscription to get changes to its metadata.
        :param subscription_change_metadata_request: The request body that contains the metadata changes.
        :return: The response body for a successful subscription metadata change.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/advancedcommerceapi/change-subscription-metadata
        """
        return self._make_request(_path("/advancedCommerce/v1/subscription/changeMetadata/{}", transaction_id), "POST", {}, subscription_change_metadata_request, AdvancedCommerceSubscriptionChangeMetadataResponse, None)

    def migrate_subscription_to_advanced_commerce_api(self, transaction_id: str, subscription_migrate_request: AdvancedCommerceSubscriptionMigrateRequest) -> AdvancedCommerceSubscriptionMigrateResponse:
        """
        Migrate a subscription that a customer purchased through Apple In-App Purchase to a subscription you manage using the Advanced Commerce API.

        :param transaction_id: The transaction identifier of the auto-renewable subscription to migrate.
        :param subscription_migrate_request: The request body that contains the details for the migration.
        :return: A response that contains signed renewal and transaction information after a subscription successfully migrates to the Advanced Commerce API.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/advancedcommerceapi/migrate-subscription-to-advanced-commerce-api
        """
        return self._make_request(_path("/advancedCommerce/v1/subscription/migrate/{}", transaction_id), "POST", {}, subscription_migrate_request, AdvancedCommerceSubscriptionMigrateResponse, None)

    def get_customer_groups(self, any_transaction_id: str) -> GetCustomerGroupsResponse:
        """
        Get the groups that a customer belongs to, and their role in each group.

        :param any_transaction_id: Any originalTransactionId, transactionId, or appTransactionId that belongs to the customer for your app.
        :return: A response that contains the groups a customer belongs to, and their role in each group.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/appstoreserverapi/get-customer-groups
        """
        return self._make_request(_path("/groups/v1/currentGroups/{}", any_transaction_id), "GET", {}, None, GetCustomerGroupsResponse, None)

    def get_group_members(self, group_id: str, pagination_token: Optional[str] = None, limit: Optional[int] = None) -> GetGroupMembersResponse:
        """
        Get a paginated list of the customers that belong to a group.

        :param group_id: The identifier of a group in your app, which the Get Customer Groups endpoint returns.
        :param pagination_token: An optional token you use to get the next set of members. Responses that have more members available include a paginationToken. Omit this parameter the first time you call this endpoint.
        :param limit: An optional maximum number of members to return in a single response.
        :return: A response that contains a page of the customers that belong to a group.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/appstoreserverapi/get-group-members
        """
        queryParameters: Dict[str, List[str]] = dict()
        if pagination_token is not None:
            queryParameters["paginationToken"] = [pagination_token]
        if limit is not None:
            queryParameters["limit"] = [str(limit)]

        return self._make_request(_path("/groups/v1/group/{}", group_id), "GET", queryParameters, None, GetGroupMembersResponse, None)

class AsyncAppStoreServerAPIClient(BaseAppStoreServerAPIClient):
    def __init__(self, signing_key: bytes, key_id: str, issuer_id: str, bundle_id: str, environment: Environment):
        super().__init__(signing_key=signing_key, key_id=key_id, issuer_id=issuer_id, bundle_id=bundle_id, environment=environment)
        try:
            import httpx
            self.http_client = httpx.AsyncClient()
        except:
            raise ModuleNotFoundError("httpx not found but attempting to instantiate an async client")

    async def async_close(self):
        await self.http_client.aclose()

    def _normalize_headers(self, headers: MutableMapping) -> Dict[str, List[str]]:
        normalized_headers: Dict[str, List[str]] = {}
        for name, value in headers.multi_items():
            normalized_headers.setdefault(name.lower(), []).append(value)
        return normalized_headers
    
    async def _make_request(self, path: str, method: str, queryParameters: Dict[str, Union[str, List[str]]], body, destination_class: Type[T], content_type: Optional[str] = None) -> T:
        url = self._get_full_url(path)
        headers = self._get_headers()

        if isinstance(body, bytes):
            # For binary data like images
            if content_type:
                headers['Content-Type'] = content_type
            response = await self._execute_request(method, url, queryParameters, headers, None, body)
        else:
            # For JSON data
            json = self._get_request_json(body)
            response = await self._execute_request(method, url, queryParameters, headers, json, None)

        return self._parse_response(response.status_code, response.headers, lambda: response.json(), destination_class)

    async def _execute_request(self, method: str, url: str, params: Dict[str, Union[str, List[str]]], headers: Dict[str, str], json: Optional[Dict[str, Any]], data: Optional[bytes]):
        return await self.http_client.request(method, url, params=params, headers=headers, json=json, data=data, timeout=30)

    async def extend_renewal_date_for_all_active_subscribers(self, mass_extend_renewal_date_request: MassExtendRenewalDateRequest) -> MassExtendRenewalDateResponse: 
        """
        Uses a subscription's product identifier to extend the renewal date for all of its eligible active subscribers.
        https://developer.apple.com/documentation/appstoreserverapi/extend-subscription-renewal-dates-for-all-active-subscribers
        
        :param mass_extend_renewal_date_request: The request body for extending a subscription renewal date for all of its active subscribers.
        :return: A response that indicates the server successfully received the subscription-renewal-date extension request.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return await self._make_request("/inApps/v1/subscriptions/extend/mass", "POST", {}, mass_extend_renewal_date_request, MassExtendRenewalDateResponse, None)

    async def extend_subscription_renewal_date(self, original_transaction_id: str, extend_renewal_date_request: ExtendRenewalDateRequest) -> ExtendRenewalDateResponse:
        """
        Extends the renewal date of a customer's active subscription using the original transaction identifier.
        https://developer.apple.com/documentation/appstoreserverapi/extend-a-subscription-renewal-date
        
        :param original_transaction_id:    The original transaction identifier of the subscription receiving a renewal date extension.
        :param extend_renewal_date_request: The request body containing subscription-renewal-extension data.
        :return: A response that indicates whether an individual renewal-date extension succeeded, and related details.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return await self._make_request(_path("/inApps/v1/subscriptions/extend/{}", original_transaction_id), "PUT", {}, extend_renewal_date_request, ExtendRenewalDateResponse, None)
    
    async def get_all_subscription_statuses(self, any_transaction_id: str, status: Optional[List[Status]] = None) -> StatusResponse:
        """
        Get the statuses for all of a customer's auto-renewable subscriptions in your app.
        https://developer.apple.com/documentation/appstoreserverapi/get-all-subscription-statuses

        :param any_transaction_id: Any transactionId, originalTransactionId, or appTransactionId that belongs to the customer for your app.
        :param status: An optional filter that indicates the status of subscriptions to include in the response. Your query may specify more than one status query parameter.
        :return: A response that contains status information for all of a customer's auto-renewable subscriptions in your app.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        queryParameters: Dict[str, List[str]] = dict()
        if status is not None:
            queryParameters["status"] = [s.value for s in status]

        return await self._make_request(_path("/inApps/v1/subscriptions/{}", any_transaction_id), "GET", queryParameters, None, StatusResponse, None)
    
    async def get_refund_history(self, any_transaction_id: str, revision: Optional[str]) -> RefundHistoryResponse:
        """
        Get a paginated list of all of a customer's refunded in-app purchases for your app.
        https://developer.apple.com/documentation/appstoreserverapi/get-refund-history

        :param any_transaction_id: Any transactionId, originalTransactionId, or appTransactionId that belongs to the customer for your app.
        :param revision: A token you provide to get the next set of up to 20 transactions. All responses include a revision token. Use the revision token from the previous RefundHistoryResponse.
        :return: A response that contains an array of signed JSON Web Signature (JWS) refunded transactions, and paging information.
        :throws APIException: If a response was returned indicating the request could not be processed
        """

        queryParameters: Dict[str, List[str]] = dict()
        if revision is not None:
            queryParameters["revision"] = [revision]

        return await self._make_request(_path("/inApps/v2/refund/lookup/{}", any_transaction_id), "GET", queryParameters, None, RefundHistoryResponse, None)
    
    async def get_status_of_subscription_renewal_date_extensions(self, request_identifier: str, product_id: str) -> MassExtendRenewalDateStatusResponse:
        """
        Checks whether a renewal date extension request completed, and provides the final count of successful or failed extensions.
        https://developer.apple.com/documentation/appstoreserverapi/get-status-of-subscription-renewal-date-extensions

        :param request_identifier: The UUID that represents your request to the Extend Subscription Renewal Dates for All Active Subscribers endpoint.
        :param product_id: The product identifier of the auto-renewable subscription that you request a renewal-date extension for.
        :return: A response that indicates the current status of a request to extend the subscription renewal date to all eligible subscribers.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return await self._make_request(_path("/inApps/v1/subscriptions/extend/mass/{}/{}", product_id, request_identifier), "GET", {}, None, MassExtendRenewalDateStatusResponse, None)
    
    async def get_test_notification_status(self, test_notification_token: str) -> CheckTestNotificationResponse:
        """
        Check the status of the test App Store server notification sent to your server.
        https://developer.apple.com/documentation/appstoreserverapi/get-test-notification-status

        :param test_notification_token: The test notification token received from the Request a Test Notification endpoint
        :return: A response that contains the contents of the test notification sent by the App Store server and the result from your server.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return await self._make_request(_path("/inApps/v1/notifications/test/{}", test_notification_token), "GET", {}, None, CheckTestNotificationResponse, None)
    
    async def get_notification_history(self, pagination_token: Optional[str], notification_history_request: NotificationHistoryRequest) -> NotificationHistoryResponse:
        """
        Get a list of notifications that the App Store server attempted to send to your server.
        https://developer.apple.com/documentation/appstoreserverapi/get-notification-history

        :param pagination_token: An optional token you use to get the next set of up to 20 notification history records. All responses that have more records available include a paginationToken. Omit this parameter the first time you call this endpoint.
        :param notification_history_request: The request body that includes the start and end dates, and optional query constraints.
        :return: A response that contains the App Store Server Notifications history for your app.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        queryParameters: Dict[str, List[str]] = dict()
        if pagination_token is not None:
            queryParameters["paginationToken"] = [pagination_token]
        
        return await self._make_request("/inApps/v1/notifications/history", "POST", queryParameters, notification_history_request, NotificationHistoryResponse, None)

    async def get_transaction_history(self, any_transaction_id: str, revision: Optional[str], transaction_history_request: TransactionHistoryRequest, version: GetTransactionHistoryVersion = GetTransactionHistoryVersion.V1) -> HistoryResponse:
        """
        Get a customer's in-app purchase transaction history for your app.
        https://developer.apple.com/documentation/appstoreserverapi/get-transaction-history

        :param any_transaction_id: Any transactionId, originalTransactionId, or appTransactionId that belongs to the customer for your app.
        :param revision: A token you provide to get the next set of up to 20 transactions. All responses include a revision token. Note: For requests that use the revision token, include the same query parameters from the initial request. Use the revision token from the previous HistoryResponse.
        :param transaction_history_request: The request parameters that includes the startDate,endDate,productIds,productTypes and optional query constraints.
        :param version: The version of the Get Transaction History endpoint to use. V2 is recommended.
        :return: A response that contains the customer's transaction history for an app.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        version = GetTransactionHistoryVersion(version)
        if version == GetTransactionHistoryVersion.V1:
            warnings.warn("GetTransactionHistoryVersion.V1 is deprecated, use GetTransactionHistoryVersion.V2 instead", DeprecationWarning, stacklevel=2)

        queryParameters: Dict[str, List[str]] = dict()
        if revision is not None:
            queryParameters["revision"] = [revision]
        
        if transaction_history_request.startDate is not None:
            queryParameters["startDate"] = [str(transaction_history_request.startDate)]
        
        if transaction_history_request.endDate is not None:
            queryParameters["endDate"] = [str(transaction_history_request.endDate)]
        
        if transaction_history_request.productIds is not None:
            queryParameters["productId"] = transaction_history_request.productIds
        
        if transaction_history_request.productTypes is not None:
            queryParameters["productType"] = [product_type.value for product_type in transaction_history_request.productTypes]
        
        if transaction_history_request.sort is not None:
            queryParameters["sort"] = [transaction_history_request.sort.value]
        
        if transaction_history_request.subscriptionGroupIdentifiers is not None:
            queryParameters["subscriptionGroupIdentifier"] = transaction_history_request.subscriptionGroupIdentifiers
        
        if transaction_history_request.inAppOwnershipType is not None:
            queryParameters["inAppOwnershipType"] = [transaction_history_request.inAppOwnershipType.value]
        
        if transaction_history_request.revoked is not None:
            queryParameters["revoked"] = ["true" if transaction_history_request.revoked else "false"]
        
        return await self._make_request(_path("/inApps/{}/history/{}", version.value, any_transaction_id), "GET", queryParameters, None, HistoryResponse, None)

    async def get_transaction_info(self, transaction_id: str) -> TransactionInfoResponse:
        """
        Get information about a single transaction for your app.
        https://developer.apple.com/documentation/appstoreserverapi/get-transaction-info
        
        :param transaction_id: The identifier of a transaction that belongs to the customer, and which may be an original transaction identifier.
        :return: A response that contains signed transaction information for a single transaction.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return await self._make_request(_path("/inApps/v1/transactions/{}", transaction_id), "GET", {}, None, TransactionInfoResponse, None)

    async def look_up_order_id(self, order_id: str) -> OrderLookupResponse:
        """
        Get a customer's in-app purchases from a receipt using the order ID.
        https://developer.apple.com/documentation/appstoreserverapi/look-up-order-id
        
        :param order_id: The order ID for in-app purchases that belong to the customer.
        :return: A response that includes the order lookup status and an array of signed transactions for the in-app purchases in the order.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return await self._make_request(_path("/inApps/v1/lookup/{}", order_id), "GET", {}, None, OrderLookupResponse, None)
    async def request_test_notification(self) -> SendTestNotificationResponse:
        """
        Ask App Store Server Notifications to send a test notification to your server.
        https://developer.apple.com/documentation/appstoreserverapi/request-a-test-notification

        :return: A response that contains the test notification token.
        :throws APIException: If a response was returned indicating the request could not be processed
        """
        return await self._make_request("/inApps/v1/notifications/test", "POST", {}, None, SendTestNotificationResponse, None)

    async def send_consumption_data(self, transaction_id: str, consumption_request: ConsumptionRequestV1):
        """
        Send consumption information about a consumable in-app purchase to the App Store after your server receives a consumption request notification.
        https://developer.apple.com/documentation/appstoreserverapi/send-consumption-information-v1

        .. deprecated::
            Use :func:`send_consumption_information` instead.

        :param transaction_id: The transaction identifier for which you're providing consumption information. You receive this identifier in the CONSUMPTION_REQUEST notification the App Store sends to your server.
        :param consumption_request:    The request body containing consumption information.
        :raises APIException: If a response was returned indicating the request could not be processed
        """
        warnings.warn("send_consumption_data is deprecated, use send_consumption_information instead", DeprecationWarning, stacklevel=2)
        await self._make_request(_path("/inApps/v1/transactions/consumption/{}", transaction_id), "PUT", {}, consumption_request, None, None)

    async def send_consumption_information(self, transaction_id: str, consumption_request: ConsumptionRequest):
        """
        Send consumption information about an In-App Purchase to the App Store after your server receives a consumption request notification.
        https://developer.apple.com/documentation/appstoreserverapi/send-consumption-information

        :param transaction_id: The transaction identifier for which you're providing consumption information. You receive this identifier in the CONSUMPTION_REQUEST notification the App Store sends to your server's App Store Server Notifications V2 endpoint.
        :param consumption_request:    The request body containing consumption information.
        :raises APIException: If a response was returned indicating the request could not be processed
        """
        await self._make_request(_path("/inApps/v2/transactions/consumption/{}", transaction_id), "PUT", {}, consumption_request, None, None)

    async def set_app_account_token(self, original_transaction_id: str, update_app_account_token_request: UpdateAppAccountTokenRequest):
        """
        Sets the app account token value for a purchase the customer makes outside your app, or updates its value in an existing transaction.
        https://developer.apple.com/documentation/appstoreserverapi/set-app-account-token

        :param original_transaction_id: The original transaction identifier of the transaction to receive the app account token update.
        :param update_app_account_token_request: The request body that contains a valid app account token value.
        :raises APIException: If a response was returned indicating the request could not be processed
        """
        await self._make_request(_path("/inApps/v1/transactions/{}/appAccountToken", original_transaction_id), "PUT", {}, update_app_account_token_request, None, None)

    async def upload_image(self, image_identifier: UUID, image: bytes, image_size: Optional[ImageSize] = None):
        """
        Upload an image to use for retention messaging.

        :param image_identifier: A UUID you provide to uniquely identify the image you upload.
        :param image: The image file to upload.
        :param image_size: The optional size of the image.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/upload-image
        """
        query_parameters = {}
        if image_size is not None:
            query_parameters["imageSize"] = [image_size.value]
        await self._make_request(_path("/inApps/v1/messaging/image/{}", image_identifier), "PUT", query_parameters, image, None, "image/png")

    async def delete_image(self, image_identifier: UUID):
        """
        Delete a previously uploaded image.

        :param image_identifier: The identifier of the image to delete.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/delete-image
        """
        await self._make_request(_path("/inApps/v1/messaging/image/{}", image_identifier), "DELETE", {}, None, None, None)

    async def get_image_list(self) -> GetImageListResponse:
        """
        Get the image identifier and state for all uploaded images.

        :return: A response that contains status information for all images.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/get-image-list
        """
        return await self._make_request("/inApps/v1/messaging/image/list", "GET", {}, None, GetImageListResponse, None)

    async def upload_message(self, message_identifier: UUID, upload_message_request_body: UploadMessageRequestBody):
        """
        Upload a message to use for retention messaging.

        :param message_identifier: A UUID you provide to uniquely identify the message you upload.
        :param upload_message_request_body: The message text to upload.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/upload-message
        """
        await self._make_request(_path("/inApps/v1/messaging/message/{}", message_identifier), "PUT", {}, upload_message_request_body, None, None)

    async def delete_message(self, message_identifier: UUID):
        """
        Delete a previously uploaded message.

        :param message_identifier: The identifier of the message to delete.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/delete-message
        """
        await self._make_request(_path("/inApps/v1/messaging/message/{}", message_identifier), "DELETE", {}, None, None, None)

    async def get_message_list(self) -> GetMessageListResponse:
        """
        Get the message identifier and state of all uploaded messages.

        :return: A response that contains status information for all messages.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/get-message-list
        """
        return await self._make_request("/inApps/v1/messaging/message/list", "GET", {}, None, GetMessageListResponse, None)

    async def configure_default_message(self, product_id: str, locale: str, default_configuration_request: DefaultConfigurationRequest):
        """
        Configure a default message for a specific product in a specific locale.

        :param product_id: The product identifier for the default configuration.
        :param locale: The locale for the default configuration.
        :param default_configuration_request: The request body that includes the message identifier to configure as the default message.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/configure-default-message
        """
        await self._make_request(_path("/inApps/v1/messaging/default/{}/{}", product_id, locale), "PUT", {}, default_configuration_request, None, None)

    async def delete_default_message(self, product_id: str, locale: str):
        """
        Delete a default message for a product in a locale.

        :param product_id: The product ID of the default message configuration.
        :param locale: The locale of the default message configuration.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/delete-default-message
        """
        await self._make_request(_path("/inApps/v1/messaging/default/{}/{}", product_id, locale), "DELETE", {}, None, None, None)

    async def get_default_message(self, product_id: str, locale: str) -> DefaultConfigurationResponse:
        """
        Get the default message for a specific product in a specific locale.

        :param product_id: The product identifier for the default configuration.
        :param locale: The locale for the default configuration.
        :return: A response that contains the default configuration information.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/get-default-message
        """
        return await self._make_request(_path("/inApps/v1/messaging/default/{}/{}", product_id, locale), "GET", {}, None, DefaultConfigurationResponse, None)

    async def configure_realtime_url(self, realtime_url_request: RealtimeUrlRequest):
        """
        Configure the real-time URL for retention messaging.

        :param realtime_url_request: The request body that contains the real-time URL.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/configure-realtime-url
        """
        await self._make_request("/inApps/v1/messaging/realtime/url", "PUT", {}, realtime_url_request, None, None)

    async def delete_realtime_url(self):
        """
        Delete the real-time URL for retention messaging.

        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/delete-realtime-url
        """
        await self._make_request("/inApps/v1/messaging/realtime/url", "DELETE", {}, None, None, None)

    async def get_realtime_url(self) -> RealtimeUrlResponse:
        """
        Get the real-time URL for retention messaging.

        :return: A response that contains the real-time URL information.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/get-realtime-url
        """
        return await self._make_request("/inApps/v1/messaging/realtime/url", "GET", {}, None, RealtimeUrlResponse, None)

    async def initiate_performance_test(self, performance_test_request: PerformanceTestRequest) -> PerformanceTestResponse:
        """
        Initiates a performance test of your Get Retention Message endpoint in the sandbox environment.

        :param performance_test_request: The request body which specifies a transaction identifier of an In-App Purchase to use for this test.
        :return: The performance test response object.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/initiate-performance-test
        """
        return await self._make_request("/inApps/v1/messaging/performanceTest", "POST", {}, performance_test_request, PerformanceTestResponse, None)

    async def get_performance_test_results(self, request_id: UUID) -> PerformanceTestResultResponse:
        """
        Gets the results of the performance test for the specified identifier.

        :param request_id: The ID of the performance test to return, which you receive in the PerformanceTestResponse when you call Initiate Performance Test.
        :return: An object the API returns that describes the performance test results.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/retentionmessaging/get-performance-test-results
        """
        return await self._make_request(_path("/inApps/v1/messaging/performanceTest/result/{}", str(request_id).lower()), "GET", {}, None, PerformanceTestResultResponse, None)

    async def get_app_transaction_info(self, any_transaction_id: str) -> AppTransactionInfoResponse:
        """
        Get a customer's app transaction information for your app.

        :param any_transaction_id: Any transactionId, originalTransactionId, or appTransactionId that belongs to the customer for your app.
        :return: A response that contains signed app transaction information for a customer.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/appstoreserverapi/get-app-transaction-info
        """
        return await self._make_request(_path("/inApps/v1/transactions/appTransactions/{}", any_transaction_id), "GET", {}, None, AppTransactionInfoResponse, None)

    async def finish_transaction(self, transaction_id: str):
        """
        Notifies the App Store server that your system has finished processing the customer's transaction.
        https://developer.apple.com/documentation/appstoreserverapi/finish-transaction

        :param transaction_id: The transaction identifier of the transaction to mark as finished.
        :raises APIException: If a response was returned indicating the request could not be processed
        """
        await self._make_request(_path("/inApps/v1/transactions/{}/finish", transaction_id), "POST", {}, None, None, None)

    async def change_subscription_price(self, transaction_id: str, subscription_price_change_request: AdvancedCommerceSubscriptionPriceChangeRequest) -> AdvancedCommerceSubscriptionPriceChangeResponse:
        """
        Increase or decrease the price of an auto-renewable subscription, a bundle, or individual items within a subscription at the next renewal.

        :param transaction_id: A transaction identifier of the auto-renewable subscription that is subject to the price change.
        :param subscription_price_change_request: The request body that contains the details of the price change.
        :return: A response that contains signed JWS renewal and JWS transaction information after a subscription price change request.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/advancedcommerceapi/change-subscription-price
        """
        return await self._make_request(_path("/advancedCommerce/v1/subscription/changePrice/{}", transaction_id), "POST", {}, subscription_price_change_request, AdvancedCommerceSubscriptionPriceChangeResponse, None)

    async def cancel_subscription(self, transaction_id: str, subscription_cancel_request: AdvancedCommerceSubscriptionCancelRequest) -> AdvancedCommerceSubscriptionCancelResponse:
        """
        Turn off automatic renewal to cancel a customer's auto-renewable subscription.

        :param transaction_id: The transaction identifier of the auto-renewable subscription to cancel.
        :param subscription_cancel_request: The request body that includes information about the subscription to cancel.
        :return: The response body for a successful subscription cancellation.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/advancedcommerceapi/cancel-a-subscription
        """
        return await self._make_request(_path("/advancedCommerce/v1/subscription/cancel/{}", transaction_id), "POST", {}, subscription_cancel_request, AdvancedCommerceSubscriptionCancelResponse, None)

    async def revoke_subscription(self, transaction_id: str, subscription_revoke_request: AdvancedCommerceSubscriptionRevokeRequest) -> AdvancedCommerceSubscriptionRevokeResponse:
        """
        Immediately cancel a customer's subscription and all the items that are included in the subscription, and request a full or prorated refund.

        :param transaction_id: The transaction identifier of the auto-renewable subscription to revoke.
        :param subscription_revoke_request: The request body you provide to terminate a subscription and all its items immediately.
        :return: The response body for a successful revoke-subscription request.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/advancedcommerceapi/revoke-subscription
        """
        return await self._make_request(_path("/advancedCommerce/v1/subscription/revoke/{}", transaction_id), "POST", {}, subscription_revoke_request, AdvancedCommerceSubscriptionRevokeResponse, None)

    async def request_transaction_refund(self, transaction_id: str, request_refund_request: AdvancedCommerceRequestRefundRequest) -> AdvancedCommerceRequestRefundResponse:
        """
        Request a refund for a one-time charge or subscription transaction.

        :param transaction_id: The transaction identifier for which you request a refund.
        :param request_refund_request: The request body for requesting a refund for a transaction.
        :return: The response body for a transaction refund request.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/advancedcommerceapi/request-transaction-refund
        """
        return await self._make_request(_path("/advancedCommerce/v1/transaction/requestRefund/{}", transaction_id), "POST", {}, request_refund_request, AdvancedCommerceRequestRefundResponse, None)

    async def change_subscription_metadata(self, transaction_id: str, subscription_change_metadata_request: AdvancedCommerceSubscriptionChangeMetadataRequest) -> AdvancedCommerceSubscriptionChangeMetadataResponse:
        """
        Update the SKU, display name, and description associated with a subscription, without affecting the subscription's billing or its service.

        :param transaction_id: The transaction identifier of the auto-renewable subscription to get changes to its metadata.
        :param subscription_change_metadata_request: The request body that contains the metadata changes.
        :return: The response body for a successful subscription metadata change.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/advancedcommerceapi/change-subscription-metadata
        """
        return await self._make_request(_path("/advancedCommerce/v1/subscription/changeMetadata/{}", transaction_id), "POST", {}, subscription_change_metadata_request, AdvancedCommerceSubscriptionChangeMetadataResponse, None)

    async def migrate_subscription_to_advanced_commerce_api(self, transaction_id: str, subscription_migrate_request: AdvancedCommerceSubscriptionMigrateRequest) -> AdvancedCommerceSubscriptionMigrateResponse:
        """
        Migrate a subscription that a customer purchased through Apple In-App Purchase to a subscription you manage using the Advanced Commerce API.

        :param transaction_id: The transaction identifier of the auto-renewable subscription to migrate.
        :param subscription_migrate_request: The request body that contains the details for the migration.
        :return: A response that contains signed renewal and transaction information after a subscription successfully migrates to the Advanced Commerce API.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/advancedcommerceapi/migrate-subscription-to-advanced-commerce-api
        """
        return await self._make_request(_path("/advancedCommerce/v1/subscription/migrate/{}", transaction_id), "POST", {}, subscription_migrate_request, AdvancedCommerceSubscriptionMigrateResponse, None)

    async def get_customer_groups(self, any_transaction_id: str) -> GetCustomerGroupsResponse:
        """
        Get the groups that a customer belongs to, and their role in each group.

        :param any_transaction_id: Any originalTransactionId, transactionId, or appTransactionId that belongs to the customer for your app.
        :return: A response that contains the groups a customer belongs to, and their role in each group.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/appstoreserverapi/get-customer-groups
        """
        return await self._make_request(_path("/groups/v1/currentGroups/{}", any_transaction_id), "GET", {}, None, GetCustomerGroupsResponse, None)

    async def get_group_members(self, group_id: str, pagination_token: Optional[str] = None, limit: Optional[int] = None) -> GetGroupMembersResponse:
        """
        Get a paginated list of the customers that belong to a group.

        :param group_id: The identifier of a group in your app, which the Get Customer Groups endpoint returns.
        :param pagination_token: An optional token you use to get the next set of members. Responses that have more members available include a paginationToken. Omit this parameter the first time you call this endpoint.
        :param limit: An optional maximum number of members to return in a single response.
        :return: A response that contains a page of the customers that belong to a group.
        :raises APIException: If a response was returned indicating the request could not be processed
        :see: https://developer.apple.com/documentation/appstoreserverapi/get-group-members
        """
        queryParameters: Dict[str, List[str]] = dict()
        if pagination_token is not None:
            queryParameters["paginationToken"] = [pagination_token]
        if limit is not None:
            queryParameters["limit"] = [str(limit)]

        return await self._make_request(_path("/groups/v1/group/{}", group_id), "GET", queryParameters, None, GetGroupMembersResponse, None)
