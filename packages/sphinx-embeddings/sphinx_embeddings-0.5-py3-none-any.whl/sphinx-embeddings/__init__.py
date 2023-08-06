from docutils import nodes
from hashlib import md5
from json import dump, load
import tiktoken
from os import environ
from copy import deepcopy

def estimate_token_count(text):
    return len(encoding.encode(text))

def generate_embeddings(app, doctree, docname):
    data = read_data()
    encoding = tiktoken.get_encoding('cl100k_base')
    clone = deepcopy(doctree)
    # Remove code blocks
    for node in clone.traverse(nodes.literal_block):
        if 'code' in node['classes']:
            node.parent.remove(node)
    for section in clone.traverse(nodes.section):
        text = section.astext()
        text = text.replace('\n', ' ')
        # Generate hash based off the docs content
        checksum = md5(text.encode('utf-8')).hexdigest()
        if checksum in data:
            continue
        data[checksum] = {
            'docname': docname,
            'text': text,
            'tokens': estimate_token_count(text)
        }
    write_data(data)

def write_data(data):
    data_file = '/tmp/embeddings.json'
    with open(data_file, 'w') as f:
        dump(data, f)

def read_data():
    data_file = '/tmp/embeddings.json'
    data = {}
    if not path.exists(data_file):
        with open(data_file, 'w') as f:
            dump(data, f)
    else:
        with open(data_file, 'r') as f:
            data = load(f)
    return data

def setup(app):
    app.connect('doctree-resolved', generate_embeddings)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
