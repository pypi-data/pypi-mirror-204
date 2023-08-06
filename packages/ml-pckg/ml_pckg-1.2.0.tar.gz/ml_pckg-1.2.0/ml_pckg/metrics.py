
import numpy as np


class Regressors_Metrics:

    def mean_squared_error(self, y, y_pred):
        return np.mean((y - y_pred) ** 2)

    def SSR(self, y, y_pred):
        return sum((y_pred - y.mean()) ** 2)

    def SSE(self, y, y_pred):
        return sum((y_pred - y) ** 2)

    def SST(self, y, y_pred):
        return self.SSR(y, y_pred) + self.SSE(y, y_pred)

    def mean_absolute_error(self, y, y_pred):
        return np.mean(abs(y - y_pred))

    def root_mean_squared_error(self, y, y_pred):
        return np.sqrt(self.mean_squared_error(y, y_pred))

    def residual_standart_error(self, y, y_pred, p):
        return np.sqrt((self.SSE(y, y_pred) / (len(y) + p + 1)))

    def r_squared(self, y, y_pred):
        return self.SSR(y, y_pred) / self.SST(y, y_pred)


class Classifiers_Metrics:

    def accuracy_score(self, y_true, y_pred):
        return np.sum(y_true == y_pred) / len(y_true)

    def confusion_matrix(self, y_true, y_pred):

        classes = np.unique(np.concatenate((y_true, y_pred)))
        n = len(classes)
        cm = np.zeros(shape=(n, n), dtype=np.int32)
        for i, j in zip(y_true, y_pred):
            cm[np.where(classes == i)[0], np.where(classes == j)[0]] += 1

        return cm

    def precision_score(self, y_true, y_pred, average='auto'):

        classes = np.unique(np.concatenate((y_true, y_pred)))
        if average == 'auto':
            if len(classes) == 2:
                average = 'binary'
            else:
                average = 'micro'

        cm = self.confusion_matrix(y_true, y_pred)
        if average == 'binary':
            tp, fp = cm.ravel()[:2]
            return tp/(tp + fp)

        if average == 'micro':
            tp, fp = list(), list()
            for i in range(len(cm)):
                tp.append(cm[i, i])
                fp.append(sum(np.delete(cm[i], i)))

            tp_all = sum(tp)
            fp_all = sum(fp)
            return tp_all/(tp_all + fp_all)

    def f1_score(self, y_true, y_pred, average='auto'):
        precision = self.precision_score(y_true, y_pred, average)
        recall = self.recall_score(y_true, y_pred, average)
        return 2 * (precision * recall)/(precision + recall)

    def recall_score(self, y_true, y_pred, average='auto'):

        classes = np.unique(np.concatenate((y_true, y_pred)))
        if average == 'auto':
            if len(classes) == 2:
                average = 'binary'
            else:
                average = 'micro'

        cm = self.confusion_matrix(y_true, y_pred)
        if average == 'binary':
            tp, fn = cm.ravel()[[0, 2]]
            return tp/(tp + fn)

        if average == 'micro':
            tp, fn = list(), list()
            for i in range(len(cm)):
                tp.append(cm[i, i])
                fn.append(sum(np.delete(cm[:, i], i)))

            tp_all = sum(tp)
            fn_all = sum(fn)
            return tp_all/(tp_all + fn_all)
