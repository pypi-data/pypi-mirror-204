import difflib
import os
from typing import Union

import pandas as pd
import regex
from flatten_everything import flatten_everything
from a_pandas_ex_bs4df_lite import pd_add_bs4_to_df_lite
pd_add_bs4_to_df_lite()



def open_text(text, encoding):
    text1 = text
    if isinstance(text1, str):
        if os.path.exists(text1):
            with open(text1, mode="rb") as f:
                text1 = f.read()
    if isinstance(text1, bytes):
        text1 = text1.decode(encoding, "ignore")
    if not isinstance(text1, list):
        text1 = text1.splitlines()
    return text1


def get_text_difference(
    text1: Union[str, list, bytes],
    text2: Union[str, list, bytes],
    encoding: str = "utf-8",
) -> pd.DataFrame:
    def get_details(x, lookinfor="diff_add"):
        try:
            if x[0] == lookinfor:
                return x[1]
            else:
                return pd.NA
        except Exception:
            return pd.NA

    text1 = open_text(text1, encoding)
    text2 = open_text(text2, encoding)

    htmla = difflib.HtmlDiff().make_file(text2, text1)
    df = pd.Q_bs4_to_df_lite(htmla.encode(), parser="lxml")
    now = (
        pd.DataFrame(
            [
                [y for y in x if '<td nowrap="nowrap">' in str(y)]
                for x in df.loc[df.aa_name == "tr"].aa_contents
                if "diff_" in str(x)
            ]
        )
        .dropna(how="all")
        .reset_index(drop=True)
    )
    now[2] = now[0].apply(lambda x: x.find_all("span"))
    now[3] = now[1].apply(lambda x: x.find_all("span"))
    now["aa_diff"] = now[3].apply(
        lambda x: tuple(
            (
                tuple(
                    flatten_everything(
                        [y.attrs.get("class"), y.text.replace("\xa0", " ")]
                    )
                )
            )
            if y
            else []
            for y in x
        )
    )
    now["bb_diff"] = now[2].apply(
        lambda x: tuple(
            (
                tuple(
                    flatten_everything(
                        [y.attrs.get("class"), y.text.replace("\xa0", " ")]
                    )
                )
            )
            if y
            else []
            for y in x
        )
    )
    now["aa_text"] = now[0].apply(lambda x: x.text)
    now["bb_text"] = now[1].apply(lambda x: x.text)
    now["aa_parts"] = now[0].apply(
        lambda x: tuple(
            [
                tra
                for tra in regex.split("<[^><]*>", str(x).replace("\xa0", " "))
                if tra != ""
            ]
        )
    )
    now["bb_parts"] = now[1].apply(
        lambda x: tuple(
            [
                tra
                for tra in regex.split("<[^><]*>", str(x).replace("\xa0", " "))
                if tra != ""
            ]
        )
    )
    now["no"] = range(len(now))
    nowdf = (
        now.drop(columns=[0, 1, 2, 3])
        .reset_index(drop=True)
        .explode("bb_diff")
        .explode("aa_diff")
        .reset_index(drop=True)
        .copy()
    )

    nowdf["aa_added"] = nowdf.aa_diff.apply(lambda x: get_details(x, "diff_add"))
    nowdf["aa_changed"] = nowdf.aa_diff.apply(lambda x: get_details(x, "diff_chg"))
    nowdf["aa_substracted"] = nowdf.aa_diff.apply(lambda x: get_details(x, "diff_sub"))
    nowdf["bb_added"] = nowdf.bb_diff.apply(lambda x: get_details(x, "diff_add"))
    nowdf["bb_changed"] = nowdf.bb_diff.apply(lambda x: get_details(x, "diff_chg"))
    nowdf["bb_substracted"] = nowdf.bb_diff.apply(lambda x: get_details(x, "diff_sub"))
    colas = [
        "no",
        "aa_text",
        "bb_text",
        "aa_added",
        "bb_added",
        "aa_substracted",
        "bb_substracted",
        "aa_changed",
        "bb_changed",
        "aa_diff",
        "bb_diff",
        "aa_parts",
        "bb_parts",
    ]
    nowdf = nowdf.filter(colas)
    nowdf = nowdf.drop(columns=["bb_added", "aa_substracted"]).copy()
    nowdf.aa_text = nowdf.aa_text.str.replace(" ", " ", regex=False)
    nowdf.bb_text = nowdf.bb_text.str.replace(" ", " ", regex=False)
    return nowdf.copy()


def pd_add_text_difference():
    pd.Q_text_difference_to_df = get_text_difference



