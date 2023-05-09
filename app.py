import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask, request
from flask_socketio import SocketIO, send
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

# Flask is a web application framework written in Python
s = socket.socket()
flask_app = Flask(__name__)
socketio=SocketIO(flask_app,cors_allowed_origins="*")
load_dotenv()  # load variables from .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
s.connect(('localhost', 8000))

# Create a Console instance for custom Styling
console = Console()
s.listen(1)
@socketio.on('message')
def slack_events():
    """
        call
    """
    return (request)
@flask_app.route("/pdf", methods=["POST"])
def a():
    current_querry=work_load()
    return ("a")
# Run the Flask app
if __name__ == "__main__":
    flask_app.run()

