
import numpy as np


# ==========================================================================================================================================|
# ===================================================================GD_Linear_Regression================================================|
# ==========================================================================================================================================|


class GD_Linear_Regression:

    def __init__(self, _learning_rate=0.01, _tolerance=0.0001, _iterations=1000):

        self.learning_rate = _learning_rate
        self.iterations = _iterations
        self.tolerance = _tolerance

    def mse(self, y_true, y_pred):
        return np.mean((y_true - y_pred) ** 2)

    def fit(self, X, y):

        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.intercept = 0
        mse_prev = np.inf

        for _ in range(self.iterations):

            y_pred = self.predict(X)

            d_weights = (2 * (X.T).dot(y_pred - y)) / n_samples
            d_intercept = 2 * np.sum(y_pred - y) / n_samples

            self.weights -= self.learning_rate * d_weights
            self.intercept -= self.learning_rate * d_intercept

            current_mse = self.mse(y, y_pred)

            if abs(current_mse - mse_prev) < self.tolerance:
                break

    def predict(self, X):
        return np.dot(X, self.weights) + self.intercept


# ==========================================================================================================================================|
# ===================================================================OLS_Linear_Regression================================================|
# ==========================================================================================================================================|

# ========================================== DEAL WITH  (while linear algebra mastering for NNs) =============================

# https://www.youtube.com/watch?v=sl3MM_i3az8&list=PL4_hYwCyhAvasRqzz4w562ce0esEwS0Mt&index=3
# https://www.youtube.com/watch?v=bOIPwdWso_0&list=RDCMUC5_6ZD6s8klmMu9TXEB_1IA&index=8
class OLS_Linear_Regression:  # https://www.youtube.com/watch?v=z2hpinQggNM&list=RDCMUC_lePY0Lm0E2-_IkYUWpI5A&index=2 - digg into

    def fit(self, X, y):

        ones = np.ones(len(X)).reshape(-1, 1)
        X = np.concatenate((ones, X), axis=1)

        model_coeficients = np.matmul(np.linalg.pinv(np.matmul(X.T, X)), np.matmul(X.T, y))  # noqa

        self.weights = model_coeficients[1:]
        self.intercept = model_coeficients[0]

    def predict(self, X):
        return np.dot(X, self.weights) + self.intercept


# ==========================================================================================================================================|
# ===================================================================Ridge_Regression================================================|
# ==========================================================================================================================================|

class Ridge_Regression:  # https://www.youtube.com/watch?v=mpuKSovz9xM&t=866s - digg into

    def __init__(self, _alpha=1.0, _learning_rate=0.01, _iterations=1000):

        self.alpha = _alpha
        self.learning_rate = _learning_rate
        self.iterations = _iterations

    def fit(self, X, y):

        self.weights = np.zeros(X.shape[1])
        self.intercept = 0

        for _ in range(self.iterations):

            y_pred = self.predict(X)
            L2_penalty = (2 * self.alpha * self.weights)

            d_weights_L2 = ((2 * (X.T).dot(y_pred - y)) + L2_penalty)/X.shape[0]  # noqa
            d_intercept = 2*np.sum(y_pred - y)/X.shape[0]

            self.weights -= self.learning_rate * d_weights_L2
            self.intercept -= self.learnilearning_rateg_rate * d_intercept

    def predict(self, X):
        return np.dot(X, self.weights) + self.intercept

# https://www.youtube.com/watch?v=eGXw9n7AnV4

# ==========================================================================================================================================|
# ===================================================================Lasso_Regression================================================|
# ==========================================================================================================================================|


class Lasso_Regression:

    def __init__(self, _alpha=1.0, _learning_rate=0.01, _iterations=1000):

        self.alpha = _alpha
        self.learning_rate = _learning_rate
        self.iterations = _iterations

    def fit(self, X, y):

        self.weights = np.zeros(X.shape[1])
        self.intercept = 0

        for _ in range(self.iterations):

            y_pred = self.predict(X)
            L1_penapty = self.alpha

            d_weights_L1 = ((2 * (X.T).dot(y_pred - y)) + L1_penapty)/X.shape[0]  # noqa
            d_intercept = 2 * np.sum(y_pred - y) / X.shape[0]

            self.weights -= self.learning_rate*d_weights_L1
            self.intercept -= self.learning_rate*d_intercept

    def predict(self, X):
        return np.dot(X, self.weights) + self.intercept

    def get_coefs(self):
        return [self.weights, self.intercept]

# ==========================================================================================================================================|
# ===================================================================Elastic_Net_Regression================================================|
# ==========================================================================================================================================|


class Elastic_Net_Regression:

    def __init__(self, _alpha=1.0, _ratio=0.5, _learning_rate=0.01, _iterations=1000):

        self.alpha = _alpha
        self.learning_rate = _learning_rate
        self.iterations = _iterations
        self.ratio = _ratio

    def fit(self, X, y):

        self.weights = np.zeros(X.shape[1])
        self.intercept = 0

        for _ in range(self.iterations):

            y_pred = self.predict(X)
            L1_panalty = self.alpha * self.ratio
            L2_penalty = (2 * self.alpha*(1 - self.ratio) * self.weights)

            d_weights_L1_L2 = ((2 * (X.T).dot(y_pred - y)) + L1_panalty + L2_penalty) / X.shape[0]  # noqa
            d_intercept = 2 * np.sum(y_pred - y)/X.shape[0]

            self.weights -= self.learning_rate * d_weights_L1_L2
            self.intercept -= self.learning_rate * d_intercept

    def predict(self, X):
        return np.dot(X, self.weights) + self.intercept


# ==========================================================================================================================================|
# ===================================================================Decision_Tree_Regressor================================================|
# ==========================================================================================================================================|

class Node():
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, _variance_reduction=None, *, value=None):

        # for decision node
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.variance_reduction = _variance_reduction

        # for leaf node
        self.value = value

    def _is_leaf_node(self):
        return self.value is not None


class Decision_Tree_Regressor():
    def __init__(self, _min_samples_split=2, _max_depth=100, _n_rand_features=None):

        # tree root
        self.root = None

        # stopping conditions
        self.min_samples_split = _min_samples_split
        self.max_depth = _max_depth
        self.n_rand_features = _n_rand_features

    def _grow_tree(self, dataset, current_depth=0):

        # current node data
        X, y = dataset[:, :-1], dataset[:, -1]
        n_samples, n_features = X.shape
        n_labels = len(np.unique(y))

        # if stopping conditions are met
        if n_samples < self.min_samples_split or current_depth >= self.max_depth or n_labels == 1:
            return Node(value=self._leaf_mean_value(y))

        # rundomly select n_rand_features featurs indexes
        random_features_indexes = np.random.choice(n_features, self.n_rand_features, replace=False)  # noqa

        best_split = self._get_best_split(dataset, random_features_indexes)  # noqa

        if best_split["variance_reduction"] > 0:

            left_subtree = self._grow_tree(best_split["dataset_left"], current_depth+1)  # noqa
            right_subtree = self._grow_tree(best_split["dataset_right"], current_depth+1)  # noqa

            return Node(best_split["feature_index"], best_split["threshold"], left_subtree, right_subtree, best_split["info_gain"])  # noqa

    def _get_best_split(self, dataset, random_features_indexes):

        # dictionary to store the best split

        best_split = {}
        max_variance_reduction = -float("inf")

        # loop over all the features
        for feature_index in random_features_indexes:

            possible_thresholds = np.unique(dataset[:, feature_index])

            for threshold in possible_thresholds:

                dataset_left, dataset_right = self._split(dataset, feature_index, threshold)  # noqa

                if len(dataset_left) > 0 and len(dataset_right) > 0:

                    parent_labels, left_child_labels, right_child_labels = dataset[:, -1], dataset_left[:, -1], dataset_right[:, -1]  # noqa
                    curr_variance_reduction = self._variance_reduction(parent_labels, left_child_labels, right_child_labels, "entropy")  # noqa

                    if curr_variance_reduction > max_variance_reduction:

                        best_split["feature_index"] = feature_index
                        best_split["threshold"] = threshold
                        best_split["dataset_left"] = dataset_left
                        best_split["dataset_right"] = dataset_right
                        best_split["variance_reduction"] = curr_variance_reduction
                        max_variance_reduction = curr_variance_reduction

        return best_split

    def _variance_reduction(self, parent_labels, left_child_labels, right_child_labels):

        weight_l = len(left_child_labels) / len(parent_labels)
        weight_r = len(right_child_labels) / len(parent_labels)
        reduction = np.var(parent_labels) - (weight_l * np.var(left_child_labels) + weight_r * np.var(right_child_labels))  # noqa

        return reduction

    def _split(self, dataset, feature_index, threshold):

        dataset_left = np.array(
            [row for row in dataset if row[feature_index] <= threshold])  # noqa
        dataset_right = np.array(
            [row for row in dataset if row[feature_index] > threshold])  # noqa

        return dataset_left, dataset_right

    def _leaf_mean_value(self, y):
        return np.mean(y)

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


# ===================================================================== TO_DO ======================================

# ==========================================================================================================================================|
# ===================================================================Polynomial_Regression================================================|
# ==========================================================================================================================================|


# https://www.youtube.com/watch?v=H8kocPOT5v0
class Polynomial_Regression():  # https://www.youtube.com/watch?v=QptI-vDle8Y

    def __init__(self, _learning_rate=0.01, _iterations=1000):
        pass

    def fit(self, X, y):
        pass

    def predict(self, X):
        pass

# ==========================================================================================================================================|
# ===================================================================Generalised_Regression================================================|
# ==========================================================================================================================================|


class Generalised_Regression():

    def __init__(self, _learning_rate=0.01, _iterations=1000):
        pass

    def fit(self, X, y):
        pass

    def predict(self, X):
        pass

# ==========================================================================================================================================|
# ===================================================================Bayesian_Regression================================================|
# ==========================================================================================================================================|


class Bayesian_Regression():

    def __init__(self, _learning_rate=0.01, _iterations=1000):
        pass

    def fit(self, X, y):
        pass

    def predict(self, X):
        pass


class Batch_GradientDescent:  # https://www.youtube.com/watch?v=-cs5D91eBLE&list=RDCMUC_lePY0Lm0E2-_IkYUWpI5A&index=3

    def __init__(self, learning_rate=0.001, max_iter=1000, get_log=False):
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.get_log = get_log

    def fit(self, X, y):
        self.W = np.zeros(X.shape[1])
        self.b = 0

        for i in range(self.max_iter):
            y_pred = self.predict(X)

            LW = (2*(X.T).dot(y_pred - y))/X.shape[0]
            Lb = 2*np.sum(y_pred - y)/X.shape[0]

            self.W -= self.learning_rate*LW
            self.b -= self.learning_rate*Lb

            if self.get_log == True:
                if i % 10 == 0:
                    self.y_pred_log.append(y_pred)
                self.loss_log.append(np.mean(np.square(y - y_pred)))

    def predict(self, X):
        return np.dot(X, self.W) + self.b


# https://www.youtube.com/watch?v=IU5fuoYBTAM
class Stochastic_GradientDescent:

    def __init__(self, learning_rate=0.001, max_iter=1000, get_log=False):

        pass

    def fit(self, X, y):
        pass

    def predict(self, X):
        pass


class MiniBatch_GradientDescent:

    def __init__(self, learning_rate=0.001, max_iter=1000, get_log=False):

        pass

    def fit(self, X, y):
        pass

    def predict(self, X):
        pass

