#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader


def build_html(dataset_path, html_table):

    file_loader = FileSystemLoader('parse_NMR_dataset/templates')
    env = Environment(loader=file_loader)
    template = env.get_template('data.html')

    dataset_name = dataset_path.parts[-1]
    filename = dataset_name + '.html'
    with open(filename, 'w') as f:
        f.write(template.render(dataset_name=dataset_name, html_table=html_table))
