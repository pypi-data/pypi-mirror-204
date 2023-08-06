import numpy as np
from IPython.display import display, Latex
from collections import Counter

# implement (ROC) (AUC)  and  (PR AUC) heck

# ==========================================================================================================================================|
# ===================================================================Logistic_Regression_Classifier================================================|

# Links:

# https://www.youtube.com/watch?v=JUchmd6I7Es&list=PL4_hYwCyhAvasRqzz4w562ce0esEwS0Mt&index=3 - MFTI

# Notes:


# ==========================================================================================================================================|

class Logistic_Regression_Classifier:

    def __init__(self, learning_rate=0.0001, _tolerance=1e-4, _iterations=5000):

        self.iterations = _iterations
        self.learning_rate = learning_rate
        self.tolerance = _tolerance

    @staticmethod
    def loss(y_true, y_pred):
        y_pred = np.clip(y_pred, 1e-12, 1 - 1e-12)
        return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

    def sigmoid(self, X):
        return 1/(1 + np.exp(-X))

    def display_equation(self):
        display(Latex(
            f'$F_{{\\theta_1,\\theta_0}}(X)^{{def}} = \\frac{{1}}{{1+e^{{-(\\theta_1 \\times X + \\theta_0)}}}}$'))

    def fit(self, X, y):

        n = X.shape[1]
        self.weights = np.zeros(n)
        self.intercept = 0
        prev_loss = np.inf

        for _ in range(self.iterations):
            y_pred = self.sigmoid(np.dot(X, self.weights) + self.intercept)

            d_weights = (1/n) * np.dot(X.T, (y_pred - y))
            d_intercept = (1/n) * np.sum(y_pred - y)

            self.weights -= self.learning_rate * d_weights
            self.intercept -= self.learning_rate * d_intercept

            current_loss = self.loss(y, y_pred)
            if abs(prev_loss - current_loss) < self.tolerance:
                break

            prev_loss = current_loss

    def predict(self, X):
        predictions = self.sigmoid(np.dot(X, self.weights) + self.intercept)
        return np.where(predictions >= 0.5, 1, 0)

# ==========================================================================================================================================|
# ===================================================================K_Nearest_Neighbours_Classifier================================================|
# ==========================================================================================================================================|


class K_Nearest_Neighbours_Classifier:

    @staticmethod
    def euclidian_distance(x_1, x_2):
        return np.sqrt(sum((x_1 - x_2) ** 2))

    def __init__(self, _k):
        self.k = _k

    def fit(self, X, y):
        self.X = X
        self.y = y

    def predict(self, X):
        return [self._predict(x) for x in X]

    def _predict(self, x):

        distances = [self.euclidian_distance(x, x_tr) for x_tr in self.X]
        knn_indices = np.argsort(distances)[:self.k]
        knn_labels = [self.y[i] for i in knn_indices]
        most_common = Counter(knn_labels).most_common()
        return most_common[0][0]


# ==========================================================================================================================================|
# ===================================================================Decision_Tree_Classifier================================================|
# Links:

    # https://www.youtube.com/watch?v=NxEHSAfFlK8&list=PLcWfeUsAys2k_xub3mHks85sBHZvg24Jd&index=5 - Better Implementaion
    # https://www.youtube.com/watch?v=sgQAhG5Q7iY - Current Implementation
    # https://www.youtube.com/watch?v=vzbyk_7HdiQ&list=PL4_hYwCyhAvasRqzz4w562ce0esEwS0Mt&index=5 - MFTI
    # https://www.youtube.com/watch?v=u4kbPtiVVB8&t=0s - _reduced_error_puning
    # https://www.youtube.com/watch?v=D0efHEJsfHo - _cost_complexity_puning

# Notes:

    # digg into bootstraping
    # binarisation (partition logic can be modified)
    # Gini Impuruty under the hood

# ==========================================================================================================================================|


class Node():
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, info_gain=None, *, value=None):
        ''' constructor '''

        # for decision node
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.info_gain = info_gain

        # for leaf node
        self.value = value

    def _is_leaf_node(self):
        return self.value is not None


class Decision_Tree_Classifier():
    def __init__(self, _min_samples_split=2, _max_depth=100, _n_rand_features=None, _criterion="entropy", _pre_prunning=False):

        # tree root
        self.root = None

        # prepruning conditions
        self.min_samples_split = _min_samples_split
        self.max_depth = _max_depth

        # modifications
        self.n_rand_features = _n_rand_features
        self.criterion = _criterion
        self.pre_prunning = _pre_prunning

    def _cost_complexity_pruning(self, tree, dataset):

        return tree

    # TO DO
    def _reduced_error_pruning(self, tree, dataset):

        return tree

    def _grow_tree(self, dataset, current_depth=0):

        # current node data
        X, y = dataset[:, :-1], dataset[:, -1]
        n_samples, n_features = X.shape
        n_labels = len(np.unique(y))

        if self.pre_prunning:
            if n_samples < self.min_samples_split or current_depth >= self.max_depth or n_labels == 1:
                return Node(value=self._most_common_label(y))

        # rundomly select n_rand_features featurs indexes
        random_features_indexes = np.random.choice(n_features, self.n_rand_features, replace=False)  # noqa

        best_split = self._get_best_split(dataset, random_features_indexes)  # noqa

        if best_split["info_gain"] > 0:

            left_subtree = self._grow_tree(best_split["dataset_left"], current_depth+1)  # noqa
            right_subtree = self._grow_tree(best_split["dataset_right"], current_depth+1)  # noqa
            return Node(best_split["feature_index"], best_split["threshold"], left_subtree, right_subtree, best_split["info_gain"])  # noqa

    def _get_best_split(self, dataset, random_features_indexes):

        # dictionary to store the best split

        best_split = {}
        max_info_gain = -float("inf")

        # loop over all the features
        for feature_index in random_features_indexes:

            possible_thresholds = np.unique(dataset[:, feature_index])

            for threshold in possible_thresholds:

                # binarisation (partition logic can be modified)
                dataset_left, dataset_right = self._split(dataset, feature_index, threshold)  # noqa

                if len(dataset_left) > 0 and len(dataset_right) > 0:

                    parent_labels, left_child_labels, right_child_labels = dataset[:, -1], dataset_left[:, -1], dataset_right[:, -1]  # noqa
                    curr_info_gain = self._get_information_gain(parent_labels, left_child_labels, right_child_labels, "entropy")  # noqa

                    if curr_info_gain > max_info_gain:

                        best_split["feature_index"] = feature_index
                        best_split["threshold"] = threshold
                        best_split["dataset_left"] = dataset_left
                        best_split["dataset_right"] = dataset_right
                        best_split["info_gain"] = curr_info_gain
                        max_info_gain = curr_info_gain

        return best_split

    def _get_information_gain(self, parent_labels, left_child_labels, right_child_labels, mode="entropy"):

        weight_l = len(left_child_labels) / len(parent_labels)
        weight_r = len(right_child_labels) / len(parent_labels)

        if self.criterion == "gini":
            return self._gini_index(
                parent_labels) - (weight_l*self._gini_index(left_child_labels) + weight_r*self._gini_index(right_child_labels))
        else:
            return self._entropy(
                parent_labels) - (weight_l*self._entropy(left_child_labels) + weight_r*self._entropy(right_child_labels))

    def _split(self, dataset, feature_index, threshold):

        dataset_left = np.array(
            [row for row in dataset if row[feature_index] <= threshold])  # noqa
        dataset_right = np.array(
            [row for row in dataset if row[feature_index] > threshold])  # noqa

        return dataset_left, dataset_right

    def _entropy(self, y):

        class_labels = np.unique(y)
        entropy = 0
        for cls in class_labels:
            p_cls = len(y[y == cls]) / len(y)
            entropy += -p_cls * np.log2(p_cls)
        return entropy

    def _gini_index(self, y):

        class_labels = np.unique(y)
        gini = 0
        for cls in class_labels:
            p_cls = len(y[y == cls]) / len(y)
            gini += p_cls**2
        return 1 - gini

    def _most_common_label(self, y):
        y = list(y)
        return max(y, key=y.count)

    def print_tree(self, tree=None, indent=" "):

        if not tree:
            tree = self.root

        if tree.value is not None:
            print(tree.value)

        else:
            print("X_"+str(tree.feature_index), "<=",
                  tree.threshold, "?", tree.info_gain)
            print("%sleft:" % (indent), end="")
            self.print_tree(tree.left, indent + indent)
            print("%sright:" % (indent), end="")
            self.print_tree(tree.right, indent + indent)

    def fit(self, X, Y):
        self.n_rand_features = X.shape[1] if not self.n_rand_features else min(X.shape[1], self.n_rand_features)  # noqa

        dataset = np.concatenate((X, Y), axis=1)
        self.root = self._grow_tree(dataset)

    def predict(self, X):

        return np.array([self._make_prediction(x, self.root) for x in X])

    def _make_prediction(self, x, node):

        if node._is_leaf_node():
            return node.value

        feature_value = x[node.feature_index]
        if feature_value <= node.threshold:
            return self._make_prediction(x, node.left)
        return self._make_prediction(x, node.right)

# ==========================================================================================================================================|
# ===================================================================Naive_Bias_Classifier================================================|
# Links:

    # https://www.youtube.com/watch?v=O2L2Uv9pdDA&list=RDCMUCtYLUTtgS3k1Fg4y5tAhLbw&index=1 - StatQuest
    # https://www.youtube.com/watch?v=lFJbZ6LVxN8&list=PLM8wYQRetTxAIU0oOarQeW2WOeYV9LyuG&index=12 - deeper dive
    # https://www.youtube.com/watch?v=3I8oX3OUL6I&list=PLM8wYQRetTxAIU0oOarQeW2WOeYV9LyuG&index=13 - implementation


# Notes:

# ==========================================================================================================================================|


class Gaussian_Naive_Bayes_Classifier:
    def __init__(self) -> None:
        pass

    def fit(self, X, y):

        self.class_labels = np.unique(y)
        self.mean_ = {}
        self.std_ = {}
        self.priors_ = {}

        for class_value in self.class_labels:
            class_values_subset = X[np.where(y == class_value)[0]]
            self.priors_[class_value] = len(class_values_subset)/X.shape[0]
            self.mean_[class_value] = np.mean(class_values_subset, axis=0)
            self.std_[class_value] = np.std(class_values_subset, axis=0)

        return self

    def predict(self, X):

        predictions = []
        for row in X:
            posteriors = []
            for class_label in self.class_labels:
                prior = self.priors_[class_label]
                conditional = np.sum(np.log(self._gaussian_density(class_label, row)))  # noqa
                posterior = prior + conditional
                posteriors.append(posterior)

            predictions.append(np.argmax(posteriors))

        return np.array(predictions)

    def _gaussian_density(self, class_label, X):
        mean = self.mean_[class_label]
        std = self.std_[class_label]
        return np.exp((-1/2)*((X - mean)**2) / (2 * std)) / np.sqrt(2 * np.pi * std)

# ==========================================================================================================================================|
# ===================================================================Support_Vector_Machine_Classifier================================================|
# Links:

# https://www.youtube.com/watch?v=efR1C6CvhmE&list=RDCMUCtYLUTtgS3k1Fg4y5tAhLbw&index=5 - stat quest Pt1
# https://www.youtube.com/watch?v=Toet3EiSFcM - The Polynomial Kernel
# https://www.youtube.com/watch?v=Qc5IyLW_hns - The Radial (RBF) Kernel(Radial Basis Function)

# Notes:


# ==========================================================================================================================================|


class SVM:

    def __init__(self, learning_rate=0.001, lambda_param=0.01, n_iters=1000):
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.w = None
        self.b = None

    def fit(self, X, y):
        n_samples, n_features = X.shape

        y_ = np.where(y <= 0, -1, 1)

        # init weights
        self.w = np.zeros(n_features)
        self.b = 0

        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                condition = y_[idx] * (np.dot(x_i, self.w) - self.b) >= 1
                if condition:
                    self.w -= self.lr * (2 * self.lambda_param * self.w)
                else:
                    self.w -= self.lr * (2 * self.lambda_param * self.w - np.dot(x_i, y_[idx]))  # noqa
                    self.b -= self.lr * y_[idx]

    def predict(self, X):
        approx = np.dot(X, self.w) - self.b
        return np.sign(approx)

# ==========================================================================================================================================|
# ===================================================================Random_Forest_Classifier================================================|
# ==========================================================================================================================================|


# ==========================================================================================================================================|
# ===================================================================Neural_Net_Classifier================================================|
# ==========================================================================================================================================|
