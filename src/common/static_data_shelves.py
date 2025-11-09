from enum import Enum

class StaticDataShelvesPorId(Enum):
    valid_id = "6"
    valid_param_id = "99"
    invalid_no_exist_id = "9999999"
    invalid_id_null = " "
    invalid_id_param_space_medium = "178 7"
    invalid_code_param_special = "%$#^@"
    invalid_id_param_string = "Cas"
    invalid_id_param_minus = "gbo"
    invalid_id_param_mayus = "GBO"
    invalid_id_param_mix = "12GB"
    invalid_id_param_cero = "0"
    invalid_id_param_more_cero = "00000"
    invalid_id_param_negative = "-3"
    invalid_id_param_space= " 1"
