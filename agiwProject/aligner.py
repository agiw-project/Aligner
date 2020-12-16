
class Aligner:
    def __init__(self, threshold):
        self.threshold = threshold

    # intersection between lst1 and lst2
    def intersection(self, lst1, lst2):
        lst3 = []
        for i in range(len(lst1)):
            if lst1[i] > self.threshold and lst2[i] > self.threshold:
                lst3.append(lst1[i])
        return lst3

    def get_aligned(self, df, numPages):
        predicted_aligned = []
        for i in range(numPages):
            if i == numPages:
                break
            # compara riga per riga
            l1 = list(df.iloc[i])
            max_intersection = 0
            k = -1
            for j in range(numPages):
                l2 = list(df.iloc[numPages + j])
                l = self.intersection(l1, l2)
                if len(l) > max_intersection:
                    max_intersection = len(l)
                    k = j

            if k != -1:
                predicted_aligned.append((i + 1, k + 1))

        return predicted_aligned

    def get_not_aligned(self, predicted_aligned, numPages):
        not_alligned = []
        for i in range(numPages):
            for j in range(numPages):
                if (i + 1, j + 1) not in predicted_aligned:
                    not_alligned.append((i + 1, j + 1))
        return not_alligned