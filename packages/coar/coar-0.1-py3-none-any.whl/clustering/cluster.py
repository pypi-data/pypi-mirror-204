import numpy as np
from pandas import Series

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances

from clustering.helper import rule_distance


def _check_input(df, columns):
    # check df is not empty
    if not df.shape[0]:
        raise ValueError(
            "The input DataFrame `df` is empty."
        )

    # check for mandatory columns
    if not all(col in df.columns for col in columns):
        raise ValueError(
            f"Dataframe must have columns {columns}."
        )

    # check column types

    if "antecedent" in columns and not all(
            type(val) == set and all(type(v) == str for v in val) for val in df["antecedent"]):
        raise ValueError("Column antecedent must contain set of strings.")

    if "succedent" in columns and not all(
            type(val) == set and all(type(v) == str for v in val) for val in df["succedent"]):
        raise ValueError("Column succedent must contain set of strings.")

    if "support" in columns and not all(type(val) == float for val in df["support"]):
        raise ValueError("Column support must be float.")

    if "confidence" in columns and not all(type(val) == float for val in df["confidence"]):
        raise ValueError("Column confidence must be float.")

    if "cluster" in columns and not all(type(val) == float for val in df["confidence"]):
        raise ValueError("Column confidence must be float.")


def agglomerative_clustering(
        df,
        n_clusters=None,
        abs_attr_diff_threshold=None,
        rel_attr_diff_threshold=None,
        abs_supp_diff_threshold=None,
        rel_supp_diff_threshold=None,
        abs_conf_diff_threshold=None,
        rel_conf_diff_threshold=None,
):
    exclusive_param_pairs = [
        (abs_attr_diff_threshold, rel_attr_diff_threshold),
        (abs_supp_diff_threshold, rel_supp_diff_threshold),
        (abs_conf_diff_threshold, rel_conf_diff_threshold),
    ]

    # validate params
    if n_clusters:
        if not all(param is None for param_pairs in exclusive_param_pairs for param in param_pairs):
            raise ValueError(
                "Threshold params"
                "abs_attr_diff_threshold, rel_attr_diff_threshold, "
                "abs_supp_diff_threshold, rel_supp_diff_threshold, "
                "abs_conf_diff_threshold, rel_conf_diff_threshold "
                " must be None if n_clusters is specified. "
                "Specify either n_clusters or threshold params."
            )
        distance_threshold = None
    else:
        for i, j in exclusive_param_pairs:
            if not ((i is None) ^ (j is None)):
                raise ValueError(
                    "Exactly one of absolute and relative thresholds has to be set per characteristic, "
                    "and the other needs to be None. Set one param per each of the following pairs:"
                    "abs_attr_diff_threshold or rel_attr_diff_threshold, "
                    "abs_supp_diff_threshold or rel_supp_diff_threshold,"
                    "abs_conf_diff_threshold or rel_conf_diff_threshold."
                )

        selected_thresholds = [abs_threshold or rel_threshold for abs_threshold, rel_threshold in exclusive_param_pairs]

        if not all(threshold >= 0 for threshold in selected_thresholds):
            raise ValueError(
                "Threshold params"
                "abs_attr_diff_threshold, rel_attr_diff_threshold, "
                "abs_supp_diff_threshold, rel_supp_diff_threshold, "
                "abs_conf_diff_threshold, rel_conf_diff_threshold "
                "must be positive. "
            )
        # add cedent threshold twice because it's used for antecedent and succedent as well
        distance_threshold = selected_thresholds[0] + sum(selected_thresholds)

    _check_input(df, ["antecedent", "succedent", "support", "confidence"])

    metric_params = {
        'df': df,
        'abs_attr_diff_threshold': abs_attr_diff_threshold,
        'rel_attr_diff_threshold': rel_attr_diff_threshold,
        'abs_supp_diff_threshold': abs_supp_diff_threshold,
        'rel_supp_diff_threshold': rel_supp_diff_threshold,
        'abs_conf_diff_threshold': abs_conf_diff_threshold,
        'rel_conf_diff_threshold': rel_conf_diff_threshold,
    }

    # surpass validation
    x = np.array([i for i in df.index]).reshape(-1, 1)
    distance_matrix = pairwise_distances(
        x, metric=rule_distance, **metric_params
    )
    clustering = AgglomerativeClustering(
        n_clusters=n_clusters, linkage='complete', metric='precomputed', compute_full_tree=True,
        distance_threshold=distance_threshold
    )

    clusters = clustering.fit_predict(distance_matrix)
    df['cluster'] = clusters
    return df


def cluster_representative(df):
    columns_in_sort_order = ["support", "confidence", "antecedent", "succedent"]
    _check_input(df, columns_in_sort_order + ["cluster"])
    repr_indexes = [df.loc[df['cluster'] == cluster].sort_values(
        columns_in_sort_order, ascending=[False, False, True, True],
        key=lambda x: Series(len(i) if type(i) == set else i for i in x)).index[0] for cluster in
                    set(df['cluster'].tolist())]
    df['representative'] = [1 if i in repr_indexes else 0 for i in df.index]
    return df
