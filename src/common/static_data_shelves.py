from enum import Enum

class StaticDataProject(Enum):
    valid_limit_param = "?limit=100&offset=0"
    invalid_url_param = "ss?limit=100&offset=0"
    invalid_limit1_param0 = "?limit=1&offset=0"
    invalid_limit0_param0 = "?limit=0&offset=0"
    invalid_limit_abc_param0 = "?limit=abc&offset=0"
    valid_limit5_param10 = "?limit=5&offset=10"
    invalid_limit10_param_1 = "?limit=10&offset=-1"
    invalid_limit101_param0 = "?limit=101&offset=0"
    invalid_limit_1_param0 = "?limit=-1&offset=0"
    invalid_limit5_param9999999 = "?limit=5&offset=9999999"

    valid_project_default = ""
    invalid_url_suffix_project = "/INVALID_PROJECT"


class StaticDataShelvesPorId(Enum):
    valid_id = "6"
    valid_param_id = "99"
    invalid_no_exist_id = "9999999"
    invalid_id_null = " "
    invalid_code_param_special = "%$#^@"
    invalid_id_param_string = "Cas"
    invalid_id_param_minus = "gbo"
    invalid_id_param_mayus = "GBO"
    invalid_id_param_mix = "12GB"
    invalid_id_param_cero = "0"
    invalid_id_param_more_cero = "00000"
    invalid_id_param_negative = "-3"
    invalid_id_param_space= " 1"


class StaticDataProjectDeletePorCode(Enum):
    invalid_code_param_delete = ""
    invalid_code_param_delete_1 = "/A"
    invalid_code_param_delete_10 = "/Aabbccddeeff"
    invalid_code_param_delete_no = "Abejita"
    invalid_code_param_delete_spacial = "%#$^@"
    invalid_code_param_delete_number = "12345"
    invalid_code_param_delete_space = "CA SA"
    invalid_code_param_delete_none = None
    invalid_code_param_delete_decimal = "123,12"