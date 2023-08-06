from __future__ import annotations

import ast

from .dataclasses import Result
from .utils import get_poskwarg, single_visitor

REMOVED_CLASSES = {
    # Removal of Support For User Accounts
    "CallMessage": "",
    "GroupCall": "",
    "Profile": "",
    "Relationship": "",
    "RelationshipType": "",
    "HypeSquadHouse": "",
    "PremiumType": "",
    "UserContentFilter": "",
    "FriendFlags": "",
    "Theme": "",
    # Major Webhook Changes
    "WebhookAdapter": "",
    "AsyncWebhookAdapter": (
        "this is now considered implementation detail and should not be depended on"
    ),
    "RequestsWebhookAdapter": (
        "this is now considered implementation detail and should not be depended on"
    ),
}
REMOVED_EVENTS = (
    # Removal of Support For User Accounts
    "on_relationship_add",
    "on_relationship_remove",
    "on_relationship_update",
)
REMOVED_METHODS = {
    # Removal of Support For User Accounts
    "fetch_user_profile": ("Client.fetch_user_profile", ""),
    "create_group": ("ClientUser.create_group", ""),
    "edit_settings": ("ClientUser.edit_settings", ""),
    "get_relationship": ("ClientUser.get_relationship", ""),
    "add_recipients": ("GroupChannel.add_recipients", ""),
    "remove_recipients": ("GroupChannel.remove_recipients", ""),
    # avoid false-positives
    #  - it's incredibly unlikely that call to edit() would be a call on GroupChannel
    #
    # "edit": ("GroupChannel.edit", ""),
    "ack": ("Guild/Message.ack", ""),
    "block": ("User.block", ""),
    "is_blocked": ("User.is_blocked", ""),
    "is_friend": ("User.is_friend", ""),
    "profile": ("User.profile", ""),
    "remove_friend": ("User.remove_friend", ""),
    "send_friend_request": ("User.send_friend_request", ""),
    "unblock": ("User.unblock", ""),
    # Major Webhook Changes
    "execute": (
        "Webhook/SyncWebhook.execute",
        "this was an alias, use Webhook/SyncWebhook.send() instead",
    ),
}
REMOVED_ATTRIBUTES = (
    # Removal of Support For User Accounts
    "blocked",
    "email",
    "friends",
    "premium",
    "premium_type",
    "relationships",
    "call",
    "mutual_friends",
    "relationship",
)
REMOVED_METHOD_PARAMETERS = (
    # Removal of Support For User Accounts
    ("Client.login", None, "bot"),
    ("Client.start", None, "bot"),
    ("Client.change_presence", None, "afk"),
    ("ClientUser.edit", None, "password"),
    ("ClientUser.edit", None, "new_password"),
    ("ClientUser.edit", None, "email"),
    ("ClientUser.edit", None, "house"),
)
# datetime Objects Are Now UTC-Aware
DATETIME_ATTRIBUTES = (
    "created_at",
    "edited_at",
    "expires_at",
    "end",
    "joined_at",
    "premium_since",
    "requested_to_speak_at",
    "start",
    "synced_at",
    "timestamp",
    "updated_at",
)
DATETIME_METHOD_PARAMETERS = (
    ("Messageable.history", None, "before"),
    ("Client.history", None, "after"),
    ("Client.history", None, "around"),
    ("Client.fetch_guilds", None, "before"),
    ("Client.fetch_guilds", None, "after"),
    ("Guild.audit_logs", None, "before"),
    ("Guild.audit_logs", None, "after"),
    ("Guild.fetch_members", None, "after"),
    ("TextChannel.purge", None, "before"),
    ("TextChannel.purge", None, "after"),
    ("TextChannel.purge", None, "around"),
    ("sleep_until", 0, "when"),
    ("time_snowflake", 0, "datetime_obj"),
)
DATETIME_CONSTRUCTOR_PARAMETERS = (("Embed", None, "timestamp"),)
EVENTS_WITH_DATETIME = (
    "on_typing",
    "on_private_channel_pins_update",
    "on_guild_channel_pins_update",
)


@single_visitor
def ast_attribute_find_usage(result: Result, node: ast.Attribute) -> None:
    """Handles usage of `var.attr_name`."""
    if node.attr in REMOVED_ATTRIBUTES:
        result.add(node, f"Removed {node.attr} attribute")
        return
    if node.attr in DATETIME_ATTRIBUTES:
        result.add(
            node,
            f"Inspect usage - {node.attr} attribute changed"
            " from naive to aware datetime object",
        )


@single_visitor
def ast_attribute_removed_classes(result: Result, node: ast.Attribute) -> None:
    """Handles usage of `discord.RemovedClass`."""
    assert isinstance(node.value, ast.Name)
    assert node.value.id == "discord"
    try:
        reason = REMOVED_CLASSES[node.attr]
    except KeyError:
        pass
    else:
        if reason:
            reason = f" - {reason}"
        result.add(node, f"Removed {node.attr} class{reason}")


@single_visitor
def ast_name_removed_classes(result: Result, node: ast.Name) -> None:
    """Handles usage of `RemovedClass`."""
    try:
        reason = REMOVED_CLASSES[node.id]
    except KeyError:
        pass
    else:
        if reason:
            reason = f" - {reason}"
        result.add(node, f"Removed {node.id} class{reason}")


@single_visitor
def ast_functiondef_listener_usage(result: Result, node: ast.FunctionDef) -> None:
    """
    Handles `@commands.Cog.listener("event_name")` and all function defs
    that use event name as their name.
    """
    func_name = node.name
    if func_name in REMOVED_EVENTS:
        result.add(node, f"Removed {func_name} event")

    if func_name in EVENTS_WITH_DATETIME:
        result.add(
            node,
            "Inspect usage - type of the datetime object"
            f" in {func_name} event changed from naive to aware",
        )

    for deco in node.decorator_list:
        if not isinstance(deco, ast.Call) or not (
            isinstance(deco.func, ast.Attribute)
            and deco.func.attr == "listener"
            or isinstance(deco.func, ast.Name)
            and deco.func.id == "listener"
        ):
            continue

        arg_value = get_poskwarg(deco, 0, "name")
        if isinstance(arg_value, ast.Constant):
            if arg_value.value in REMOVED_EVENTS:
                result.add(node, f"Removed {arg_value.value} event")
            elif arg_value.value in EVENTS_WITH_DATETIME:
                result.add(
                    node,
                    "Inspect usage - type of the datetime object"
                    f" in {arg_value.value} event changed from naive to aware",
                )


@single_visitor
def ast_functiondef_removed_event(result: Result, node: ast.FunctionDef) -> None:
    """
    Handles `@commands.Cog.listener("removed_event")` and all function defs
    that use event name as their name.
    """
    if node.name in REMOVED_EVENTS:
        result.add(node, f"Removed {node.name} event")

    for deco in node.decorator_list:
        if not isinstance(deco, ast.Call) or not (
            isinstance(deco.func, ast.Attribute)
            and deco.func.attr == "listener"
            or isinstance(deco.func, ast.Name)
            and deco.func.id == "listener"
        ):
            continue

        arg_value = get_poskwarg(deco, 0, "name")
        if isinstance(arg_value, ast.Constant) and arg_value.value in REMOVED_EVENTS:
            result.add(node, f"Removed {arg_value.value} event")


@single_visitor
def ast_call_removed_event(result: Result, node: ast.Call) -> None:
    """Handles `var.add_listener(..., "removed_event")`."""
    assert isinstance(node.func, ast.Attribute)
    assert node.func.attr == "add_listener"
    arg_value = get_poskwarg(node, 1, "name")
    assert isinstance(arg_value, ast.Constant)
    assert arg_value.value in REMOVED_EVENTS
    result.add(node, f"Removed {arg_value.value} event")


@single_visitor
def ast_call_function_usage(result: Result, node: ast.Call) -> None:
    """Handles `var.function_name(...)` (for module access) and `function_name(...)."""
    if isinstance(node.func, ast.Attribute):
        function_name = node.func.attr
    elif isinstance(node.func, ast.Name):
        function_name = node.func.id
    else:
        return

    if function_name == "snowflake_time":
        result.add(
            node,
            "Inspect usage - return type of snowflake_time() changed"
            " from naive to aware datetime object",
        )


@single_visitor
def ast_call_constructor_usage(result: Result, node: ast.Call) -> None:
    """Handles `discord.ClassName(...)` and `ClassName(...)."""
    if isinstance(node.func, ast.Attribute):
        assert isinstance(node.func.value, ast.Name)
        assert node.func.value.id == "discord"
        class_name = node.func.attr
    elif isinstance(node.func, ast.Name):
        class_name = node.func.id
    else:
        return

    for expected_class_name, param_pos, param_name in DATETIME_CONSTRUCTOR_PARAMETERS:
        if class_name != expected_class_name:
            continue
        if get_poskwarg(node, param_pos, param_name) is not None:
            result.add(
                node,
                f"Inspect usage - {class_name}'s timestamp parameter"
                " now assumes local time if naive datetime is passed",
            )


@single_visitor
def ast_call_method_usage(result: Result, node: ast.Call) -> None:
    """Handles `var.method_name(...)`."""
    assert isinstance(node.func, ast.Attribute)
    method_name = node.func.attr

    try:
        full_name, reason = REMOVED_METHODS[method_name]
    except KeyError:
        pass
    else:
        if reason:
            reason = f" - {reason}"
        result.add(node, f"Removed {full_name}() method{reason}")
        return


@single_visitor
def ast_call_method_parameter_usage(result: Result, node: ast.Call) -> None:
    """Handles `var.some_method(removed_param=...)`."""
    assert isinstance(node.func, ast.Attribute)
    for method_path, param_pos, param_name in REMOVED_METHOD_PARAMETERS:
        method_name = method_path.rsplit(".", maxsplit=1)[-1]
        if node.func.attr != method_name:
            continue
        if get_poskwarg(node, param_pos, param_name) is not None:
            result.add(node, f"Removed {param_name} parameter to {method_path}()")

    for method_path, param_pos, param_name in DATETIME_METHOD_PARAMETERS:
        method_name = method_path.rsplit(".", maxsplit=1)[-1]
        if node.func.attr != method_name:
            continue
        if get_poskwarg(node, param_pos, param_name) is not None:
            result.add(
                node,
                f"Inspect usage - {param_name} parameter to {method_path}()"
                " now assumes local time if naive datetime is passed",
            )


class RemovalVisitor(ast.NodeVisitor):
    def __init__(self, result: Result) -> None:
        self.result = result

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        ast_functiondef_listener_usage(self.result, node)
        ast_functiondef_removed_event(self.result, node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        ast_attribute_removed_classes(self.result, node)
        ast_attribute_find_usage(self.result, node)

    def visit_Name(self, node: ast.Name) -> None:
        ast_name_removed_classes(self.result, node)

    def visit_Call(self, node: ast.Call) -> None:
        ast_call_removed_event(self.result, node)
        ast_call_function_usage(self.result, node)
        ast_call_constructor_usage(self.result, node)
        ast_call_method_usage(self.result, node)
        ast_call_method_parameter_usage(self.result, node)


def visit(result: Result) -> None:
    visitor = RemovalVisitor(result)
    with result.current_file.path.open(encoding="utf-8") as fp:
        visitor.visit(ast.parse(fp.read()))
