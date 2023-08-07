import re
import warnings
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import pandas as pd
import polars as pl
from sklearn.preprocessing import FunctionTransformer

from sk_transformers.base_transformer import BaseTransformer
from sk_transformers.utils import check_ready_to_transform


class ColumnEvalTransformer(BaseTransformer):
    """Provides the possibility to use Pandas methods on columns. Internally
    this transformer uses Polars. You may encounter issues with your
    implementation. Please check the Polars documentation for more information:
    https://pola-rs.github.io/polars/py-polars/html/reference/

    Example:
    ```python
    import pandas as pd
    from sk_transformers import ColumnEvalTransformer

    # In this example we use Polars implementation of Pandas `str.upper()`: `str.to_uppercase()`.

    X = pd.DataFrame({"foo": ["a", "b", "c"], "bar": [1, 2, 3]})
    transformer = ColumnEvalTransformer(
        [("foo", "str.to_uppercase()"), ("bar", "apply(lambda x: x + 1)")]
    )
    transformer.fit_transform(X)
    ```
    ```
       foo  bar
    0    A    2
    1    B    3
    2    C    4
    ```

    Args:
        features (List[Union[Tuple[str, str], Tuple[str, str, str]]]): List of tuples containing the column name and the method (`eval_func`) to apply.
            As a third entry in the tuple an alternative name for the column can be provided. If not provided the column name will be used.
            This can be useful if the the original column should not be replaced but another column should be created.

    Raises:
        ValueError: If the `eval_func` starts with a dot (`.`).
        ValueError: If the `eval_func` tries to assign multiple columns to one target column.
    """

    __slots__ = ("features",)

    def __init__(
        self, features: List[Union[Tuple[str, str], Tuple[str, str, str]]]
    ) -> None:
        super().__init__()  # pylint: disable=duplicate-code
        self.features = features

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform the dataframe by using the `eval` function provided.

        Args:
            X (pandas.DataFrame): dataframe to transform.
        Returns:
            pandas.DataFrame: Transformed dataframe.
        """
        X = check_ready_to_transform(
            self,
            X,
            [feature[0] for feature in self.features],
            force_all_finite="allow-nan",
            return_polars=True,
        )

        for eval_tuple in self.features:
            column = eval_tuple[0]
            eval_func = eval_tuple[1]
            new_column = eval_tuple[2] if len(eval_tuple) == 3 else column  # type: ignore # pylint: disable=unused-variable

            if eval_func[0] == ".":
                raise ValueError(
                    "The provided `eval_func` must not start with a dot! Just write e.g. `str.len()` instead of `.str.len()`."
                )

            try:
                X = X.with_columns(
                    eval(  # pylint: disable=eval-used # nosec
                        f"pl.col({'column'}).{eval_func}.alias({'new_column'})"
                    )
                )
            except AttributeError as error:
                raise AttributeError(
                    f"""Internally this transformer uses Polars. You may encounter issues with your implementation.
                    Please check the Polars documentation for more information:
                    https://pola-rs.github.io/polars/py-polars/html/reference/
                    Original error: {error}"""
                ) from error

        return X.to_pandas()


class DtypeTransformer(BaseTransformer):
    """Transformer that converts a column to a different dtype.

    Example:
    ```python
    import numpy as np
    import pandas as pd
    from sk_transformers import DtypeTransformer

    X = pd.DataFrame({"foo": [1, 2, 3], "bar": ["a", "a", "b"]})
    transformer = DtypeTransformer([("foo", np.float32), ("bar", "category")])
    transformer.fit_transform(X).dtypes
    ```
    ```
    foo     float32
    bar    category
    dtype: object
    ```

    Args:
        features (List[Tuple[str, Union[str, type]]]): List of tuples containing the column name and the dtype (`str` or `type`).
    """

    def __init__(self, features: List[Tuple[str, Union[str, type]]]) -> None:
        super().__init__()
        self.features = features

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform the dataframe by converting the columns to the specified
        dtypes.

        Args:
            X (pandas.DataFrame): dataframe to transform.

        Returns:
            pandas.DataFrame: Transformed dataframe.
        """
        X = check_ready_to_transform(
            self,
            X,
            [feature[0] for feature in self.features],
            force_all_finite="allow-nan",
        )

        for column, dtype in self.features:
            X[column] = X[column].astype(dtype)
        return X


class AggregateTransformer(BaseTransformer):
    """This transformer uses Pandas `groupby` method and `aggregate` to apply
    function on a column grouped by another column. Read more about Pandas
    `aggregate` method to understand how to use function for aggregation. Other
    than Pandas function this transformer only support functions and string-
    names.

    Internally this transformer uses Polars. You may encounter issues with your implementation.
    Please check the Polars documentation for more information:
    https://pola-rs.github.io/polars/py-polars/html/reference/

    Example:
    ```python
    import pandas as pd
    from sk_transformers import AggregateTransformer

    X = pd.DataFrame(
        {
            "foo": ["mr", "mr", "ms", "ms", "ms", "mr", "mr", "mr", "mr", "ms"],
            "bar": [46, 32, 78, 48, 93, 68, 53, 38, 76, 56],
        }
    )

    transformer = AggregateTransformer([("foo", ("bar", "mean", "MEAN(foo_bar)"))])
    transformer.fit_transform(X)
    ```
    ```
      foo  bar  MEAN(foo_bar)
    0  mr   46       52.166668
    1  mr   32       52.166668
    2  ms   78       68.750000
    3  ms   48       68.750000
    4  ms   93       68.750000
    5  mr   68       52.166668
    6  mr   53       52.166668
    7  mr   38       52.166668
    8  mr   76       52.166668
    9  ms   56       68.750000
    ```

    Args:
        features (List[Tuple[str, Tuple[str, Union[str, Callable], str]]]): List of tuples where
            the first element is the name or the list of names of columns to be grouped-by,
            and the second element is a tuple or list of tuples containing the aggregation information.
            In this tuple, the first element is the name of the column to be aggregated,
            the second element is the aggregation function as a string or function object,
            and the third element is the name of the new aggregated column.
    """

    def __init__(
        self,
        features: List[
            Tuple[
                Union[str, List[str]],
                Union[
                    Tuple[str, Union[str, Callable], str],
                    List[Tuple[str, Union[str, Callable], str]],
                ],
            ]
        ],
    ) -> None:
        super().__init__()
        self.features = features

    def __get_list_of_features(self) -> List[str]:
        feature_list = []

        for groupby_columns, agg_features in self.features:
            if isinstance(groupby_columns, str):
                groupby_columns = [groupby_columns]
            for groupby_column in groupby_columns:
                feature_list.append(groupby_column)

            if isinstance(agg_features, tuple):
                agg_features = [agg_features]
            for agg_column, _, _ in agg_features:
                feature_list.append(agg_column)

        return list(set(feature_list))

    def __check_input(self) -> None:
        for feature in self.features:
            if len(feature) != 2:
                raise IndexError(
                    f"Expected 2 elements in the feature tuple, got {len(feature)}."
                )

            agg_features = feature[1]

            if isinstance(agg_features, tuple):
                agg_features = [agg_features]
            if isinstance(agg_features, list):
                for agg_feature in agg_features:
                    if isinstance(agg_feature, tuple):
                        if len(agg_feature) != 3:
                            raise IndexError(
                                f"Expected 3 elements in the aggregation tuple, got {len(agg_feature)}."
                            )
                    else:
                        raise TypeError(
                            f"Expected a list of tuples, found {type(agg_feature).__name__} in list."
                        )

                    func = agg_feature[1]
                    if isinstance(func, str) is False:
                        func = func.__name__  # type: ignore
                    if func == "<lambda>":
                        warnings.warn(
                            """
                        Internally this transformer uses Polars. You may encounter issues with your lambda implementation.
                        Please check the documentation for correct syntax and functionality:
                        https://pola-rs.github.io/polars-book/user-guide/dsl/custom_functions.html
                        """,
                            SyntaxWarning,
                        )

            else:
                raise TypeError(
                    f"Expected a list or tuple of aggregations, got {type(agg_features).__name__}."
                )

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Creates new columns by using Pandas `groupby` method and `aggregate`
        to apply function on the column.

        Args:
            X (pd.DataFrame): Input dataframe.

        Returns:
            pd.DataFrame: Transformed dataframe. It contains the original columns and the new columns created by this transformer.
        """
        self.__check_input()
        X = check_ready_to_transform(
            self,
            X,
            self.__get_list_of_features(),
            return_polars=True,
        )

        for groupby_columns, agg_features in self.features:
            if isinstance(agg_features, tuple):
                agg_features = [agg_features]

            agg_df = X.groupby(groupby_columns).agg(
                [
                    getattr(pl, agg_func)(agg_column).alias(agg_new_column)
                    if isinstance(agg_func, str)
                    else pl.col(agg_column).apply(agg_func).alias(agg_new_column)
                    for (agg_column, agg_func, agg_new_column) in agg_features
                ]
            )
            X = X.join(agg_df, on=groupby_columns)

        return X.to_pandas()


class FunctionsTransformer(BaseTransformer):
    """This transformer is a plain wrapper around the.

    [`sklearn.preprocessing.FunctionTransformer`](https://scikit-learn.org/stab
    le/modules/generated/sklearn.preprocessing.FunctionTransformer.html). Its
    main function is to apply multiple functions to different columns. Other
    than the scikit-learn transformer, this transformer *does not* support the
    `inverse_func`, `accept_sparse`, `feature_names_out` and, `inv_kw_args`
    parameters.

    Example:
    ```python
    import numpy as np
    import pandas as pd
    from sk_transformers import FunctionsTransformer

    X = pd.DataFrame({"foo": [1, 2, 3], "bar": [4, 5, 6]})
    transformer = FunctionsTransformer([("foo", np.log1p, None), ("bar", np.sqrt, None)])
    transformer.fit_transform(X)
    ```
    ```
            foo       bar
    0  0.693147  2.000000
    1  1.098612  2.236068
    2  1.386294  2.449490
    ```

    Args:
        features (List[str, Callable, Optional[Dict[str, Any]]]): List of tuples containing the name of the
            column to apply the function on and the function itself.
            As well as a dictionary passed to the function as `kwargs`.
    """

    def __init__(
        self, features: List[Tuple[str, Callable, Optional[Dict[str, Any]]]]
    ) -> None:
        super().__init__()
        self.features = features

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Applies the functions to the columns, and returns the dataframe with
        the modified columns.

        Args:
            X (pandas.DataFrame): DataFrame containing the columns to apply the functions on.

        Returns:
            pandas.DataFrame: The original dataframe with the modified columns.
        """
        X = check_ready_to_transform(self, X, [feature[0] for feature in self.features])

        for column, func, kwargs in self.features:
            X[column] = FunctionTransformer(
                func, validate=True, kw_args=kwargs
            ).transform(X[[column]].to_numpy())

        return X


class MapTransformer(BaseTransformer):
    """This transformer iterates over all columns in the `features` list and
    applies the given callback to the column.

    Internally this transformer uses Polars. You may encounter issues with your implementation.
    Please check the Polars documentation for more information:
    https://pola-rs.github.io/polars/py-polars/html/reference/

    Example:
    ```python
    import pandas as pd
    from sk_transformers import MapTransformer

    X = pd.DataFrame({"foo": [1, 2, 3], "bar": [4, 5, 6]})
    transformer = MapTransformer([("foo", lambda x: x + 1)])
    transformer.fit_transform(X)
    ```
    ```
       foo  bar
    0    2    4
    1    3    5
    2    4    6
    ```

    Args:
        features (List[Tuple[str, Callable]]): List of tuples containing the name of the
            column to apply the callback on and the callback itself.
    """

    def __init__(self, features: List[Tuple[str, Callable]]) -> None:
        super().__init__()
        self.features = features

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Applies the callback to the column.

        Args:
            X (pandas.DataFrame): Dataframe containing the the columns to apply the callback on.

        Returns:
            pandas.DataFrame: The dataframe containing
                the new column together with the non-transformed original columns.
        """
        for _, func in self.features:
            if isinstance(func, str) is False:
                func = func.__name__  # type: ignore
            if func == "<lambda>":  # type: ignore
                warnings.warn(
                    """
                        Internally this transformer uses Polars. You may encounter issues with your lambda implementations.
                        Please check the documentation for correct syntax and functionality:
                        https://pola-rs.github.io/polars-book/user-guide/dsl/custom_functions.html
                        """,
                    SyntaxWarning,
                )

        X = check_ready_to_transform(
            self, X, [feature[0] for feature in self.features], return_polars=True
        )

        return X.with_columns(
            [pl.col(column).map(callback) for column, callback in self.features]
        ).to_pandas()


class ColumnDropperTransformer(BaseTransformer):
    """Drops columns from a dataframe using Pandas `drop` method.

    Example:
    ```python
    import pandas as pd
    from sk_transformers import ColumnDropperTransformer

    X = pd.DataFrame({"foo": [1, 2, 3], "bar": [4, 5, 6]})
    transformer = ColumnDropperTransformer(["foo"])
    transformer.fit_transform(X)
    ```
    ```
       bar
    0    4
    1    5
    2    6
    ```

    Args:
        columns (Union[str, List[str]]): Columns to drop. Either a single column name or a list of column names.
    """

    def __init__(self, columns: Union[str, List[str]]) -> None:
        super().__init__()
        self.columns = columns

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Returns the dataframe with the `columns` dropped.

        Args:
            X (pd.DataFrame): Dataframe to drop columns from.

        Returns:
            pd.DataFrame: Dataframe with columns dropped.
        """
        X = check_ready_to_transform(self, X, self.columns, force_all_finite=False)
        return X.drop(columns=self.columns)


class NaNTransformer(BaseTransformer):
    """Replace NaN values with a specified value. Internally Pandas [`fillna`](
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html)
    method is used.

    Example:
    ```python
    from sk_transformers import NaNTransformer
    import pandas as pd
    import numpy as np

    X = pd.DataFrame({"foo": [1, np.NaN, 3], "bar": ["a", np.NaN, "c"]})
    transformer = NaNTransformer([("foo", -999), ("bar", "-999")])
    transformer.fit_transform(X)
    ```
    ```
          foo   bar
    0     1.0     a
    1  -999.0  -999
    2     3.0     c
    ```

    Args:
        features (List[Tuple[str, Any]]): List of tuples where the first element is the column name, and the second is the value to replace NaN with.

    Raises:
        TypeError: If the value to replace NaN with is not a number, but the column is a number or vice versa.
    """

    def __init__(self, features: List[Tuple[str, Any]]) -> None:
        super().__init__()
        self.features = features

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Replace NaN values with a specified value.

        Args:
            X (pandas.DataFrame): Dataframe to transform.

        Returns:
            pandas.DataFrame: Transformed dataframe.
        """
        X = check_ready_to_transform(
            self,
            X,
            [feature[0] for feature in self.features],
            force_all_finite="allow-nan",
            return_polars=True,
        )

        feature_dict = dict(self.features)
        select_expr = []
        for feature in X.columns:
            if feature in feature_dict.keys():
                select_expr.append(pl.col(feature).fill_null(feature_dict[feature]))
            else:
                select_expr.append(pl.col(feature))
        return X.select(select_expr).to_pandas()


class ValueIndicatorTransformer(BaseTransformer):
    """Adds a column to a dataframe indicating if a value is equal to a
    specified value. The idea behind this method is, that it is often useful to
    know if a `NaN` value was present in the original data and has been changed
    by some imputation step. Sometimes the present of a `NaN` value is actually
    important information. But obviously this method works with any kind of
    data.

    `NaN`, `None` or `np.nan` are **Not** caught by this implementation.

    Example:
    ```python
    from sk_transformers import ValueIndicatorTransformer
    import pandas as pd

    X = pd.DataFrame({"foo": [1, -999, 3], "bar": ["a", "-999", "c"]})
    transformer = ValueIndicatorTransformer([("foo", -999), ("bar", "-999")])
    transformer.fit_transform(X).to_dict()
    ```
    ```
       foo   bar  foo_found_indicator  bar_found_indicator
    0    1     a                False                False
    1 -999  -999                 True                 True
    2    3     c                False                False
    ```

    Args:
        features (List[Tuple[str, Any]]): A list of tuples where the first value in represents the column
            name and the second value represents the value to check for.
    """

    def __init__(self, features: List[Tuple[str, Any]], as_int: bool = False) -> None:
        super().__init__()
        self.features = features
        self.as_int = as_int

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Add a column to a dataframe indicating if a value is equal to a
        specified value.

        Args:
            X (pandas.DataFrame): Dataframe to transform.

        Returns:
            pandas.DataFrame: Transformed dataframe containing columns indicating if a certain value was found.
                Format of the new columns: `"column_name"_nan_indicator`.
        """
        X = check_ready_to_transform(
            self,
            X,
            [feature[0] for feature in self.features],
            force_all_finite="allow-nan",
            return_polars=True,
        )

        return X.with_columns(
            [
                (pl.col(column) == indicator)
                .cast(pl.Int32 if self.as_int else pl.Boolean)
                .suffix("_found_indicator")
                for column, indicator in self.features
            ]
        ).to_pandas()


class QueryTransformer(BaseTransformer):
    """Applies a list of queries to a dataframe. If it operates on a dataset
    used for supervised learning this transformer should be applied on the
    dataframe containing `X` and `y`. So removing of columns by queries also
    removes the corresponding `y` value.

    Example:
    ```python
    import pandas as pd
    from sk_transformers import QueryTransformer

    X = pd.DataFrame({"foo": [1, 8, 3, 6, 5, 4, 7, 2]})
    transformer = QueryTransformer(["foo > 4"])
    transformer.fit_transform(X)
    ```
    ```
       foo
    1    8
    3    6
    4    5
    6    7
    ```

    Args:
        queries (List[str]): List of query string to evaluate to the dataframe.
    """

    def __init__(self, queries: List[str]) -> None:
        super().__init__()
        self.queries = queries

    def transform(self, Xy: pd.DataFrame) -> pd.DataFrame:
        """Applies the list of queries to the dataframe.

        Args:
            Xy (pd.DataFrame): Dataframe to apply the queries to. For also operating on the target column `y` - if needed.
                This column should also be part of the dataframe.

        Returns:
            pd.DataFrame: Dataframe with the queries applied.
        """
        Xy = check_ready_to_transform(
            self, Xy, Xy.columns, force_all_finite="allow-nan"
        )
        for query in self.queries:
            Xy = Xy.query(query, inplace=False)
        return Xy


class ValueReplacerTransformer(BaseTransformer):
    r"""Uses Pandas `replace` method to replace values in a column. This
    transformer loops over the `features` and applies `replace` to the
    according columns. If the column is not from type string but a valid
    regular expression is provided the column will be temporarily changed to a
    string column and after the manipulation by `replace` changed back to its
    original type. It may happen, that this type changing fails if the modified
    column is not compatible with its original type.

    Example:
    ```python
    import pandas as pd
    from sk_transformers import ValueReplacerTransformer

    X = pd.DataFrame(
        {"foo": ["0000-01-01", "2022/01/08", "bar", "1982-12-7", "28-09-2022"]}
    )
    transformer = ValueReplacerTransformer(
        [
            (
                ["foo"],
                r"^(?!(19|20)\d\d[-\/.](0[1-9]|1[012]|[1-9])[-\/.](0[1-9]|[12][0-9]|3[01]|[1-9])$).*",
                "1900-01-01",
            )
        ]
    )

    transformer.fit_transform(X)
    ```
    ```
              foo
    0  1900-01-01
    1  2022/01/08
    2  1900-01-01
    3   1982-12-7
    4  1900-01-01
    ```

    Args:
        features (List[Tuple[List[str], str, Any]]): List of tuples containing the column names as a list,
            the value to replace (can be a regex), and the replacement value.
    """

    def __init__(self, features: List[Tuple[List[str], Any, Any]]) -> None:
        super().__init__()
        self.features = features

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Replaces a value or regular expression with another value.

        Args:
            X (pd.DataFrame): Dataframe containing the columns where values should be replaced.

        Returns:
            pd.DataFrame: Dataframe with replaced values.
        """
        X = check_ready_to_transform(
            self, X, [feature[0][0] for feature in self.features]
        )

        for columns, value, replacement in self.features:
            for column in columns:
                is_regex = ValueReplacerTransformer.__check_for_regex(value)
                column_dtype = X[column].dtype

                if column_dtype is not str and is_regex:
                    X[column] = X[column].astype(str)

                X[column] = X[column].replace(value, replacement, regex=is_regex)

                if X[column].dtype != column_dtype:
                    X[column] = X[column].astype(column_dtype)

        return X

    @staticmethod
    def __check_for_regex(value: Any) -> bool:
        if not isinstance(value, str):
            return False
        try:
            re.compile(value)
            is_valid = True
        except re.error:
            is_valid = False
        return is_valid


class LeftJoinTransformer(BaseTransformer):
    """Performs a database-style left-join using `pd.merge`. This transformer
    is suitable for replacing values in a column of a dataframe by looking-up
    another `pd.DataFrame` or `pd.Series`. Note that, the join is based on the
    index of the right dataframe.

    Example:
    ```python
    import pandas as pd
    from sk_transformers import LeftJoinTransformer

    X = pd.DataFrame({"foo": ["A", "B", "C", "A", "C"]})
    lookup_df = pd.Series([1, 2, 3], index=["A", "B", "C"], name="values")
    transformer = LeftJoinTransformer([("foo", lookup_df)])
    transformer.fit_transform(X)
    ```
    ```
      foo  foo_values
    0   A           1
    1   B           2
    2   C           3
    3   A           1
    4   C           3
    ```

    Args:
        features (List[Tuple[str, Union[pd.Series, pd.DataFrame]]]): A list of tuples
            where the first element is the name of the column
            and the second element is the look-up dataframe or series.
    """

    __slots__ = ("features",)

    def __init__(
        self, features: List[Tuple[str, Union[pd.Series, pd.DataFrame]]]
    ) -> None:
        super().__init__()
        self.features = features

    @staticmethod
    def __prepare_lookup_df(
        df: Union[pd.Series, pd.DataFrame], prefix: str
    ) -> pd.DataFrame:
        if isinstance(df, pd.Series):
            df.name = df.name if df.name else "lookup"
            df = df.to_frame()

        if df.index.name is None:
            df.index.name = prefix

        df.columns = [df.index.name + "_" + column for column in df.columns]

        return df

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Perform a left-join on the given columns of a dataframe with another
        cooresponding dataframe.

        Args:
            X (pd.DataFrame): Dataframe containing the columns to be joined on.

        Returns:
            pd.DataFrame: Dataframe joined on the given columns.
        """
        X = check_ready_to_transform(
            self,
            X,
            [feature[0] for feature in self.features],
            force_all_finite="allow-nan",
            return_polars=True,
        )

        for column, lookup_df in self.features:
            X = X.join(
                pl.from_pandas(
                    self.__prepare_lookup_df(lookup_df, column), include_index=True
                ),
                on=column,
                how="left",
            )
        return X.to_pandas()


class AllowedValuesTransformer(BaseTransformer):
    """Replaces all values that are not in a list of allowed values with a
    replacement value. This performs an complementary transformation to that of
    the ValueReplacerTransformer. This is useful while lumping several minor
    categories together by selecting them using a list of major categories.

    Example:
    ```python
    import pandas as pd
    from sk_transformers.generic_transformer import AllowedValuesTransformer

    X = pd.DataFrame({"foo": ["a", "b", "c", "d", "e"]})
    transformer = AllowedValuesTransformer([("foo", ["a", "b"], "other")])
    transformer.fit_transform(X)
    ```
    ```
         foo
    0      a
    1      b
    2  other
    3  other
    4  other
    ```

    Args:
        features (List[Tuple[str, List[Any], Any]]): List of tuples where
            the first element is the column name,
            the second element is the list of allowed values in the column, and
            the third element is the value to replace disallowed values in the column.
    """

    def __init__(self, features: List[Tuple[str, List[Any], Any]]) -> None:
        super().__init__()
        self.features = features

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Replaces values not in a list with another value.

        Args:
            X (pd.DataFrame): Dataframe containing the columns with values to be replaced.

        Returns:
            pd.DataFrame: Dataframe with replaced values.
        """
        X = check_ready_to_transform(
            self, X, [feature[0] for feature in self.features], return_polars=True
        )

        return X.with_columns(
            [
                pl.col(column)
                .map_dict(
                    {allowed_value: allowed_value for allowed_value in allowed_values}
                )
                .cast(type(replacement))
                .fill_null(replacement)
                for column, allowed_values, replacement in self.features
            ]
        ).to_pandas()
