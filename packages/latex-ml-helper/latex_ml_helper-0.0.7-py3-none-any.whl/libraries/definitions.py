def PerceptronDef():
    return r"""
$h_{\theta}(X) = \text{sign}(\theta^TX)$

$J(\theta) = \frac{1}{m} \sum_{i=1}^{m}(1-\delta(y^{(i)},h_{\theta}(x^{(i)}))) \\ \delta(x, y)=\begin{cases} 1 & \text{, } x=y \\ 0 & \text{, } x\neq y \end{cases}$
"""

def SVMDef():
    return r"""
$h_{\theta}(X) = \text{sign}(\theta^TX)$
$J(\theta) = \frac{1}{m}\sum_{i=1}^ml(y^{(i)}\theta^Tx^{(i)}) \\ l(x)=max(1,1-x) \ \text{(hinge-loss funkcija)}$
Maksimizacija margina
$$
 \textrm{argmax}_{\gamma, \Theta}\frac{\gamma}{||\Theta||}
 $$
 $$
 \text{  uz uvjet  } y^{(i)}\Theta^T x^{(i)} \geq \gamma, \text{ }  i = 1, 2, \dots, m,
 $$
 $$
 \textrm{argmin}_{\gamma, \Theta}\frac{1}{2}\left(\frac{||\Theta||}{\gamma}\right)^2
 $$
 $$
 \text{  uz uvjet  } y^{(i)}\Theta^T x^{(i)} \geq \gamma, \text{ }  i = 1, 2, \dots, m,
 $$
 $$
 \textrm{argmin}_{\Theta}\frac{1}{2}||\Theta||^2
 $$
 $$
 \text{  uz uvjet  } y^{(i)}\Theta^T x^{(i)} \geq 1, \text{ }  i = 1, 2, \dots, m,
 $$
 Hiperravnina ne prolazi ishodistem
 $$
 \textrm{argmin}_{\Theta, \theta_0}\frac{1}{2}||\Theta||^2
 $$
 $$
 \text{  uz uvjet  } y^{(i)}(\Theta^T x^{(i)} + \theta_0) \geq 1, \text{ }  i = 1, 2, \dots, m,
 $$
 Podaci nisu linearno separablini
 $$
 \textrm{argmin}_{\Theta, \theta_0, \xi_i}\frac{1}{2}||\Theta||^2 + C\sum\limits_{i=1}^m \xi_i
 $$
 
 $$
 \text{  uz uvjet  } y^{(i)}(\Theta^T x^{(i)} + \theta_0) \geq 1 - \xi_i \textrm{ i } \xi_i \geq 0, \text{ }  i = 1, 2, \dots, m,
 $$

Regularizacija
$$
\textrm{argmin}_{\Theta, \theta_0, \xi}\frac{1}{2}||\Theta||^2 + C\sum\limits_{i=1}^m \xi_i
$$
uz uvjet
$$
\text{  uz uvjet  } y^{(i)}(\Theta^T x^{(i)} + \theta_0) \geq 1 - \xi_i \textrm{ i } \xi_i \geq 0, \text{ }  i = 1, 2, \dots, m,
$$
Bezuvjetna optimizacija
$$
\textrm{argmin}_{\Theta, \theta_0}\lambda||\Theta||^2 + \frac{1}{m}\sum\limits_{i=1}^m\ell_{hinge}(y^{(i)}(\Theta^T x^{(i)} + \theta_0)).
$$
"""

def LogisticRegressionDef():
    return r"""
$h_{\Theta}(x) = \sigma(\Theta^Tx) = \frac{1}{1+\exp{(-\Theta^Tx)}}$


$J(\Theta) = \sum_{i=1}^m\log{}(1 + \exp(-y^{(i)}\Theta^Tx^{(i)}))$

$J(\Theta, \theta_0) = \frac{1}{m}\sum\limits_{i=1}^{m}\left[-y^{(i)}\log{(h_{\Theta, \theta_0}(x^{(i)}))}-(1-y^{(i)})\log{(1-h_{\Theta, \theta_0}(x^{(i)}))}\right] + \frac{\lambda}{2}||\Theta||^2$
"""

def LinearRegressionDef():
    return r"""
$h_{\Theta, \theta_0}(x) = \theta_0 + \theta_1 x_1 + \dots + \theta_n x_n$


$J(\Theta, \theta_0) = \frac{1}{2m}\sum\limits_{i=1}^m (h_{\Theta, \theta_0}(x^{(i)}) - y^{(i)})^2$


$J(\Theta) = \frac{1}{2m}\sum\limits_{i=1}^m (h_{\Theta, \theta_0}(x^{(i)}) - y^{(i)})^2 + \lambda\sum_{i=1}^{m}\theta^2_i$
"""

def PolinomialRegressionDef():
    return r"""
$h_{\theta}(x)=\theta_0 + \sum_{i=1}^{m}\theta_ix_i$

$\frac{1}{2m}\sum\limits_{i=1}^m (h_{\Theta}(x^{(i)}) - y^{(i)})^2$

$\frac{1}{2}\sum\limits_{i=1}^m (h_{\Theta}(x^{(i)}) - y^{(i)})^2 + \frac{\lambda}{2}\Theta^T\Theta$
"""

def SoftmaxDef():
    return r"""
$h_{\theta}(x)=\sigma(\theta^Tx) \\ \sigma(z)_j=\frac{e^{z_j}}{\sum_{l=1}^{k}e^{z_l}}$

$P(Y|X;\theta) = \prod_{i=1}^mP(y^{(i)}|x^{(i)}; \theta) \to \mathrm{max}_{\theta} \ \text{(Max-likelyhood funkcija)}$

$-\log{}P(Y|X;\theta) = -\sum_{i=1}^m\log{}P(y^{(i)}|x^{(i)}; \theta) \to \mathrm{min}_{\theta}$
"""

def GradientPseudo():
    return """
def grad_method(X, y, theta, iterations):
    for i in range(iterations):
        grad <- derivacije od j po theta
        theta <- theta - alpha * grad

    return theta
"""

def PerceptronPseudo():
    return """
def perceptron(X, y, theta):
    good = False

    while not good: <- terminira se u slucaju da su podaci linearno separabilni
        good = True

        for i in range(len(X)): <- prolazak kroz sve podatke
            if y[i] * (X[i] @ theta) <= 0: <- uvijet azuriranja
                theta += y[i] * X[i] <- korak azuriranja
                good = False

    return theta
"""

def HelpDef():
    return """
PerceptronDef() - perceptron model, cost
SVMDef() - SVM model, cost, margine
LogisticRegressionDef() - logistic regression model, cost, cost regularizacija
LinearRegressionDef() - linear regression model, cost, cost regularizacija
PolinomialRegressionDef() - polinomial regression model, cost, cost regularizacija
SoftmaxDef() - softmax model, cost (Max-likelyhood)
GradientPseudo() - pseudokod za gradientntalnu metodu
PerceptronPseudo() - pseudokod za perceptron algoritam
"""
