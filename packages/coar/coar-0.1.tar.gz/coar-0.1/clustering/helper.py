import sys


def get_support_from_fourfold(fourfold):
    return fourfold[0] / sum(fourfold)


def get_confidence_from_fourfold(fourfold):
    return fourfold[0] / (fourfold[0] + fourfold[1])


def jacquard_distance(set_1, set_2) -> float:
    intersection = set_1.intersection(set_2)
    union = set_1.union(set_2)
    return 1 - len(intersection) / len(union)


def rule_jacquard_distance(x, y, df=None) -> float:
    x = df.iloc[int(x[0])]
    y = df.iloc[int(y[0])]
    ante_1, succ_1, support_1, confidence_1 = x.antecedent, x.succedent, x.support, x.confidence
    ante_2, succ_2, support_2, confidence_2 = y.antecedent, y.succedent, y.support, y.confidence

    alpha = abs(support_1 - support_2) + 0.1
    beta = abs(confidence_1 - confidence_2) + 0.1
    dist = alpha * jacquard_distance(ante_1.union(succ_1), ante_2.union(succ_2)) + beta * (
            jacquard_distance(ante_1, ante_2) + jacquard_distance(succ_1, succ_2))

    return dist


def dist_abs(val_1, val_2):
    return abs(val_1 - val_2)


def confidence_dist_rel(conf1, conf2):
    try:
        return abs(conf1 - conf2) / max(1 - conf1, 1 - conf2)
    except ZeroDivisionError:
        return 0


def support_dist_rel(supp1, supp2):
    try:
        return abs(supp1 - supp2) / max(supp1, supp2)
    except ZeroDivisionError:
        return 0


def cedent_dist_abs(cen1, cen2):
    intersection = cen1.intersection(cen2)
    if not intersection:
        return float('inf')
    return len(cen1.union(cen2)) - len(intersection)


def cedent_dist_rel(cen1, cen2):
    dist = jacquard_distance(cen1, cen2)
    if dist == 1:
        return float('inf')
    return dist


def rule_distance(
        x, y, df=None,
        abs_attr_diff_threshold=None,
        rel_attr_diff_threshold=None,
        abs_supp_diff_threshold=None,
        rel_supp_diff_threshold=None,
        abs_conf_diff_threshold=None,
        rel_conf_diff_threshold=None,
) -> float:
    x = df.iloc[int(x[0])]
    y = df.iloc[int(y[0])]

    ante_x, succ_x, supp_x, conf_x = x.antecedent, x.succedent, float(x.support), float(x.confidence)
    ante_y, succ_y, supp_y, conf_y = y.antecedent, y.succedent, float(y.support), float(y.confidence)

    cedent_metric, cedent_threshold = (cedent_dist_abs, abs_attr_diff_threshold) if abs_attr_diff_threshold else (
        jacquard_distance, rel_attr_diff_threshold)
    supp_metric, supp_threshold = (dist_abs, abs_supp_diff_threshold) if abs_supp_diff_threshold else (
        support_dist_rel, rel_supp_diff_threshold)
    conf_metric, conf_threshold = (dist_abs, abs_conf_diff_threshold) if abs_conf_diff_threshold else (
        confidence_dist_rel, rel_conf_diff_threshold)

    ante_dist = cedent_metric(ante_x, ante_y)
    succ_dist = cedent_metric(succ_x, succ_y)
    supp_dist = supp_metric(supp_x, supp_y)
    conf_dist = conf_metric(conf_x, conf_y)

    dist = float('inf') if (cedent_threshold and supp_threshold and conf_threshold) and (
            ante_dist > cedent_threshold or succ_dist > cedent_threshold or supp_dist > supp_threshold or
            conf_dist > conf_threshold
    ) else ante_dist + succ_dist + supp_dist + conf_dist

    # clustering requires float64, can't return inf
    return sys.float_info.max if dist == float('inf') else dist
