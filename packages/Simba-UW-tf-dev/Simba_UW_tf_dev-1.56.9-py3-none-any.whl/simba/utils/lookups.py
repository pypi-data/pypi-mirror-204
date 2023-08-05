import os, glob
import pandas as pd
import re
from simba.enums import Paths, Methods
from simba.read_config_unit_tests import check_file_exist_and_readable, check_if_dir_exists
from simba.feature_extractors.feature_extractor_16bp import ExtractFeaturesFrom16bps
from simba.feature_extractors.feature_extractor_14bp import ExtractFeaturesFrom14bps
from simba.feature_extractors.extract_features_9bp import extract_features_wotarget_9
from simba.feature_extractors.feature_extractor_8bp import ExtractFeaturesFrom8bps
from simba.feature_extractors.feature_extractor_8bps_2_animals import ExtractFeaturesFrom8bps2Animals
from simba.feature_extractors.feature_extractor_7bp import ExtractFeaturesFrom7bps
from simba.feature_extractors.feature_extractor_4bp import ExtractFeaturesFrom4bps
from simba.feature_extractors.feature_extractor_user_defined import UserDefinedFeatureExtractor
from simba.misc_tools import get_fn_ext
import struct
import simba


def get_body_part_configurations() -> dict:

    """Helper to return dict with named body-part schematics of pose-estimation schemas in SimBA installation as keys,
    and paths to the images representing those body-part schematics as values.
    """

    lookup = {}
    simba_dir = os.path.dirname(simba.__file__)
    img_dir = os.path.join(simba_dir, Paths.SCHEMATICS.value)
    names_path = os.path.join(simba_dir, Paths.PROJECT_POSE_CONFIG_NAMES.value)
    check_file_exist_and_readable(file_path=names_path)
    check_if_dir_exists(in_dir=img_dir)
    names_lst = list(pd.read_csv(names_path, header=None)[0])
    img_paths = glob.glob(img_dir + '/*.png')
    img_paths.sort(key=lambda v: [int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', v)])
    for name, img_path in zip(names_lst, img_paths):
        lookup[name] = {}
        lookup[name]['img_path'] = img_path
    return lookup


def get_bp_config_codes() -> dict:
    return {'1 animal; 4 body-parts': '4',
            '1 animal; 7 body-parts': '7',
            '1 animal; 8 body-parts': '8',
            '1 animal; 9 body-parts': '9',
            '2 animals; 8 body-parts': '8',
            '2 animals; 14 body-parts': '14',
            '2 animals; 16 body-parts': '16',
            'MARS': Methods.USER_DEFINED.value,
            'Multi-animals; 4 body-parts': '8',
            'Multi-animals; 7 body-parts': '14',
            'Multi-animals; 8 body-parts': '16',
            '3D tracking': '3D_user_defined'}


def get_bp_config_code_class_pairs() -> dict:
    return {'16': ExtractFeaturesFrom16bps,
            '14': ExtractFeaturesFrom14bps,
            '9': extract_features_wotarget_9,
            '8': {1: ExtractFeaturesFrom8bps, 2: ExtractFeaturesFrom8bps2Animals},
            '7': ExtractFeaturesFrom7bps,
            '4': ExtractFeaturesFrom4bps,
            'user_defined': UserDefinedFeatureExtractor}


def get_icons_paths() -> dict:
    simba_dir = os.path.dirname(simba.__file__)
    icons_dir = os.path.join(simba_dir, Paths.ICON_ASSETS.value)
    icon_paths = glob.glob(icons_dir + '/*.png')
    icons = {}
    for icon_path in icon_paths:
        _, icon_name, _ = get_fn_ext(icon_path)
        icons[icon_name] = {}
        icons[icon_name]['icon_path'] = icon_path
    return icons


def get_third_party_appender_file_formats() -> dict:
    return {'BORIS': 'csv',
            'ETHOVISION': 'xlsx',
            'OBSERVER': 'xlsx',
            'SOLOMON': 'csv',
            'DEEPETHOGRAM': 'csv',
            'BENTO': 'annot'}


def get_emojis() -> dict:
    return {'thank_you': ''.join(chr(x) for x in struct.unpack('>2H', '\U0001f64f'.encode('utf-16be'))),
            'relaxed': ''.join(chr(x) for x in struct.unpack('>2H', '\U0001F600'.encode('utf-16be'))),
            'error': ''.join(chr(x) for x in struct.unpack('>2H', '\U0001F6A8'.encode('utf-16be'))),
            'complete': ''.join(chr(x) for x in struct.unpack('>2H', '\U0001F680'.encode('utf-16be'))),
            'warning': ''.join(chr(x) for x in struct.unpack('>2H', '\u2757\uFE0F'.encode('utf-16be'))),
            'trash': ''.join(chr(x) for x in struct.unpack('>2H', '\U0001F5D1'.encode('utf-16be')))}


def get_meta_data_file_headers() -> list:
    return ["Classifier_name",
            "RF_criterion",
            "RF_max_features",
            "RF_min_sample_leaf",
            "RF_n_estimators",
            "compute_feature_permutation_importance",
            "generate_classification_report",
            "generate_example_decision_tree",
            "generate_features_importance_bar_graph",
            "generate_features_importance_log",
            "generate_precision_recall_curves",
            "generate_rf_model_meta_data_file",
            "generate_sklearn_learning_curves",
            "learning_curve_data_splits",
            "learning_curve_k_splits",
            "n_feature_importance_bars",
            "over_sample_ratio",
            "over_sample_setting",
            "train_test_size",
            "train_test_split_type",
            "under_sample_ratio",
            "under_sample_setting",
            "class_weight"]


def get_cmaps() -> list:
    return ['spring',
            'summer',
            'autumn',
            'cool',
            'Wistia',
            'Pastel1',
            'Set1',
            'winter',
            'afmhot',
            'gist_heat',
            'copper']

