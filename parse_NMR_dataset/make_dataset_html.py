#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def make_html_page(html_table, dataset_path):

    base_html = '''
    <!doctype html>
    <html lang="en">
      <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

        <title>
          TITLE
        </title>
      </head>

      <body>
        BODY
      </body>
    </html>
    '''

    title = dataset_path.parts[-1]
    base_html = base_html.replace('TITLE', title)

    body = html_table
    html_page = base_html.replace('BODY', body)

    return html_page
