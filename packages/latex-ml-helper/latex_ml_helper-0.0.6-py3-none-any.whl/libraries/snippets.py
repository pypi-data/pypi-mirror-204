from libraries.copy import copy_text

def Imports(copy = False):
    text = """
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, make_regression, load_digits
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Perceptron
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression, LinearRegression, RidgeClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix, mean_squared_error
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
"""
    return copy_text(text, copy)

def Grad(copy = False):
    text = """
m, n = 100, 5
X, y = make_regression(n_samples=m, n_features=n, noise=0.1)
h = lambda x, theta : np.dot(x, theta)
J = lambda X, y, theta : np.sum(np.square(h(X, theta) - y)) / (1 / 2 * m)
learning_rate = 0.01
it = 500

def gradiental_method(X, y, learning_rate, it):
    m, n = X.shape
    one_x = [np.insert(x, 0, 1) for x in X]
    theta = np.random.rand(n + 1)
    cost = []

    for i in range(it):
        a = sum([h(one_x[i], theta) - y[i] for i in range(m)]) / m
        b = [sum([(h(one_x[i], theta) - y[i]) * X[i][j - 1] for i in range(m) if i != 0]) / m for j in range(n + 1) if j != 0]
        grad = np.array([a] + b)
        cost.append(J(one_x, y, theta))
        theta = np.subtract(theta, learning_rate * grad)
    
    return theta, cost

theta, cost = gradiental_method(X, y, learning_rate, it)
x_axis = range(len(cost))
plt.plot(X, y, "o")
plt.show()
plt.plot(x_axis, cost)
plt.show()
#
#def gradient_method(X, y, lmbd, lr=0.1, num_iter=50000):
#    print(f'Starting gradient descent with learning rate {lr}, regularization parameter {lmbd} and {num_iter} iterations')
#    m, n = X.shape
#    theta = np.zeros(X.shape[1]).reshape(-1, 1)
#    loss = np.empty(num_iter)
#    for it in range(num_iter):
#        loss[it] = (0.5 / m) * np.sum(np.square(X @ theta - y))
#        grad = (1.0 / m) * ((X @ theta - y).T @ X).reshape(-1, 1)
#        theta[0] = theta[0] - lr * grad[0]
#        theta[1:] = theta[1:] *  (1 - lr * lmbd / m) - lr * grad[1:]
#    return theta, loss
"""
    return copy_text(text, copy)

def Loss(copy = False):
    text = """
m_test, n_test = X_test.shape
one_x = [np.insert(x, 0, 1) for x in X_test]
predictions = h(one_x, theta)
loss = 0
for i, prediction in enumerate(predictions):
    loss += (prediction -  y_test[i])**2
print(f'Loss: {loss[0] / (2 * m)}')
#
loss = 0
for i, prediction in enumerate(lr.predict(X_test)):
    loss += (prediction -  y_test[i])**2
print(f'Sklearn loss {loss[0] / (2 * m)}')
"""
    return copy_text(text, copy)

def Perc(copy = False):
    text = """
X = np.array([[2, -2], [1, -3], [-1, -3], [-3, -1], [-2, 2], [-1, 3], [1, 3], [4, 1]])
y = np.array([1, 1, 1, 1, -1, -1, -1, -1])
theta = np.array([0, 1, -1])

good = False
while not good:
    good = True
    for i in range(m):
        #print(y[i] * (np.dot(theta[1:], X[i]) + theta[0]))
        if (y[i] * (np.dot(theta[1:], X[i]) + theta[0]) <= 0):
            theta[1:] += y[i] * X[i]
            good = False
            print(i, X[i])
print(theta)

plt.scatter(X[:, 0], X[:, 1], c=y)
xx = np.linspace(-4, 4, 1000)
yy = -theta[0] / theta[2] - theta[1] / theta[2] * xx
plt.plot(xx, yy)
plt.show()
#
class Perceptron:
    def __init__(self, X, y, learning_rate=0.01, n_iter=100):
        self.learning_rate = learning_rate
        self.n_iter = n_iter
        self.X = X
        self.y = y
        self.theta = None
        self.k_total = None
    
    def fit(self):
        m = self.X.shape[0]
        n = self.X.shape[1] + 1

        self.theta = np.random.rand(n)

        X = np.concatenate((np.ones((m, 1)), self.X), axis=1)

        self.k_total = 0
        while self.k_total < self.n_iter:
            k = 0            
            for i in range(m):
                if np.dot(self.theta, X[i]) * self.y[i] <= 0:
                    k += 1
                    self.theta += self.learning_rate * self.y[i] * X[i]
                    plt.plot(self.X[i][0], self.X[i][1], marker=1)
                else:
                    plt.scatter(self.X[i][0], self.X[i][1], marker="+")
            self.k_total += k

            if k == 0:
                break
            plt.show()

        print(self.X[0])

    def accuracy(self, X, y):
        m = X.shape[0]
        X = np.concatenate((np.ones((m, 1)), X), axis=1)

        y_pred = np.sign(np.dot(X, self.theta))

        return np.sum(y_pred == y) / m

    def draw(self, hiperplane=True):
        plt.scatter(self.X[:, 0], self.X[:, 1], c=self.y)

        if hiperplane:
            x1 = np.linspace(self.X[:, 0].min(), self.X[:, 0].max(), 100)
            x2 = -(self.theta[0] + self.theta[1] * x1) / self.theta[2]
            plt.plot(x1, x2, 'r')
            
        plt.show()    
"""
    return copy_text(text, copy)

def SVM_Line(copy = False):
    text = """
theta_0 = -0.5
theta = np.array([1, 1])
xx = np.linspace(-0.5, 1.5, 100)
yy = -(theta[0] / theta[1]) * xx - theta_0 / theta[1]
#
xx = np.linspace(np.min(X)-1, np.max(X)+1, 1000)
yy = -(model.coef_[0][0] / model.coef_[0][1]) * xx - (model.intercept_ / model.coef_[0][1])
"""
    return copy_text(text, copy)

def SVM_Margin(copy = False):
    text = """
X, y = make_blobs(n_samples=40, centers=2, random_state=1)
clf = LinearSVC(random_state=0).fit(X, y)
dec_func = clf.decision_function(X)
support_vector_indices = np.where(np.abs(dec_func) <= 1 + 1e-15)
support_vectors = X[support_vector_indices]
#plt.scatter(X_a[:, 0], X_a[:, 1], c=y_a)
#ax = plt.gca()
#xlim = ax.get_xlim()
#ylim = ax.get_ylim()
#xx, yy = np.meshgrid(np.linspace(xlim[0], xlim[1], 1000), np.linspace(ylim[0], ylim[1], 1000))
#Z = clf_a.decision_function(np.c_[xx.ravel(), yy.ravel()])
#Z = Z.reshape(xx.shape)
#plt.contour(xx, yy, Z, levels=[-1,0,1], alpha=0.5, linestyles=['--', '-', '--'])
#plt.scatter(complete_vector[:, 0], complete_vector[:, 1], s=100, marker='*', color='red')
"""

    return copy_text(text, copy)

def Contour(copy = False):
    text = """
plt.scatter(X[:, 0], X[:, 1], c=y)
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()
xx, yy = np.meshgrid(np.linspace(xlim[0], xlim[1], 1000), np.linspace(ylim[0], ylim[1], 1000))
Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
#Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.contourf(xx, yy, Z, cmap='spring', alpha=0.2)
#plt.contourf(xx, yy, Z, levels=[-100, -1,0,1, 100], alpha=0.5, linestyles=['--', '-', '--'])
#plt.scatter(support_vectors[:, 0], support_vectors[:, 1], s=100, linewidth=1, facecolors='none', edgecolors='k')    
"""

    return copy_text(text, copy)

def Scaler(copy = False):
    text = """
scaler = preprocessing.StandardScaler()
scaler.fit(X_train, y_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
"""
    return copy_text(text, copy)

def SoftMax(copy = False):
    text = """
def softmax(x):
    expd = np.exp(x)
    return expd / np.sum(expd)

X = np.array([[1, 5, -2, 3], [1, 1, 1, 1], [5, 3, 2, 2], [8, 0, 1, 2]])
y_true = np.array([0, 1, 2, 1])
theta = np.array([[1, 0.5, 0.2], [2, 0.2, 0.3], [1, 3, 0.4], [2, 1, 0.5]])
res = theta.T @ X.T

y_pred = []
for i in range(4):
    sm = softmax(res[:, i])
    y_pred.append(np.argmax(sm))
    print(sm, np.argmax(sm))
y_pred = np.array(y_pred)
print(confusion_matrix(y_true, y_pred))
"""
    return copy_text(text, copy)

def Pip(copy = False):
    text = """
!pip install --upgrade pip
!pip install ipykernel
!pip install numpy
!pip install pandas
!pip install scikit-learn
!pip install matplotlib
"""

    return copy_text(text, copy)

def HelpSnippets(copy = False):
    text = """
Imports <- Importi
Loss <- Loss funkcija
Perc <- Perceptron algoritam
SVM_Line <- Support Vector Machine sa linijom
SVM_Margin <- Support Vector Machine sa marginom
Contour <- Konture
Scaler <- Skaliranje
SoftMax <- SoftMax
Pip <- Instalacija paketa
"""
    return copy_text(text, copy)