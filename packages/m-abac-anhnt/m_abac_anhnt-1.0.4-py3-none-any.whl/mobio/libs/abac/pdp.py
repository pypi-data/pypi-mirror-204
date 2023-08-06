"""
    Policy decision point implementation
"""

from copy import deepcopy

from .call_api import CallAPI
from .policy import PolicySchema, AccessType
from .policy.utils import Utils
from .result_access import ResultAccess


class PolicyDecisionPoint(object):
    """
        Policy decision point
    """

    class AccountType:
        SYSTEM = "system"
        NORMAL = "normal"

    class AccessLevel:
        LIST = "list"
        READ = "read"
        ADD = "add"
        EDIT = "edit"
        DELETE = "delete"
        OTHER = "other"

    def __init__(self,
                 merchant_id, resource: str, action: str, account_id: str = None, user_info: dict = None,
                 request_access: dict = None, environment: dict = None, account_type=AccountType.NORMAL):
        if not merchant_id:
            raise ValueError("merchant_id required")
        if not resource:
            raise ValueError("resource required")
        if not action:
            raise ValueError("action required")

        if account_type == PolicyDecisionPoint.AccountType.NORMAL:
            if not account_id:
                raise ValueError("account normal account_id required")
            if not user_info:
                user_info = CallAPI.admin_get_account_info(merchant_id, account_id)

        self.account_type = account_type
        self.merchant_id = merchant_id
        self.account_id = account_id
        self.resource = resource
        self.action = action
        self.request_access = request_access if request_access else {}
        self.result_access = ResultAccess()
        self.request_access.update({
            "user": user_info if user_info else {},
            "env": self.get_info_environment(environment)
        })

    def get_policy_statement_for_target(self):
        return CallAPI.admin_get_list_statement(self.merchant_id, self.account_id, self.resource, self.action)

    def is_allowed(self):
        """
            Check if authorization request is allowed

            :param request: request object
            :return: True if authorized else False
        """
        try:
            if self.account_type == PolicyDecisionPoint.AccountType.SYSTEM:
                self.result_access.set_allow_access(True)
                return self.result_access
            list_statement = self.get_policy_statement_for_target()
            if list_statement:
                action_info = CallAPI.admin_get_json_action(merchant_id=self.merchant_id)
                if not action_info:
                    raise ValueError("action for merchant_id {} not found".format(self.merchant_id))
                if not action_info.get(self.action):
                    raise ValueError("action {} not found".format(self.action))
                access_level = action_info.get(self.action, {}).get("access_level").lower()

                statement_check_allow, statement_check_deny = self.get_statement_by_type(list_statement, access_level)
                if statement_check_deny:
                    if self.check_list_statement_is_deny(statement_check_deny):
                        self.result_access.set_allow_access(False)
                        return self.result_access
                if statement_check_allow:
                    self.result_access.set_allow_access(self.check_list_statement_is_allow(statement_check_allow))
                else:
                    self.result_access.set_allow_access(False)
            else:
                self.result_access.set_allow_access(False)
        except Exception as err:
            print("Exception: {}".format(err))
            self.result_access.set_allow_access(False)

        return self.result_access

    def get_info_environment(self, environment):
        if not environment:
            environment = Utils.get_info_from_header_request()
            if environment:
                if environment.get("env:user_agent"):
                    environment.update(Utils.parse_user_agent(environment.get("env:user_agent")))
        environment = environment if environment else {}
        environment.update({"env:current_time": Utils.get_date_utcnow()})
        return environment

    def check_access_level_action(self, statement, access_level):
        """
                # list_statement_level = self.get_statement_by_level(list_statement)
                # for statement_level in list_statement_level:
                #     next_statement = True
                #     for statement in statement_level:
                #         next_statement = self.check_access_level_action(statement=statement, access_level=access_level)
                #         if not next_statement:
                #             break
                #     if not next_statement:
                #         break
            kiểm tra các từng statement, condition thỏa mãn thì lấy thông tin bộ lọc hoặc hiển thị field nếu có
        :param statement:
        :return:
        """
        next_statement = True

        statement_copy = deepcopy(statement)
        condition_check = []
        condition_filter = []
        display_field = {}
        if access_level == "list":
            for item_cond in statement_copy.get("condition"):
                if item_cond.get("field").startswith("user") or item_cond.get("field").startswith("env"):
                    condition_check.append(item_cond)
                else:
                    values = [self.get_value_from_variable(i) for i in item_cond.get("values")]
                    item_cond["values"] = values
                    condition_filter.append(item_cond)
        else:
            condition_filter = statement_copy.get("condition")
        if access_level in ["list", "read"]:
            if statement_copy.get("fields"):
                display_field.update({
                    "effect": statement_copy.get("effect"),
                    "fields": statement_copy.get("fields"),
                })
        statement_allow = False
        if condition_check:
            statement_check = {**statement_copy}
            statement_check["condition"] = condition_check
            statement_check["request_access"] = self.request_access
            policy_schema = PolicySchema().load(statement_check)
            if policy_schema.is_allowed():
                statement_allow = True
                if policy_schema.get("effect") == AccessType.ALLOW_ACCESS:
                    next_statement = True
                    self.result_access.set_allow_access(True)
                else:
                    next_statement = False
                    self.result_access.set_allow_access(False)
        else:
            next_statement = True
            statement_allow = True
            self.result_access.set_allow_access(True)
        if statement_allow:
            if condition_filter:
                statement_filter = {"effect": statement_copy.get("effect"), "condition": condition_filter}
                self.result_access.add_filter_config(statement_filter)
            if display_field:
                self.result_access.add_display_config(display_field)
        return next_statement

    def get_value_from_variable(self, str_variable):
        variables = Utils.get_field_key_from_variable(str_variable)
        if variables:
            if len(variables) == 1 and Utils.check_field_is_variable(variables[0]):
                field_value = self.get_value_from_field(variables[0])
                return field_value
            for field_key in variables:
                field_value = self.get_value_from_field(field_key)
                if field_value is not None:
                    field_value = str(field_value)
                    str_variable = Utils.replace_variable_to_value(field_key, field_value, str_variable)
        return str_variable

    def get_value_from_field(self, field_key):
        resource_name, resource_key = Utils.split_delemiter_resource(field_key)
        if resource_name and resource_key:
            if self.request_access.get(resource_name) and isinstance(self.request_access.get(resource_name), dict):
                data_resource = self.request_access.get(resource_name)
                value = Utils.get_nested_value(data_resource, resource_key)
                return value
        return None

    def get_statement_by_level(self, list_statement: list):
        statement_deny = []
        statement_allow = []
        for item in list_statement:
            if item.get("effect") == AccessType.DENY_ACCESS:
                statement_deny.append(item)
            else:
                statement_allow.append(item)
        return [statement_deny, statement_allow]

    def get_statement_by_type(self, list_statement: list, access_level: str):
        statement_check_allow, statement_check_deny = [], []
        for statement in list_statement:
            statement_copy = deepcopy(statement)
            fields = {}
            for item_resource in statement_copy.get("resource"):
                data_fields = Utils.get_fields_of_resource(item_resource)
                if data_fields and self.resource in data_fields:
                    fields.update(data_fields)
            if fields:
                statement_copy["fields"] = fields
            if access_level == PolicyDecisionPoint.AccessLevel.LIST:
                condition_check = []
                condition_filter = []
                for item_cond in statement_copy.get("condition"):
                    if item_cond.get("field").startswith("user") or item_cond.get("field").startswith("env"):
                        condition_check.append(item_cond)
                    else:
                        values = [self.get_value_from_variable(i) for i in item_cond.get("values")]
                        item_cond["values"] = values
                        condition_filter.append(item_cond)
                if statement_copy.get("effect") == AccessType.ALLOW_ACCESS:
                    statement_check_allow.append({
                        **statement_copy,
                        "condition": condition_check
                    })
                else:
                    statement_check_deny.append({
                        **statement_copy,
                        "condition": condition_check
                    })
                if condition_filter:
                    self.result_access.add_filter_config(
                        {"effect": statement_copy.get("effect"), "condition": condition_filter})
            elif access_level == PolicyDecisionPoint.AccessLevel.READ:
                if statement_copy.get("effect") == AccessType.ALLOW_ACCESS:
                    statement_check_allow.append(statement_copy)
                else:
                    statement_check_deny.append(statement_copy)
                if statement_copy.get("fields"):
                    self.result_access.add_display_config({
                        "effect": statement_copy.get("effect"),
                        "fields": statement_copy.get("fields"),
                    })
            else:
                if fields:
                    statement_copy["check_field"] = 1
                if statement_copy.get("effect") == AccessType.ALLOW_ACCESS:
                    statement_check_allow.append(statement_copy)
                else:
                    statement_check_deny.append(statement_copy)
        return statement_check_allow, statement_check_deny

    def check_list_statement_is_deny(self, list_statement: list):
        result_deny = False
        try:
            for statement in list_statement:
                if statement.get("check_field") and statement.get("fields"):
                    if not Utils.field_in_body_request(statement.get("fields").get(self.resource),
                                                       self.request_access.get(self.resource)):
                        continue
                statement["request_access"] = self.request_access
                policy_schema = PolicySchema().load(statement)
                if policy_schema.is_allowed():
                    result_deny = True
                    break
        except Exception as err:
            print("check_list_statement_is_deny err: {}".format(err))
            result_deny = False
        return result_deny

    def check_list_statement_is_allow(self, list_statement: list):
        result_allow = True
        try:
            for statement in list_statement:
                # đối với action là edit create mà resource liên quan đến field thì kiểm tra field có trong body yêu cầu truy cập hay ko. nếu ko có thì bỏ qua statement
                if statement.get("check_field") and statement.get("fields"):
                    if not Utils.field_in_body_request(statement.get("fields").get(self.resource),
                                                       self.request_access.get(self.resource)):
                        continue
                statement["request_access"] = self.request_access
                policy_schema = PolicySchema().load(statement)
                if not policy_schema.is_allowed():
                    result_allow = False
                    break
        except Exception as err:
            print("check_list_statement_is_allow err: {}".format(err))
            result_allow = False
        return result_allow
