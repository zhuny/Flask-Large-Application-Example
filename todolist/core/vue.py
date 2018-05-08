import subprocess

import xml.etree.ElementTree as ET

import requests
from jinja2 import Markup
from flask import Flask, url_for


class Node:
    def __init__(self, root=None):
        self.root: ET.Element = root

    def __getattr__(self, item):
        children = ET.Element(item)
        if self.root is not None:
            self.root.append(children)
        return Node(children)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def attrs(self, **kwargs):
        if 'text' in kwargs:
            self.root.text = kwargs.pop('text')
        self.root.attrib.update(kwargs)

    def get_string(self):
        return ET.tostring(self.root).decode()

    @classmethod
    def get_node(cls, name):
        return cls(ET.Element(name))


class VueApp:
    def __init__(self, app=None):
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):

        def get_js_path(name):
            if app.config['DEBUG']:
                return (
                    "//localhost:%s/dist/%s.bundle.js"
                ) % (
                    app.config['VUE_PORT'],
                    name
                )
            else:
                return (
                    url_for(
                        'static',
                        filename="vue/%s.bundle.js"%name
                    )
                )

        def vue_convert(name):
            with Node.get_node('div') as root:
                with root.div as f1:
                    f1.attrs(id="vue-elem-"+name)
                with root.script as f2:
                    f2.attrs(
                        type = "text/javascript",
                        src = get_js_path(name),
                        text = " "
                    )
            return Markup(root.get_string())

        @app.context_processor
        def get_processor():
            return dict(vue=vue_convert)

        def is_server_running():
            url = "http://localhost:%s/"%app.config['VUE_PORT']
            try:
                requests.get(url, timeout=0.5)
                running = True
            except requests.exceptions.ConnectTimeout:
                running = False
            return running

        @app.before_first_request
        def start_vue():
            if app.config['DEBUG']:
                if not is_server_running():
                    subprocess.Popen(
                        (
                            "npm run dev -- --port %s" %
                            app.config['VUE_PORT']
                        ),
                        shell = True
                    )

        app.config.setdefault('VUE_PORT', "8957")


