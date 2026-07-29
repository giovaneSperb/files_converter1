import os

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

load_dotenv(os.path.join(BASE_DIR,".env"))

class Config:

    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"


    UPLOAD_FOLDER = os.path.join(BASE_DIR, os.getenv("UPLOAD_FOLDER", "uploads"))
    OUTPUT_FOLDER = os.path.join( BASE_DIR, os.getenv( "OUTPUT_FOLDER", "outputs" ) )
    PDF_ORDER = os.getenv( "PDF_ORDER", "desc" ).lower()

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024