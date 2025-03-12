from enum import Enum


class LocaleKey(str, Enum):
    already_in_queue = "already_in_queue"
    empty = "empty"
    head_ntf = "head_ntf"
    help_info_reg = "help_info_regul"
    help_info_admin = "help_info_admin" 
    help_info_footer = "help_info_footer"
    invalid_callback = "invalid_callback_data"
    new_position_ntf = "new_position_ntf"
    new_queue = "new_queue"
    new_queue_err = "new_queue_err"
    no_queue = "no_queue"
    not_admin_alert = "not_admin_alert"
    queue_404 = "queue_404"
    queue_cleared = "queue_cleared"
    queue_list_header = "queue_list_header"
    quit_button = "quit_button"
    user_404 = "user_404"
    user_not_in_queue = "user_not_in_queue"
    user_removed = "user_removed"