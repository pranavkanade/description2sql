import tensorflow as tf
import numpy as np

n_input = 1500
n_hidden1 = 1024
n_hidden2 = 512
n_hidden3 = 64
n_output = 6

learning_rate = 1e-4
n_iteration = 11
batch_size = 128
dropout = 0.1

X = tf.placeholder("float", [None, n_input])
Y = tf.placeholder("float", [None, n_output])
# keep_prob = tf.placeholder(tf.float32) # used to control the dropout rate

weights = {
    'w1': tf.Variable(tf.truncated_normal([n_input, n_hidden1], stddev=0.1)),
    'w2': tf.Variable(tf.truncated_normal([n_hidden1, n_hidden2], stddev=0.1)),
    'w3': tf.Variable(tf.truncated_normal([n_hidden2, n_hidden3], stddev=0.1)),
    'out': tf.Variable(tf.truncated_normal([n_hidden3, n_output], stddev=0.1))
}

biases = {
    'b1': tf.Variable(tf.constant(0.1, shape=[n_hidden1])),
    'b2': tf.Variable(tf.constant(0.1, shape=[n_hidden2])),
    'b3': tf.Variable(tf.constant(0.1, shape=[n_hidden3])),
    'out': tf.Variable(tf.constant(0.1, shape=[n_output]))
}

layer_1 = tf.nn.tanh(tf.add(tf.matmul(X, weights['w1']), biases['b1']))
layer_2 = tf.nn.tanh(tf.add(tf.matmul(layer_1, weights['w2']), biases['b2']))
layer_3 = tf.nn.relu(tf.add(tf.matmul(layer_2, weights['w3']), biases['b3']))
# layer_drop = tf.nn.dropout(layer_3, keep_prob)
output_layer = tf.nn.leaky_relu(tf.add(tf.matmul(layer_3, weights['out']), biases['out']))

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=Y, logits=output_layer))
train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)

correct_pred = tf.equal(tf.argmax(output_layer, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

def predict_agg(agg_X):
    tf.train.Saver().restore(sess, './checkpoints/agg/training.ckpt')
    prediction = sess.run(tf.argmax(output_layer,1), feed_dict={X: [agg_X]})
    return int(np.squeeze(prediction))