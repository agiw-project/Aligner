def ground_truth():
    gt = []
    for i in range(50):
        gt.append((i, i))
    return gt


def get_TP(predicted_aligned):
    num_TP = 0
    gt = ground_truth()
    for (i, j) in predicted_aligned:
        if gt.__contains__((i, j)):
            num_TP += 1
    return num_TP


def get_FP(predicted_aligned):
    num_FP = 0
    gt = ground_truth()
    for (i, j) in predicted_aligned:
        if not gt.__contains__((i, j)):
            num_FP += 1
    return num_FP


def get_FN(predicted_not_aligned):
    num_FN = 0
    gt = ground_truth()
    for (i, j) in predicted_not_aligned:
        if gt.__contains__((i, j)):
            num_FN += 1
    return num_FN


def get_TN(predicted_not_aligned):
    num_TN = 0
    gt = ground_truth()
    for (i, j) in predicted_not_aligned:
        if not gt.__contains__((i, j)):
            num_TN += 1
    return num_TN


def precision(predicted_aligned):
    tp = get_TP(predicted_aligned)
    fp = get_FP(predicted_aligned)
    if (fp + tp) == 0:
        return 0
    return tp / (fp + tp)


def recall(predicted_aligned, predicted_not_aligned):
    tp = get_TP(predicted_aligned)
    fn = get_FN(predicted_not_aligned)
    if (fn + tp) == 0:
        return 0
    return tp / (fn + tp)


def f1(predicted_aligned, predicted_not_aligned):
    p = precision(predicted_aligned)
    r = recall(predicted_aligned, predicted_not_aligned)
    if (p + r) == 0:
        return 0
    score = (2 * (p * r)) / (p + r)
    return score
