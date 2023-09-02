import numpy as np

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def diff_sigmoid(x):
    return sigmoid(x)*(1-sigmoid(x))
    
def logistic(X, y):
    '''
    LR Logistic Regression.

    INPUT:  X: training sample features, P-by-N matrix.
            y: training sample labels, 1-by-N row vector.

    OUTPUT: w: learned parameters, (P+1)-by-1 column vector.
    '''
    P, N = X.shape
    w = np.zeros((P + 1, 1))
    # YOUR CODE HERE
    # begin answer
    # TODO
    # end answer
   
    training_rate = 0.2
    X = np.vstack((np.ones((1, X.shape[1])), X))

    # Compute the predicted probabilities
    y_pred = sigmoid(np.dot(w.T, X))

    # Compute the gradient of the loss with respect to w
    dw = np.dot(X, 2*(y_pred - y).T)
    
    # Update w
    w -= training_rate * dw

    return w
