from enum import Enum

class StaticDataHeaders(Enum):
    default_header = "default_header"
    no_content_header = "no_content_header"
    no_accept_header = "no_accept_header"
    no_token_header = "no_token_header"
    invalid_token_header = "invalid_token_header"