#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
parse_NMR_dataset - parse experimental information from a Bruker NMR dataset
author: Norm1 <norm@normandcyr.com>
'''

import re
import os
import json
import argparse
import nmrglue as ng
from pathlib import Path
from datetime import date
from operator import itemgetter
from collections import OrderedDict
from json2html import json2html as j2h
from parse_NMR_dataset import _version
from parse_NMR_dataset import make_dataset_html


def load_experiment_data(experiment_number):

    dic, data = ng.bruker.read(str(experiment_number))

    return dic, data


def determine_nb_dimensions(dic):

    acqu_list = []
    for key in dic:
        if re.match('acqu.+', key):
            acqu_list.append(key)

    nb_dimensions = len(acqu_list)

    return(acqu_list, nb_dimensions)


def parse_dimension_parameters(all_dimension_parameters):

    nucleus = all_dimension_parameters['NUC1']
    spectral_width = round(all_dimension_parameters['SW'], 2)
    nb_increments = all_dimension_parameters['TD']
    offset = round(all_dimension_parameters['O1']/all_dimension_parameters['SFO1'], 2)

    dimension_acquision_parameters = OrderedDict()
    dimension_acquision_parameters['nucleus'] = nucleus
    dimension_acquision_parameters['spectral width'] = spectral_width
    dimension_acquision_parameters['carrier offset'] = offset
    dimension_acquision_parameters['number of increments'] = nb_increments

    return(dimension_acquision_parameters)


def parse_general_acquision_parameters(all_dimension_parameters, nb_dimensions):

    nb_scans = all_dimension_parameters['NS']
    temperature = round(all_dimension_parameters['TE'] - 273.15, 1)
    acquisition_date = str(date.fromtimestamp(all_dimension_parameters['DATE']))
    pulse_program = all_dimension_parameters['PULPROG']

    general_acquision_parameters = OrderedDict()
    general_acquision_parameters['acquisition date'] = acquisition_date
    general_acquision_parameters['pulse program'] = pulse_program
    general_acquision_parameters['number of dimensions'] = nb_dimensions
    general_acquision_parameters['number of scans'] = nb_scans
    general_acquision_parameters['temperature'] = temperature

    return general_acquision_parameters


def build_experiment_information(dataset_info, experiment_number):

    dic, data = load_experiment_data(experiment_number)
    acqu_list, nb_dimensions = determine_nb_dimensions(dic)

    acquision_parameters = OrderedDict()

    for dimension in acqu_list:
        all_dimension_parameters = dic[dimension]

        if dimension == 'acqus':
            acquision_parameters['general parameters'] = parse_general_acquision_parameters(all_dimension_parameters, nb_dimensions)
            acquision_parameters['direct dimension parameters'] = parse_dimension_parameters(all_dimension_parameters)

        else:
            acquision_parameters['indirect dimension parameters'] = parse_dimension_parameters(all_dimension_parameters)

    dataset_info['experiments'].append({'experiment number': int(experiment_number.parts[-1]), 'acquision parameters': acquision_parameters})

    return dataset_info


def create_json_format(dataset_info):

    sorted_experiments_list = sorted(dataset_info['experiments'], key=itemgetter('experiment number'), reverse=False)
    dataset_experiments_sorted = {'dataset name': dataset_info['dataset name'], 'experiments': sorted_experiments_list}
    dataset_info_json = json.dumps(dataset_experiments_sorted, indent=4)

    return dataset_info_json


def build_html_table(general_info_json):

    build_direction = 'TOP_TO_BOTTOM'
    table_attributes = 'id=\"info-table\" class=\"table table-bordered table-striped table-hover table-sm\"'
    html_table = j2h.convert(json=general_info_json, table_attributes=table_attributes)

    return html_table


def save_json_file(dataset_info_json, dataset_path):

    filename = dataset_path.parts[-1] + '.json'
    with open(filename, 'w') as output_file:
        output_file.write(dataset_info_json)


def main():

    parser = argparse.ArgumentParser(prog='parse NMR dataset', usage='parse_dataset [options]')
    parser.add_argument('dataset_path',
                        help='indicate the path to dataset you want to be parsed',
                        type=Path,
                        #default=Path(__file__).absolute().panamerent / "data",
                        #nargs='?',
                        )
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s ' + _version.__version__,
                        )
    args = parser.parse_args()
    dataset_path = args.dataset_path

    dataset_info = {'dataset name': str(dataset_path.parts[-1]), 'experiments': []}

    for experiment_number in dataset_path.iterdir():
        if experiment_number.is_dir():
            dataset_info = build_experiment_information(dataset_info, experiment_number)

    dataset_info_json = create_json_format(dataset_info)
    save_json_file(dataset_info_json, dataset_path)

    html_table = build_html_table(dataset_info_json)
    make_dataset_html.build_html(dataset_path, html_table)


if __name__ == '__main__':
    main()
