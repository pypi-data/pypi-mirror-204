# Copyright 2023 The Deeper-I Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import os
os.environ['TF_DETERMINISTIC_OPS'] = '0'

import tensorflow as tf



def transform(
    x, 
    bit=1, 
    max_scale=4.0, 
    method='L1', 
    valid=False):
    '''
    x: (h,w,i,o)
    x_mag: (i,o)
    method = 'L1' or 'L2' default=L1

    Map means metrics with extended dimension
    '''
    # Check argument 
    if (bit < 1) or not valid:
        return x
        
    kernel_axis = list(range(len(x.get_shape().dims) - 2))

    ones = tf.ones_like(x, dtype=x.dtype)
    zeros = tf.zeros_like(x, dtype=x.dtype)
    max_scale = tf.constant(max_scale, dtype=x.dtype)
    bit_scale = bit - 1

    # Map of sign - Plus=1, Minus=-1
    x_sign = tf.where(x >= zeros, ones, -ones)

    # Magnitude
    if method =='L2':
        x_mag = tf.reduce_mean(tf.sqrt(tf.square(x)), axis=kernel_axis) # (i,o)
    else:
        x_mag = tf.reduce_mean(tf.abs(x), axis=kernel_axis) # (i,o)

    # Dummy scale
    x_scale = tf.ones_like(x, dtype=tf.int64)

    # No Scale bit
    if bit_scale < 1:
        x_p = tf.where((x >= zeros), x_mag * ones, zeros)
        x_n = tf.where((x < zeros), -x_mag * ones, zeros)
        x = x_p + x_n

    # Scale bit
    else:
        num_scale = tf.pow(2, bit_scale)

        # Map of scale
        map_scale = [] # (i,o,b)
        for i in range(num_scale):
            coeff = tf.cast(tf.pow(0.5, i), x.dtype)
            map_scale.append((max_scale * x_mag * coeff)[..., None])
        map_scale = tf.concat(map_scale, axis=-1)

        # Map of weight
        map_diff = tf.abs(tf.abs(x)[..., None] - map_scale)
        indices = tf.argmin(map_diff, axis=-1)
        map_x = tf.ones_like(map_diff, dtype=x.dtype) * map_scale
        x = tf.gather(map_x, indices, axis=-1, batch_dims=len(x.get_shape().dims)) * x_sign

    return x



def pruning(
    x, 
    valid=False, 
    weight=0.50):
    """
    Pruning optimization
    x: (h,w,i,o)
    o: (h,w,i,o) or (i,o)
    """
    kernel_axis = list(range(len(x.get_shape().dims) - 2))

    x_mag = tf.reduce_mean(tf.abs(x), axis=kernel_axis) # (i,o)
    m_mag = tf.reduce_mean(x_mag, axis=0)[None, :] # (1,o)

    if not valid: 
        return tf.ones_like(x, dtype=x.dtype)

    mask = tf.where(
        tf.less(x_mag, m_mag * weight), 
        tf.zeros_like(x_mag, dtype=x.dtype), 
        tf.ones_like(x_mag, dtype=x.dtype)
    ) # (i,o)

    return mask


def optimization(
    x, 
    use_transform=False, 
    bit=1, 
    max_scale=4.0,
    use_pruning=False, 
    prun_weight=0.50, 
    method='L1',
    ):
    x_tr = transform(
        x, 
        bit=bit, 
        max_scale=max_scale, 
        valid=use_transform,
        method=method,
    )

    x_mask = pruning(x, valid=use_pruning, weight=prun_weight)
    x = x_tr * x_mask

    return x


