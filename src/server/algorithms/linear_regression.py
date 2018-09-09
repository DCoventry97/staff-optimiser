from __future__ import print_function

import tensorflow as tf
import numpy
from src.server.rest import read_user_data
rng = numpy.random


class LinearRegression:

    # Initialise object with username to query
    def __init__(self, username):
        self.username = username

        # Parameters
        learning_rate = 0.01
        training_epochs = 1000
        display_step = 50

        #Get Training Data From XML File
        train_X, train_Y = read_user_data.read(username)
        train_X = numpy.asarray(train_X)
        train_Y = numpy.asarray(train_Y)
        n_samples = train_X.shape[0]

        # tf Graph Input
        X = tf.placeholder("float")
        Y = tf.placeholder("float")

        # Set model weights
        W = tf.Variable(rng.randn(), name="weight")
        b = tf.Variable(rng.randn(), name="bias")

        # Construct a linear model
        pred = tf.add(tf.multiply(X, W), b)

        # Mean squared error
        cost = tf.reduce_sum(tf.pow(pred-Y, 2))/(2*n_samples)
        # Gradient descent
        #  Note, minimize() knows to modify W and b because Variable objects are trainable=True by default
        optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

        # Initialize the variables (i.e. assign their default value)
        init = tf.global_variables_initializer()



        # Start training
        with tf.Session() as sess:

            # Run the initializer
            sess.run(init)

            # Fit all training data
            for epoch in range(training_epochs):
                for (x, y) in zip(train_X, train_Y):
                    sess.run(optimizer, feed_dict={X: x, Y: y})

                # Display logs per epoch step
                if (epoch+1) % display_step == 0:
                    c = sess.run(cost, feed_dict={X: train_X, Y:train_Y})
                    print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(c), \
                        "W=", sess.run(W), "b=", sess.run(b))

            print("Optimization Finished!")
            training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
            print("Training cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n')

            return sess.run(W)
