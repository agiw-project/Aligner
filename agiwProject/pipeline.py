import json
from prediction import predict, predict2
from extraction import extract

N_SOURCES = 3


def load(fileName):
    f = open(fileName)
    json_object = json.loads(f.read())
    f.close()
    return json_object


def get_max_fscore(json_site1, json_site2):
    aligned1, fscore1, threshold1 = predict(json_site1, json_site2, False)
    aligned2, fscore2, threshold2 = predict(json_site2, json_site1, False)
    if fscore1 > fscore2:
        return threshold1
    return threshold2


def get_max_fscore_with_threshold(json_site1, json_site2, threshold):
    aligned1, fscore1, threshold1 = predict2(json_site1, json_site2, True, threshold)
    aligned2, fscore2, threshold2 = predict2(json_site2, json_site1, True, threshold)
    if fscore1 > fscore2:
        return aligned1, fscore1, threshold1
    return aligned2, fscore2, threshold2


class Pipeline:
    max_thresholds = []

    def __init__(self):
        self.start()

    def start(self):
        # EXTRACTION
        try:
            print("Skipping extraction\n")
            print("Loading contents from json files\n")
            json_site1 = load("Json/pages_new_url1.json")
            json_site2 = load("Json/pages_new_url2.json")
            json_site3 = load("Json/pages_new_url3.json")
        except FileNotFoundError:
            print("Starting extraction")
            extract("Url/url1.txt")
            extract("Url/url2.txt")
            extract("Url/url3.txt")
            print("Loading contents from json files\n\n")
            json_site1 = load("Json/pages_new_url1.json")
            json_site2 = load("Json/pages_new_url2.json")
            json_site3 = load("Json/pages_new_url3.json")

        # TUNING
        print("Checking thresholds tuning...\n")
        try:
            f = open("max_thresholds.txt", "r")
            for line in f:
                self.max_thresholds.append(float(line.replace("\n", "")))
            print("Skipping tuning\n")
        except FileNotFoundError:
            print("Need to tune threshold to compare sources 1 and 2...\n")
            f = open("max_thresholds.txt", "a")
            max_threshold_12 = get_max_fscore(json_site1, json_site2)
            f.write(str(max_threshold_12))
            f.write("\n")
            self.max_thresholds.append(max_threshold_12)
            print("New threshold is " + str(max_threshold_12) + "\n")

            print("Need to tune threshold to compare sources 1 and 3...\n")
            max_threshold_13 = get_max_fscore(json_site1, json_site3)
            f.write(str(max_threshold_13))
            f.write("\n")
            self.max_thresholds.append(max_threshold_13)
            print("New threshold is " + str(max_threshold_13) + "\n")

            print("Need to tune threshold to compare sources 2 and 3...\n")
            max_threshold_23 = get_max_fscore(json_site2, json_site3)
            f.write(str(max_threshold_23))
            f.write("\n")
            f.close()
            self.max_thresholds.append(max_threshold_23)
            print("New threshold is " + str(max_threshold_23) + "\n")

        # ALIGNMENT 1, 2

        print("Starting page alignement learning...\n")
        print("Max thresholds: ")
        print(self.max_thresholds)
        print("\nComparing source 1 with source 2")
        aligned, fscore, threshold = get_max_fscore_with_threshold(json_site1, json_site2, self.max_thresholds[0])

        # METRICS 1, 2
        print("\n#############################################\n")
        print("\nBest results for comparing source 1 with 2\n")
        print("Pages aligned: ")
        print(aligned)
        print("best fscore: " + str(fscore))
        print("threshold: " + str(threshold))
        print("\n#############################################\n")

        print("\n")

        # ALIGNMENT 1, 3
        print("Comparing source 1 with source 3")
        aligned, fscore, threshold = get_max_fscore_with_threshold(json_site1, json_site3, self.max_thresholds[1])

        # METRIC 1, 3
        print("\n#############################################\n")
        print("\nBest results for comparing source 1 with 3\n")
        print("Pages aligned: ")
        print(aligned)
        print("best fscore: " + str(fscore))
        print("threshold: " + str(threshold))
        print("\n#############################################\n")

        print("\n")

        # ALIGNMENT 2, 3
        print("Comparing source 2 with source 3")
        aligned, fscore, threshold = get_max_fscore_with_threshold(json_site2, json_site3, self.max_thresholds[2])

        # METRIC 2, 3
        print("\n#############################################\n")
        print("\nBest results for comparing source 2 with 3\n")
        print("Pages aligned: ")
        print(aligned)
        print("best fscore: " + str(fscore))
        print("threshold: " + str(threshold))
        print("\n#############################################\n")

        print("\n")
