import os
import shutil
import unittest
from pprint import pprint
import numpy as np
import pandas as pd
import seaborn as sns
from aistac.properties.property_manager import PropertyManager
from ds_discovery import Transition, FeatureCatalog
from ds_discovery.components.discovery import DataDiscovery as Discover, DataDiscovery
from ds_discovery import SyntheticBuilder

# Pandas setup
pd.set_option('max_colwidth', 320)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)
pd.set_option('expand_frame_repr', True)



class DiscoveryTest(unittest.TestCase):
    """Test: """

    def setUp(self):
        # set environment variables
        os.environ['HADRON_PM_PATH'] = os.path.join("${PWD}", 'work', 'config')
        os.environ['HADRON_DEFAULT_SOURCE_PATH'] = os.path.join("${HOME}", 'code', 'projects',  'data', 'sample')
        PropertyManager._remove_all()
        try:
            shutil.rmtree('work')
        except:
            pass
        try:
            shutil.copytree('../data', os.path.join(os.environ['PWD'], 'work'))
        except:
            pass

    def tearDown(self):
        try:
            shutil.rmtree('work')
        except:
            pass

    def test_sharpo_wilks(self):
        norm = pd.Series(np.random.normal(size=10000))
        expo = pd.Series(np.random.exponential(size=10000))
        logistic = pd.Series(np.random.logistic(size=10000))

        norm.sort_values(inplace=True)
        # result = DataDiscovery.shapiro_wilk_normality(norm)
        # print(result)
        # result = DataDiscovery.dagostinos_k2_normality(norm)
        # print(result)
        result = DataDiscovery.anderson_darling_tests(norm, dist='norm')
        print(result)
        result = DataDiscovery.anderson_darling_tests(expo, dist='expon')
        print(result)
        result = DataDiscovery.anderson_darling_tests(logistic, dist='logistic')
        print(result)

    def test_interquartile_outliers(self):
        expo = pd.Series(np.random.exponential(size=10000))
        result = DataDiscovery.interquartile_outliers(expo)
        print(result)

    def test_bootstrap_confidence_interval(self):
        rng = np.random.default_rng(13)
        normal = pd.Series(rng.normal(size=10000))
        expo = pd.Series(rng.exponential(size=10000))
        p, q = DataDiscovery.bootstrap_confidence_interval(normal)
        self.assertAlmostEqual(-0.01, p, 2)
        self.assertAlmostEqual(0.03, q, 2)
        p, q = DataDiscovery.bootstrap_confidence_interval(expo)
        self.assertAlmostEqual(0.97, p, 2)
        self.assertAlmostEqual(1.01, q, 2)

    def test_hellinger_distance(self):
        p = [0.36, 0.48, 0.16]
        q = [0.30, 0.50, 0.20]
        result = Discover.distance_hellinger(p, q, precision=4)
        self.assertEqual(0.0508, result)
        p = np.array([0.36, 0.48, 0.16], dtype=np.float32)
        q = np.array([0.30, 0.50, 0.20], dtype=np.float32)
        result = Discover.distance_hellinger(p, q, precision=4)
        self.assertEqual(0.0508, result)
        p = pd.Series([0.36, 0.48, 0.16])
        q = pd.Series([0.30, 0.50, 0.20])
        result = Discover.distance_hellinger(p, q, precision=4)
        self.assertEqual(0.0508, result)

    def test_jensen_shannon_distance(self):
        p = [0.36, 0.48, 0.16]
        q = [0.30, 0.50, 0.20]
        result = Discover.distance_jensen_shannon(p, q, precision=4)
        self.assertEqual(0.0508, result)
        p = np.array([0.36, 0.48, 0.16], dtype=np.float32)
        q = np.array([0.30, 0.50, 0.20], dtype=np.float32)
        result = Discover.distance_jensen_shannon(p, q, precision=4)
        self.assertEqual(0.0508, result)
        p = pd.Series([0.36, 0.48, 0.16])
        q = pd.Series([0.30, 0.50, 0.20])
        result = Discover.distance_jensen_shannon(p, q, precision=4)
        self.assertEqual(0.0508, result)

    def test_filter_univariate_roc_auc(self):
        tr = Transition.from_env('test', default_save=False, default_save_intent=False, has_contract=False)
        tr.set_source('paribas.csv', nrows=5000)
        data = tr.load_source_canonical()
        result = Discover.filter_univariate_roc_auc(data, target='target', threshold=0.55)
        self.assertCountEqual(['v10', 'v129', 'v14', 'v62', 'v50'], result)
        # Custom classifier
        classifier_kwargs = {'iterations': 2, 'learning_rate': 1, 'depth': 2}
        result = Discover.filter_univariate_roc_auc(data, target='target', threshold=0.55, package='catboost',
                                                    model='CatBoostClassifier', classifier_kwargs=classifier_kwargs,
                                                    fit_kwargs={'verbose': False})
        self.assertCountEqual(['v50', 'v10', 'v14', 'v12', 'v129', 'v62', 'v21', 'v34'], result)

    def test_filter_univariate_mse(self):
        tr = Transition.from_env('test', default_save=False, default_save_intent=False, has_contract=False)
        tr.set_source('ames_housing.csv', nrows=5000)
        data = tr.load_source_canonical()
        result = Discover.filter_univariate_mse(data, target='SalePrice', as_series=False, top=5)
        self.assertEqual(['OverallQual', 'GarageCars', 'FullBath', 'TotRmsAbvGrd', 'YearBuilt'], result)


    def test_filter_correlated(self):
        tools = SyntheticBuilder.scratch_pad()
        df = pd.DataFrame()
        df['col1'] = [1,2,3,4,5,6,7]
        df['col2'] = [1,2,3,4,5,6,7]
        df['col3'] = [2,2,3,2,2,2,3]
        df['col4'] = [2,2,3,2,2,2,3]
        df['col5'] = [2,2,3,2,2,2,3]
        df['col4'] = [7,2,4,2,1,6,4]
        df['target'] = [1,0,1,1,0,0,1]
        result = DataDiscovery.filter_correlated(df, target='target')
        print(result)

    def test_canonical_report(self):
        sb = SyntheticBuilder.from_memory()
        size = 1000
        df = pd.DataFrame()
        df['cat'] = sb.tools.get_category(list('ABCDE'), size=size)
        df['num'] = sb.tools.get_number(100.0, size=size)
        df['int'] = sb.tools.get_number(100, size=size)
        df['bool'] = sb.tools.get_category([1, 0], size=size)
        df['date'] = sb.tools.get_datetime(start='2022-12-01', until='2023-03-31', date_format='%Y-%m-%d', size=size)
        df['object'] = sb.tools.get_string_pattern('ccd', size=size)
        self.assertNotIn('%_Nxt', sb.canonical_report(df, stylise=False).columns)
        self.assertIn('%_Nxt', sb.canonical_report(df, stylise=False, inc_next_dom=True).columns)
        result = sb.canonical_report(df, stylise=False, report_header='Attributes', condition="=='num'")
        self.assertTrue(result.columns[0] == 'Attributes (6)')
        self.assertEqual((1,7), result.shape)
        result = sb.canonical_report(df, stylise=False, report_header='Observations', condition=".str.contains('mean')")
        self.assertEqual((3, 7), result.shape)
        self.assertEqual(['bool', 'int', 'num'], result['Attributes (6)'].values.tolist())

    def test_data_dictionary(self):
        sb = SyntheticBuilder.from_memory()
        size = 1000
        df = sb.tools.get_sample('type_data', size=size)
        print(df.shape)



if __name__ == '__main__':
    unittest.main()
