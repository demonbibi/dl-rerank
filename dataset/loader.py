import json
import os

import tensorflow as tf
from tensorflow import feature_column as fc


class DataLoader(object):
    """load tfrecord format data set


    tf-record dataset path config
      hdfs_dir
         |-- train
         |      |-- part-00000
         |
         |-- eval
         |      |-- part-00000
         |
    """

    def __init__(self, features_config):
        self.columns = [x for _, x in features_config.get_feature_columns().items()]
        print(self.columns)

    def load_data(self, file_dir, batch_size=512):
        shard_num, shard_id = self.get_shard_info()
        files = tf.data.Dataset.list_files(os.path.join(file_dir, 'part-*'))
        files = files.shard(shard_num, shard_id)
        return files.flat_map(lambda tf_file: self.load_file(tf_file, batch_size))

    def get_shard_info(self):
        tf_config = os.environ.get('TF_CONFIG', None)
        if tf_config is None:
            return 1, 0

        config = json.loads(tf_config)
        worker_num = len(config['cluster']['worker'])
        chief_num = len(config['cluster']['chief'])
        shard_num = worker_num + chief_num
        if config['task']['type'] == 'chief':
            shard_id = 0
        elif config['task']['type'] == 'worker':
            shard_id = config['task']['index'] + 1
        elif config['task']['type'] == 'evaluator':
            shard_num = 1
            shard_id = 0
        else:
            raise ValueError('invalid get_shard_info apply logic')
        return shard_num, shard_id

    def load_file(self, tf_file, batch_size):
        dataset = tf.data.TFRecordDataset(tf_file, buffer_size=256*1024*1024)
        dataset = dataset.shuffle(buffer_size=batch_size*10, reshuffle_each_iteration=True)
        parse_spec = fc.make_parse_example_spec(self.columns)
        dataset = dataset.map(map_func=lambda x: self.parse_example(x, parse_spec), num_parallel_calls=8)
        dataset = dataset.batch(batch_size=batch_size)
        dataset = dataset.prefetch(buffer_size=batch_size*10)
        return dataset

    def parse_example(self, serialized, columns):
        features = tf.io.parse_example(serialized=serialized, features=columns)
        label = tf.expand_dims(tf.sparse.to_dense(features.pop('label')), axis=-1)
        return features, label

#
# from feature.feature_config import FeatureConfig
# from pathlib import Path
#
# tf.compat.v1.disable_eager_execution()
#
# root_path = Path(__file__).parent.parent
# config_dir = os.path.join(root_path, 'resources/config')
# vocab_dir = os.path.join(root_path, 'resources/vocab')
# feature_config = FeatureConfig(config_dir, vocab_dir)
# data_loader = DataLoader(feature_config)
# tf.compat.v1.enable_eager_execution()
#
#
# file_dir = os.path.join(root_path, 'resources/train')
# vocab_dir = os.path.join(root_path, 'resources/vocab')
# dataset = data_loader.load_data(file_dir, 2)
#
# dataset_iter = iter(dataset)
# features, label = next(dataset_iter)
#
# feature_columns = feature_config.get_feature_columns()
#
# print('item.cate_ids')
# columns = [feature_columns.get('item.cate_ids')]
# layer = tf.keras.experimental.SequenceFeatures(columns)
# embedding, _ = layer(features)
# print(embedding)
#
# print('user.visited_cate_ids')
# columns = [feature_columns.get('user.visited_cate_ids')]
# layer = tf.keras.experimental.SequenceFeatures(columns)
# embedding, _ = layer(features)
# print(embedding)
#
# print('label')
# print(label)

