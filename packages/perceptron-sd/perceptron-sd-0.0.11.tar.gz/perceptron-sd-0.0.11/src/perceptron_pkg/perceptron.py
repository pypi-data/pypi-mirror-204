import os
import numpy as np
import joblib

class Perceptron:
    def __init__(self, learning_rate:float=None, epochs:int=None ):
        self.weights = np.random.randn(3) * 1e-4 #(small random weights)
        training = (learning_rate is not None) and (epochs is not None)
        if training:
            print(f"Initial weights before training: {self.weights}")
        self.learning_rate = learning_rate
        self.epochs = epochs
        
    def _z_outcome(self,inputs,weights):
        return np.dot(inputs,weights)
        
    def activation_function(self,z ):
        return np.where(z>0, 1, 0)
    
    def fit(self, X, y):
        self.X = X
        self.y = y        
        X_with_bias = np.c_[self.X, -np.ones((len(self.X),1))] #line ##
        print(f"X with bias : \n{X_with_bias}")
        
        for epoch in range(self.epochs):
            print("--"*10)
            print(f"for epoch >>{epoch+1}")
            print("--"*10)
            
            z =  self._z_outcome(X_with_bias, self.weights)
            y_hat = self.activation_function(z)
            print(f"predicted value after forward pass \n{y_hat}")  
            
            self.error = self.y-y_hat
            print(f"error \n{self.error}")
            
            print(f"epoch loss: \n {np.sum(self.error)}")
            
            self.weights = self.weights + \
                self.learning_rate*np.dot(X_with_bias.T,self.error)
            print(f"updated weights after epoch {epoch+1}\
                  /{self.epochs} is \n{self.weights}")
            
            print("##"*10)
            
    def predict(self,test_input):
        X_with_bias = np.c_[test_input, \
                            -np.ones((len(test_input),1))] \
                                #user testinput remove self.X from line ##
        z =  self._z_outcome(X_with_bias, self.weights)
        return self.activation_function(z)

    def total_loss(self):
        total_loss = np.sum(self.error)
        print(f"\n total loss {total_loss}\n")
        return total_loss

    def _create_dir_return_path(self, model_dir, filename):
        os.makedirs(model_dir, exist_ok = True)
        return os.path.join(model_dir, filename)

    def save(self, filename, model_dir = None):
        if model_dir is not None:
            model_file_path = self._create_dir_return_path(model_dir, filename)
        else:
            model_file_path = self._create_dir_return_path("model", filename)
        joblib.dump(self, model_file_path)

    def load(self, filepath):
        return joblib.load(filepath)
    