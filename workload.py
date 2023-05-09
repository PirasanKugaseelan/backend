from waitress import serve
import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask, request
from flask_socketio import SocketIO, send
from flask_socketio import SocketIO, emit
from main_proto import Chat_With_PDFs_and_Summarize
import hashlib
import glob
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
# from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from modify import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

# local server object sender im using.
""" It is important to encode using b before sending it and .decode will save it properly  """
import socket
from rich import print
from rich.console import Console
from rich.table import Table

load_dotenv()  # load variables from .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the chatbot
chatbot = Chat_With_PDFs_and_Summarize()

@flask_app.route("/pdf", methods=["POST"])
def handle_pdf():
    """
    Handle incoming PDF data.
    """
    pdf_file = request.files['pdf_file']  # get the PDF file from the request
    page_range = request.form.get('page_range')  # get the page range from the request
    if page_range:
        page_range = list(map(int, page_range.split(',')))  # convert string to list of integers
    os.makedirs('Docs', exist_ok=True)  # create Docs subdirectory if it doesn't exist
    pdf_path = os.path.join('Docs', '{}.pdf'.format(hashlib.sha256(pdf_file.read()).hexdigest()))  # create path for the PDF file
    pdf_file.seek(0)  # reset file pointer to the beginning
    pdf_file.save(pdf_path)  # save the PDF file
    chatbot.load_document(pdf_path, page_range)  # load the document
    return 'PDF loaded.', 200

@socketio.on('message')
def handle_message(data):
    """
    Handle incoming SocketIO messages.
    """
    query = data['query']
    answer = chatbot.ask_question(query)  # ask the chatbot a question
    emit('message', {'answer': answer})

@flask_app.route("/summary", methods=["GET"])
def handle_summary():
    """
    Generate a summary of the loaded document.
    """
    summary = chatbot.summarize()  # generate a summary
    return {'summary': summary}, 200

# Run the Flask app
if __name__ == "__main__":
    from waitress import serve
    from eventlet import monkey_patch
    monkey_patch()

    import eventlet
    import eventlet.wsgi

    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), flask_app)
