import unittest
import sys
from ModelDbSyncerTest import SyncerTest

import modeldb.tests.utils as utils
from modeldb.thrift.modeldb import ttypes as modeldb_types
from modeldb.sklearn_native.ModelDbSyncer import *

from sklearn import linear_model
from sklearn import preprocessing
import pandas as pd

class TestTransformEvent(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        name = "logistic-test"
        author = "srinidhi"
        description = "income-level logistic regression"
        SyncerObj = SyncerTest(
            NewOrExistingProject(name, author, description),
            DefaultExperiment(),
            NewExperimentRun("Abc"))
        letters = ['A', 'B', 'C', 'D']
        X = np.random.choice(letters, size=(100, 1)).ravel()
        model = preprocessing.LabelEncoder()
        model.tag("label encoder")
        SyncerTest.instance.clearBuffer()
        model.fitSync(X)
        model.transformSync(X)
        events = SyncerTest.instance.sync()
        self.fitEvent = events[0]
        self.transformEvent = events[1]

    # Tests Transformer values.
    def test_transformer_construction(self):
        utils.validate_transform_event_struct(self.transformEvent, self)
        transformer = self.transformEvent.transformer
        expected_transformer = modeldb_types.Transformer(
            -1,
            [0.0],
            'LabelEncoder',
            'label encoder')
        utils.is_equal_transformer(transformer, expected_transformer, self)

    # Tests values of old dataframe of TransformEvent object.
    def test_old_dataframe(self):
        old_df = self.transformEvent.oldDataFrame
        utils.validate_dataframe_struct(old_df, self)
        expected_old_df = modeldb_types.DataFrame(
            -1,
            [],
            100,
            '')
        utils.is_equal_dataframe(expected_old_df, old_df, self)

    # Tests values of new dataframe of TransformEvent object.
    def test_new_dataframe(self):
        new_df = self.transformEvent.newDataFrame
        utils.validate_dataframe_struct(new_df, self)

        new_df_column = new_df.schema[0]
        df_column = modeldb_types.DataFrameColumn(
            '0',
            'int64'
            )
        expected_new_df = modeldb_types.DataFrame(
            -1,
            [df_column],
            100,
            '') # fix columns
        utils.is_equal_dataframe(expected_new_df, new_df, self)

    # Tests TransformerSpec values
    def test_transformer_spec_construction(self):
        spec = self.fitEvent.spec
        utils.validate_transformer_spec_struct(self.fitEvent.spec, self)
        expected_spec = modeldb_types.TransformerSpec(
            -1, 
            'LabelEncoder',
            [],
            [],
            'label encoder') # Fix hyperparams.
        utils.is_equal_transformer_spec(expected_spec, spec, self)

    # Tests DataFrame values, associated with FitEvent
    def test_dataframe_fit_event(self):
        df = self.fitEvent.df
        utils.validate_dataframe_struct(df, self)
        expected_df = modeldb_types.DataFrame(
            -1,
            [],
            100,
            '')
        utils.is_equal_dataframe(expected_df, df, self)

    # Tests model values, associated with FitEvent
    def test_model_fit_event(self):
        transformer = self.fitEvent.model
        utils.validate_transformer_struct(transformer, self)
        expected_transformer = modeldb_types.Transformer(
            -1,
            [0.0],
            'LabelEncoder',
            'label encoder')
        utils.is_equal_transformer(transformer, expected_transformer, self)

if __name__ == '__main__':
    unittest.main()
