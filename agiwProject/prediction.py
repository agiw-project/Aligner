from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import metrics
from aligner import Aligner


# thresholds = [0.09, 0.10127, 0.1128, 0.12]
def predict2(json_site1, json_site2, print_report, threshold):
    numPages = len(json_site1)
    rows = []

    for page in json_site1:
        row_page = ""
        for leaf in page["leaves"]:
            content = str(leaf)
            new_content = content.replace("\n", "")
            row_page += " " + new_content

        row_page += "\n"
        rows.append(row_page)

    for page in json_site2:

        row_page = ""
        for leaf in page["leaves"]:
            content = str(leaf)
            new_content = content.replace("\n", "")
            row_page += " " + new_content
        row_page += "\n"
        rows.append(row_page)

    vectorizer = TfidfVectorizer(stop_words="english")
    # vectorialize the strings of the file
    vectors = vectorizer.fit_transform(rows)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)

    aligner = Aligner(threshold)

    predicted_aligned = aligner.get_aligned(df, numPages)
    not_predicted_aligned = aligner.get_not_aligned(predicted_aligned, numPages)

    fscore = metrics.f1(predicted_aligned, not_predicted_aligned)

    if print_report:
        print("Pages aligned: ")
        print(predicted_aligned)
        print("Pages not aligned: ")
        print(not_predicted_aligned)

        print("Comparazioni totali: " + str(len(predicted_aligned) + len(not_predicted_aligned)))

        print("#TP:" + str(metrics.get_TP(predicted_aligned)))
        print("#FP:" + str(metrics.get_FP(predicted_aligned)))
        print("#FN:" + str(metrics.get_FN(not_predicted_aligned)))
        print("#TN:" + str(metrics.get_TN(not_predicted_aligned)))

        print("precision: " + str(metrics.precision(predicted_aligned)))
        print("recall: " + str(metrics.recall(predicted_aligned, not_predicted_aligned)))

        print("f1-score: " + str(fscore))
        print("threshold: " + str(threshold))
        print("\n")

    return predicted_aligned, fscore, threshold


def predict(json_site1, json_site2, print_report):
    numPages = len(json_site1)
    rows = []

    for page in json_site1:
        row_page = ""
        for leaf in page["leaves"]:
            content = str(leaf)
            new_content = content.replace("\n", "")
            row_page += " " + new_content

        row_page += "\n"
        rows.append(row_page)

    for page in json_site2:

        row_page = ""
        for leaf in page["leaves"]:
            content = str(leaf)
            new_content = content.replace("\n", "")
            row_page += " " + new_content
        row_page += "\n"
        rows.append(row_page)

    vectorizer = TfidfVectorizer(stop_words="english")
    # vectorialize the strings of the file
    vectors = vectorizer.fit_transform(rows)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)

    fscoremax = 0
    aligned = []
    best_threshold = None

    thresholds = []
    start_from = 0.095
    step = 0.005
    for i in range(25):
        offset = step * i
        thresholds.append(start_from + offset)

    for threshold in thresholds:
        aligner = Aligner(threshold)

        predicted_aligned = aligner.get_aligned(df, numPages)
        not_predicted_aligned = aligner.get_not_aligned(predicted_aligned, numPages)

        fscore = metrics.f1(predicted_aligned, not_predicted_aligned)

        if print_report:
            print("Pages aligned: ")
            print(predicted_aligned)
            print("Pages not aligned: ")
            print(not_predicted_aligned)

            print("Comparazioni totali: " + str(len(predicted_aligned) + len(not_predicted_aligned)))

            print("#TP:" + str(metrics.get_TP(predicted_aligned)))
            print("#FP:" + str(metrics.get_FP(predicted_aligned)))
            print("#FN:" + str(metrics.get_FN(not_predicted_aligned)))
            print("#TN:" + str(metrics.get_TN(not_predicted_aligned)))
            print("precision: " + str(metrics.precision(predicted_aligned)))
            print("recall: " + str(metrics.recall(predicted_aligned, not_predicted_aligned)))

            print("f1-score: " + str(fscore))

        if fscoremax < fscore:
            fscoremax = fscore
            aligned = predicted_aligned
            best_threshold = threshold

    return aligned, fscoremax, best_threshold
