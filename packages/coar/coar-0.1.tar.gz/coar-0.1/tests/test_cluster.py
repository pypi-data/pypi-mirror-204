import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances

from clustering.cluster import agglomerative_clustering
from clustering.helper import rule_distance
from tests.conftest import SUPP, CONF, ANTECEDENT_TYPE, SUCCEDENT_TYPE, MAX_SUPP, MAX_CONF

REL_ATTR_DIFF_THRESHOLD = 0.2
REL_SUPP_DIFF_THRESHOLD = 0.2
REL_CONF_DIFF_THRESHOLD = 0.2


# params tests
def test_cluster_two_identical_rules(rule_factory, short_cedents):
    # one cluster
    ante_1, succ_1 = short_cedents
    df = pd.DataFrame.from_records([rule_factory(ante_1, succ_1, SUPP, CONF)] * 2)
    clustering = agglomerative_clustering(
        df, rel_attr_diff_threshold=REL_ATTR_DIFF_THRESHOLD, rel_supp_diff_threshold=REL_SUPP_DIFF_THRESHOLD,
        rel_conf_diff_threshold=REL_CONF_DIFF_THRESHOLD,
    )
    assert len(set(clustering['cluster'])) == 1


def test_cluster_two_rules_ante_diff(rule_factory, short_cedents, attr_factory):
    # one cluster
    ante_1, succ_1 = short_cedents
    ante_2, succ_2 = short_cedents
    ante_2.add(attr_factory(2, ANTECEDENT_TYPE))
    df = pd.DataFrame.from_records([rule_factory(ante_1, succ_1, SUPP, CONF), rule_factory(ante_2, succ_2, SUPP, CONF)])
    clustering = agglomerative_clustering(
        df, rel_attr_diff_threshold=REL_ATTR_DIFF_THRESHOLD, rel_supp_diff_threshold=REL_SUPP_DIFF_THRESHOLD,
        rel_conf_diff_threshold=REL_CONF_DIFF_THRESHOLD,
    )
    assert len(set(clustering['cluster'])) == 1


def test_cluster_two_rules_ante_supp_diff(rule_factory, short_cedents, attr_factory):
    # two clusters
    ante_1, succ_1 = short_cedents
    ante_2, succ_2 = short_cedents
    ante_2.add(attr_factory(2, ANTECEDENT_TYPE))
    df = pd.DataFrame.from_records(
        [rule_factory(ante_1, succ_1, SUPP, CONF), rule_factory(ante_2, succ_2, MAX_SUPP, CONF)])
    clustering = agglomerative_clustering(
        df, rel_attr_diff_threshold=REL_ATTR_DIFF_THRESHOLD, rel_supp_diff_threshold=REL_SUPP_DIFF_THRESHOLD,
        rel_conf_diff_threshold=REL_CONF_DIFF_THRESHOLD,
    )
    assert len(set(clustering['cluster'])) == 2


def test_cluster_two_rules_succ_diff(rule_factory, short_cedents, attr_factory):
    # one cluster
    ante_1, succ_1 = short_cedents
    ante_2, succ_2 = short_cedents
    succ_2.add(attr_factory(2, SUCCEDENT_TYPE))
    df = pd.DataFrame.from_records([rule_factory(ante_1, succ_1, SUPP, CONF), rule_factory(ante_2, succ_2, SUPP, CONF)])
    clustering = agglomerative_clustering(
        df, rel_attr_diff_threshold=REL_ATTR_DIFF_THRESHOLD, rel_supp_diff_threshold=REL_SUPP_DIFF_THRESHOLD,
        rel_conf_diff_threshold=REL_CONF_DIFF_THRESHOLD,
    )
    assert len(set(clustering['cluster'])) == 1


def test_cluster_two_rules_succ_conf_diff(rule_factory, short_cedents, attr_factory):
    # two clusters
    ante_1, succ_1 = short_cedents
    ante_2, succ_2 = short_cedents
    df = pd.DataFrame.from_records([rule_factory(ante_1, succ_1, SUPP, CONF),
                                    rule_factory(ante_2, succ_2.union({attr_factory(2, SUCCEDENT_TYPE)}), SUPP,
                                                 MAX_CONF)])
    clustering = agglomerative_clustering(
        df, rel_attr_diff_threshold=REL_ATTR_DIFF_THRESHOLD, rel_supp_diff_threshold=REL_SUPP_DIFF_THRESHOLD,
        rel_conf_diff_threshold=REL_CONF_DIFF_THRESHOLD,
    )
    assert len(set(clustering['cluster'])) == 2


# n_clusters tests
# By passing n_clusters param we get as many clusters as we ask for no matter the distances.
# We need to test distance matrix instead.
def test_cluster_two_identical_rules_n_clusters(rule_factory, short_cedents):
    # one cluster
    ante_1, succ_1 = short_cedents
    df = pd.DataFrame.from_records([rule_factory(ante_1, succ_1, SUPP, CONF)] * 2)
    x = np.array([i for i in df.index]).reshape(-1, 1)
    distance_matrix = pairwise_distances(
        x, metric=rule_distance, **{'df': df}
    )
    assert (distance_matrix == 0.0).all()


def test_cluster_two_rules_ante_diff_n_clusters(rule_factory, short_cedents, attr_factory):
    # one cluster
    ante_1, succ_1 = short_cedents
    ante_2, succ_2 = short_cedents
    ante_2.add(attr_factory(2, ANTECEDENT_TYPE))
    df = pd.DataFrame.from_records([rule_factory(ante_1, succ_1, SUPP, CONF), rule_factory(ante_2, succ_2, SUPP, CONF)])
    x = np.array([i for i in df.index]).reshape(-1, 1)
    distance_matrix = pairwise_distances(
        x, metric=rule_distance, **{'df': df}
    )
    assert (distance_matrix == 0.0).all()


def test_cluster_two_rules_ante_supp_diff_n_clusters(rule_factory, short_cedents, attr_factory):
    # two clusters
    ante_1, succ_1 = short_cedents
    ante_2, succ_2 = short_cedents
    ante_2.add(attr_factory(2, ANTECEDENT_TYPE))
    df = pd.DataFrame.from_records(
        [rule_factory(ante_1, succ_1, SUPP, CONF), rule_factory(ante_2, succ_2, MAX_SUPP, CONF)])
    x = np.array([i for i in df.index]).reshape(-1, 1)
    distance_matrix = pairwise_distances(
        x, metric=rule_distance, **{'df': df}
    )
    assert distance_matrix[0][1] == distance_matrix[1][0] != 0.0


def test_cluster_two_rules_succ_diff_n_clusters(rule_factory, short_cedents, attr_factory):
    # one cluster
    ante_1, succ_1 = short_cedents
    ante_2, succ_2 = short_cedents
    succ_2.add(attr_factory(2, SUCCEDENT_TYPE))
    df = pd.DataFrame.from_records([rule_factory(ante_1, succ_1, SUPP, CONF), rule_factory(ante_2, succ_2, SUPP, CONF)])
    clustering = agglomerative_clustering(
        df, rel_attr_diff_threshold=REL_ATTR_DIFF_THRESHOLD, rel_supp_diff_threshold=REL_SUPP_DIFF_THRESHOLD,
        rel_conf_diff_threshold=REL_CONF_DIFF_THRESHOLD,
    )
    assert len(set(clustering['cluster'])) == 1


def test_cluster_two_rules_succ_conf_diff_n_clusters(rule_factory, short_cedents, attr_factory):
    # two clusters
    ante_1, succ_1 = short_cedents
    ante_2, succ_2 = short_cedents
    df = pd.DataFrame.from_records([rule_factory(ante_1, succ_1, SUPP, CONF),
                                    rule_factory(ante_2, succ_2.union({attr_factory(2, SUCCEDENT_TYPE)}), SUPP,
                                                 MAX_CONF)])
    x = np.array([i for i in df.index]).reshape(-1, 1)
    distance_matrix = pairwise_distances(
        x, metric=rule_distance, **{'df': df}
    )
    assert distance_matrix[0][1] == distance_matrix[1][0] != 0.0
