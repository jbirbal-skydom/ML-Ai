# import the necessary packages
from keras.models import Sequential
from keras.layers import Flatten
from keras.layers import Dense


class FullyConnected:
    @staticmethod
    def build(states, height, depth, actions):
        # initialize the model along with the input shape to be
        # # "channels last"
        model = Sequential()
        model.add(Flatten(input_shape = (1, states)))
        #build the amount of 
        for i in range(depth):                
            # define the first (and only) CONV => RELU layer
            model.add(Dense(height, activation='relu'))

        model.add(Dense(actions, activation='linear'))
        return model