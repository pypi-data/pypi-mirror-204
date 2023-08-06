from .gris import tag2string, missing_data

def get_pubyear(ref):
    """Return the publication year"""
    py = tag2string(ref, 'PY')
    if py == missing_data:
        py = tag2string(ref, 'C6')
        if py != missing_data:
            py = py.split()[1]
    return py

