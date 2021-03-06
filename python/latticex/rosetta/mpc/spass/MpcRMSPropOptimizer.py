# ==============================================================================
# Copyright 2020 The LatticeX Foundation
# This file is part of the Rosetta library.
#
# The Rosetta library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The Rosetta library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with the Rosetta library. If not, see <http://www.gnu.org/licenses/>.
# =============================================================================="
import tensorflow as tf


class MpcRMSPropOptimizer(tf.train.RMSPropOptimizer):
    """
    # mpc RMSProp optimizer, only override __init__ & minimize functions
    """

    def __init__(self, learning_rate, decay=0.9, momentum=0.0, epsilon=1e-10,
                 use_locking=False, name="RMSProp"):
        """
        # Construct a new mpc RMSProp optimizer.
        """
        super(tf.train.RMSPropOptimizer, self).__init__(learning_rate, decay, momentum,
                                                        epsilon, use_locking, name)


    def minimize(self, loss, global_step=None, var_list=None,
                 gate_gradients=1, aggregation_method=None,
                 colocate_gradients_with_ops=False, name=None,
                 grad_loss=None):

        raise NotImplementedError("Now, RMSPropOptimizer is not supported!")


# assign mpc RMSProp optimizer to RMSProp optimizer,
# now, the tf default RMSProp optimizer is mpc RMSProp optimizer
tf.train.RMSPropOptimizer = MpcRMSPropOptimizer


# for testing
if __name__ == "__main__":
    # linear model
    X = tf.Variable(1.0, name='x')
    W = tf.Variable(2.0, name='weight')
    b = tf.Variable(3.0, name='bias')
    Loss = tf.multiply(X, W) + b
    train_step = tf.train.RMSPropOptimizer(0.01).minimize(Loss)
