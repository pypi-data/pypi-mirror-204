import os
import pandas as pd
import bs4
import pypistats
from pathlib import Path
from cprinter import TC
import requests
from platformdirs import user_cache_dir
from list_all_files_recursively import get_folder_file_complete_path
from time import sleep


def get_packages_from_user(username):
    with requests.get(f'https://pypi.org/user/{username.strip("/ ")}/') as res:
        data = res.content
    allpa = list(
        sorted([q.text for q in bs4.BeautifulSoup(data, "lxml").find_all("h3")])
    )
    allpa = sorted(allpa, key=lambda x: x[0].lower())
    return allpa


def get_user_pip_stats(
    username_or_packages: str | tuple | list,
    sleeptime: float | int = 1.0,
    clear_cache: bool = False,
) -> pd.DataFrame:
    """
    Retrieves download statistics for a given user or package(s) from PyPI Stats API.

    Args:
        username_or_packages (str | tuple | list): The username or package(s) to retrieve statistics for.
        If a string is passed,  username_or_packages will be treated as a username. If a list/tuple is passed,
        username_or_packages will be treated as packages.
        sleeptime (float | int, optional): The time to sleep between API requests. Defaults to 1.0.
        clear_cache (bool, optional): Whether to clear the PyPI Stats API cache before retrieving statistics.
            Defaults to False.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the download statistics for the given user or package(s).

    Raises:
        Exception: If an error occurs while retrieving statistics for a package."""
    if clear_cache:
        CACHE_DIR = Path(user_cache_dir("pypistats"))
        for ax in get_folder_file_complete_path(str(CACHE_DIR)):
            try:
                print(f"Deleting: {ax.path}")
                os.remove(ax.path)
            except Exception:
                continue
    if isinstance(username_or_packages, str):
        allpa = get_packages_from_user(username_or_packages)
    else:
        allpa = username_or_packages
    dfall = []
    for i in allpa:
        try:
            df = pypistats.overall(i, total=True, format="pandas")

            df = (
                df.loc[df.category == "without_mirrors"]
                .sort_values(by="date", ascending=False)
                .drop(columns="category")
                .reset_index(drop=True)
            )
            dfall.append(
                df.drop(columns="percent")
                .set_index("date")
                .rename(columns={"downloads": i})
                .copy()
            )
            print(TC(f"{i}").fg_green.bg_black)
        except Exception as fe:
            print(TC(f"{i}").fg_red.bg_black)
        sleep(sleeptime)

    dffinal = pd.concat(dfall, axis=1).T.fillna(-1)
    dffinal = dffinal.convert_dtypes("Int64")
    dffinal = pd.concat([dffinal.T.replace(-1, 0).sum(), dffinal], axis=1).rename(
        columns={0: "total"}
    )
    return dffinal
