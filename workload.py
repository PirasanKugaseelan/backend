import os
import hashlib
import glob
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
# from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from modify import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from main_proto import Chat_With_PDFs_and_Summarize
from rich import print
from rich.console import Console
from rich.table import Table
import main_proto
import socket


load_dotenv()  # load variables from .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
s = socket.socket()
s.listen(1)
# Create a Console instance for custom Styling
console = Console()
def work_load():
    chat = Chat_With_PDFs_and_Summarize()

    # Search the 'documents' folder for PDF files
    document_list = glob.glob("documents/*.pdf")

    # Prepare a Rich Table for diplaying available PDF documents
    docs_table = Table(title="Available documents", show_header=True,
                       header_style="bold magenta")
    docs_table.add_column("Index", justify="right", style="dim")
    docs_table.add_column("Document", justify="right", style="bright_yellow")

    for index, document in enumerate(document_list):
        docs_table.add_row(str(index), document)

    console.print(docs_table)

    # Get user input for selecting the document to load
    s.send(b'Enter the index of the document you want to load: ')
    document_index = int(console.input("Enter the index of the document you want to load: "))
    selected_document = document_list[document_index]

    # Get user input the range of pages to index
    page_range_option = console.input("Select pages to index: (A)ll pages or (C)ustom range: ").strip()

    if page_range_option.lower == "c":
        start_page = int(console.input("Start page (0-indexed): "))
        end_page = int(console.input("End page: "))
        page_range = (start_page, end_page)

    elif page_range_option.lower() == "a":
        page_range = None

    # Load the selected document with the specified page range
    chat.load_document(selected_document, page_range=page_range)

    console.rule("Document loaded")

    # Get user input for generating a summary
    summary_option = console.input("Do you want to generate a summary? (Y)es or (N)o: ").strip()

    if summary_option.lower() == "y":
        summary = chat.summarize()
        console.print(f"\nSummary: {summary}", style="bold")
        console.print('\n')

    # Ask questions and get answers in a Loop
    while True:
        query = console.input("Question: ")
        answer = chat.ask_question(query)
        console.print(f"Answer: {answer}", style="green")
a=work_load()