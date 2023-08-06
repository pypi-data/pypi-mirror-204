
import numpy as np


def accuracy_score(y_true, y_pred):
    return np.sum(y_true == y_pred) / len(y_true)


def mean_squared_error(y, y_pred):
    return np.mean((y - y_pred) ** 2)


def SSR(y, y_pred):
    return sum((y_pred - y.mean()) ** 2)


def SSE(y, y_pred):
    return sum((y_pred - y) ** 2)


def SST(y, y_pred):
    return SSR(y, y_pred) + SSE(y, y_pred)


def mean_absolute_error(y, y_pred):
    return np.mean(abs(y - y_pred))


def root_mean_squared_error(y, y_pred):
    return np.sqrt(mean_squared_error(y, y_pred))


def residual_standart_error(y, y_pred, p):
    return np.sqrt((SSE(y, y_pred) / (len(y) + p + 1)))


def r_squared(y, y_pred):
    return SSR(y, y_pred) / SST(y, y_pred)


def confusion_matrix(y_true, y_pred):

    classes = np.unique(np.concatenate((y_true, y_pred)))
    n = len(classes)
    cm = np.zeros(shape=(n, n), dtype=np.int32)
    for i, j in zip(y_true, y_pred):
        cm[np.where(classes == i)[0], np.where(classes == j)[0]] += 1

    return cm


def f1_score(y_true, y_pred, average='auto'):
    precision = precision_score(y_true, y_pred, average)
    recall = recall_score(y_true, y_pred, average)
    return 2 * (precision * recall)/(precision + recall)


def precision_score(y_true, y_pred, average='auto'):

    classes = np.unique(np.concatenate((y_true, y_pred)))
    if average == 'auto':
        if len(classes) == 2:
            average = 'binary'
        else:
            average = 'micro'

    cm = confusion_matrix(y_true, y_pred)
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


def recall_score(y_true, y_pred, average='auto'):

    classes = np.unique(np.concatenate((y_true, y_pred)))
    if average == 'auto':
        if len(classes) == 2:
            average = 'binary'
        else:
            average = 'micro'

    cm = confusion_matrix(y_true, y_pred)
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
