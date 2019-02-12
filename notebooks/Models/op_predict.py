import tensorflow as tf
import numpy as np




def predict_cond_op(op_x):
    op_n_input = 1200
    op_n_hidden1 = 512
    op_n_hidden2 = 256
    op_n_hidden3 = 64
    op_n_output = 4

    op_learning_rate = 1e-4
    op_n_iteration = 31
    op_batch_size = 128
    op_dropout = 0.1

    op_X = tf.placeholder("float", [None, op_n_input])
    op_Y = tf.placeholder("float", [None, op_n_output])
    # keep_prob = tf.placeholder(tf.float32) # used to control the dropout rate

    op_weights = {
        'w1': tf.Variable(tf.truncated_normal([op_n_input, op_n_hidden1], stddev=0.1)),
        'w2': tf.Variable(tf.truncated_normal([op_n_hidden1, op_n_hidden2], stddev=0.1)),
        'w3': tf.Variable(tf.truncated_normal([op_n_hidden2, op_n_hidden3], stddev=0.1)),
        'out': tf.Variable(tf.truncated_normal([op_n_hidden3, op_n_output], stddev=0.1))
    }

    op_biases = {
        'b1': tf.Variable(tf.constant(0.1, shape=[op_n_hidden1])),
        'b2': tf.Variable(tf.constant(0.1, shape=[op_n_hidden2])),
        'b3': tf.Variable(tf.constant(0.1, shape=[op_n_hidden3])),
        'out': tf.Variable(tf.constant(0.1, shape=[op_n_output]))
    }

    op_layer_1 = tf.nn.tanh(tf.add(tf.matmul(op_X, op_weights['w1']), op_biases['b1']))
    op_layer_2 = tf.nn.tanh(tf.add(tf.matmul(op_layer_1, op_weights['w2']), op_biases['b2']))
    op_layer_3 = tf.nn.relu(tf.add(tf.matmul(op_layer_2, op_weights['w3']), op_biases['b3']))
    # layer_drop = tf.nn.dropout(layer_3, keep_prob)
    op_output_layer = tf.nn.leaky_relu(tf.add(tf.matmul(op_layer_3, op_weights['out']), op_biases['out']))

    op_cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=op_Y, logits=op_output_layer))
    op_train_step = tf.train.AdamOptimizer(op_learning_rate).minimize(op_cross_entropy)

    op_correct_pred = tf.equal(tf.argmax(op_output_layer, 1), tf.argmax(op_Y, 1))
    op_accuracy = tf.reduce_mean(tf.cast(op_correct_pred, tf.float32))

    op_init = tf.global_variables_initializer()
    op_sess = tf.Session()
    op_sess.run(op_init)
    
    tf.train.Saver().restore(op_sess, './checkpoints/op/training.ckpt')
    prediction = op_sess.run(tf.argmax(op_output_layer,1), feed_dict={op_X: [op_x]})
    op_sess.close()
    return int(np.squeeze(prediction))