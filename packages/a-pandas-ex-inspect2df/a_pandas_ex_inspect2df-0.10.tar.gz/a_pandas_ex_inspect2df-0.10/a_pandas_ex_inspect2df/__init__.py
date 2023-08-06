import inspect
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions

pd_add_apply_ignore_exceptions()
import pandas as pd


def inspect2df(obj):
    r"""
    Convert the attributes of an object into a pandas DataFrame with information about each attribute.

    Args:
        obj: An object to inspect.

    Returns:
        A pandas DataFrame with the following columns:
            - aa_attrb_name: The name of the attribute.
            - aa_signature: The signature of the attribute.
            - aa_attrb: The attribute itself.
            - aa_doc: The docstring of the attribute.
            - aa_annotations: The annotations of the attribute.
            - aa_absfile: The absolute path of the file containing the attribute.
            - aa_closurevars: The closure variables of the attribute.
            - aa_unwrapped: The unwrapped attribute.

    Raises:
        None.
    """
    df = pd.DataFrame(inspect.getmembers(obj))
    df.columns = ["aa_attrb_name", "aa_attrb"]
    df["aa_annotations"] = df["aa_attrb"].ds_apply_ignore(
        pd.NA, lambda x: inspect.get_annotations(x)
    )
    df["aa_unwrapped"] = df["aa_attrb"].ds_apply_ignore(
        pd.NA, lambda x: inspect.unwrap(x)
    )
    df["aa_doc"] = df["aa_attrb"].ds_apply_ignore(pd.NA, lambda x: inspect.getdoc(x))
    df["aa_absfile"] = df["aa_attrb"].ds_apply_ignore(
        pd.NA, lambda x: inspect.getabsfile(x)
    )
    df["aa_signature"] = df["aa_attrb"].ds_apply_ignore(
        pd.NA, lambda x: inspect.signature(x)
    )
    df["aa_closurevars"] = df["aa_attrb"].ds_apply_ignore(
        pd.NA, lambda x: inspect.getclosurevars(x)
    )
    cols = [
        "aa_attrb_name",
        "aa_signature",
        "aa_attrb",
        "aa_doc",
        "aa_annotations",
        "aa_absfile",
        "aa_closurevars",
        "aa_unwrapped",
    ]
    df = df.filter(cols)
    return df


