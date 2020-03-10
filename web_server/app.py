import os

from flask import Flask, request, render_template, abort
import nltk

from web_server.functions import search_docs_ids, find_docs
from config import GLUSTERFS_MASTER_IP_ADDRESS, REDIS_MASTER_IP_ADDRESS

local_dir = os.path.abspath(__file__)
app = Flask(__name__)


@app.route('/', methods=['GET'])
def handle_query():
    query_sentence: str = request.args.get('query')
    doc_ids = search_docs_ids(query_sentence)
    docs = find_docs(doc_ids)
    return render_template('results_page.html', context={'docs': docs})


@app.route('/documents/<doc_id>', methods=['GET'])
def handle_document_link(doc_id):
    docs = find_docs([int(doc_id)])
    if not len(docs):
        abort(404)
    return render_template('document_page.html', context={'doc': docs[0]})


def process(namespace):
    global GLUSTERFS_MASTER_IP_ADDRESS, REDIS_MASTER_IP_ADDRESS
    print(namespace)
    GLUSTERFS_MASTER_IP_ADDRESS = namespace.gluster_ip
    REDIS_MASTER_IP_ADDRESS = namespace.redis_ip
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('stopwords')
    app.run(host='0.0.0.0', debug=True, port=80)
