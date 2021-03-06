import latticex.rosetta as rtt  # difference from tensorflow
import math
import os
import sys
import csv
import tensorflow as tf
import numpy as np
from util import read_dataset, savecsv

np.set_printoptions(suppress=True)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

np.random.seed(0)

EPOCHES = 100
BATCH_SIZE = 16
learning_rate = 0.0002

# real data
# ######################################## difference from tensorflow
file_x = '../dsets/P' + str(rtt.mpc_player.id) + "/cls_train_x.csv"
file_y = '../dsets/P' + str(rtt.mpc_player.id) + "/cls_train_y.csv"
real_X, real_Y = rtt.MpcDataSet(label_owner=0).load_XY(file_x, file_y)
# ######################################## difference from tensorflow
DIM_NUM = real_X.shape[1]

X = tf.placeholder(tf.float64, [None, DIM_NUM])
Y = tf.placeholder(tf.float64, [None, 1])
print(X)
print(Y)

# initialize W & b
W = tf.Variable(tf.zeros([DIM_NUM, 1], dtype=tf.float64))
b = tf.Variable(tf.zeros([1], dtype=tf.float64))
print(W)
print(b)

# predict
pred_Y = tf.sigmoid(tf.matmul(X, W) + b)
print(pred_Y)

# loss
logits = tf.matmul(X, W) + b
loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=Y, logits=logits)
loss = tf.reduce_mean(loss)
print(loss)

# optimizer
train = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)
print(train)

init = tf.global_variables_initializer()
print(init)

# ########### for test, reveal
reveal_W = rtt.MpcReveal(W)
reveal_b = rtt.MpcReveal(b)
reveal_Y = rtt.MpcReveal(pred_Y)
# ########### for test, reveal

# #############################################################
# save to csv for comparing, for debug
if rtt.mpc_player.id == 0:
    scriptname = os.path.basename(sys.argv[0]).split(".")[0]
    csvprefix = "./log/" + scriptname
    os.makedirs(csvprefix, exist_ok=True)
    csvprefix = csvprefix + "/rtt"
# #############################################################


with tf.Session() as sess:
    sess.run(init)
    rW, rb = sess.run([reveal_W, reveal_b])
    print("init weight:{} \nbias:{}".format(rW, rb))

    # train
    BATCHES = math.ceil(len(real_X) / BATCH_SIZE)
    for e in range(EPOCHES):
        for i in range(BATCHES):
            bX = real_X[(i * BATCH_SIZE): (i + 1) * BATCH_SIZE]
            bY = real_Y[(i * BATCH_SIZE): (i + 1) * BATCH_SIZE]
            sess.run(train, feed_dict={X: bX, Y: bY})

            j = e * BATCHES + i
            if j % 50 == 0 or (j == EPOCHES * BATCHES - 1 and j % 50 != 0):
                rW, rb = sess.run([reveal_W, reveal_b])
                print("I,E,B:{:0>4d},{:0>4d},{:0>4d} weight:{} \nbias:{}".format(
                    j, e, i, rW, rb))
                if rtt.mpc_player.id == 0:
                    savecsv("{}-{:0>4d}-{}.csv".format(csvprefix, j, "W"), rW)
                    savecsv("{}-{:0>4d}-{}.csv".format(csvprefix, j, "b"), rb)

    # predict
    Y_pred = sess.run(reveal_Y, feed_dict={X: real_X, Y: real_Y})
    if rtt.mpc_player.id == 0:
        print("Y_pred:", Y_pred)
        savecsv("{}-pred-{}.csv".format(csvprefix, "Y"), Y_pred)
