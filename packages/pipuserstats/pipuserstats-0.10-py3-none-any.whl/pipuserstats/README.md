# PyPi download statistics for several packages or for all packages from a user

## pip install pipuserstats



```python
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
	Exception: If an error occurs while retrieving statistics for a package.





from pipuserstats import get_user_pip_stats

df = get_user_pip_stats(
    username_or_packages="hansalemao", sleeptime=1, clear_cache=False
)
print(df)
"""
# -1 means "no data available"
                             total  2023-04-20  ...  2022-10-23  2022-10-22
a-cv-imwrite-imread-plus      3593          31  ...          -1          -1
a-cv-sift-detection            244          -1  ...          -1          -1
a-cv2-calculate-difference     279           2  ...          -1          -1
a-cv2-calculate-simlilarity    339           2  ...          -1          -1
a-cv2-easy-resize             2223          24  ...          -1          -1
                            ...         ...  ...         ...         ...
"""

df = get_user_pip_stats(
    username_or_packages=["pandas", "numpy"], sleeptime=0.5, clear_cache=False
)

"""
df
Out[4]: 
            total  2023-04-20  2023-04-19  ...  2022-10-24  2022-10-23  2022-10-22
pandas  639313100     4258267     4265098  ...     3721798     2540678     2738365
numpy   843036266     5667169     5747109  ...     4882242     3261557     3556995
[2 rows x 181 columns]
"""
	
"""

```