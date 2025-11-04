
def get_url_parametrized(base_url, module, code=None):

    if code:
        return f"{base_url}/{module}/{code}"
    else:
        return f"{base_url}/{module}"

def case_patch_join(modulo, id):
    return f"{modulo}/{id}"



