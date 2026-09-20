import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GUARANTOR_ID = int(os.getenv("GUARANTOR_ID"))
BOT_USERNAME = os.getenv("BOT_USERNAME")

START_GIF = "CgACAgIAAxkBAAMDaq1XSvbOcKSe065WrMwmRin2Ml8AAmCnAALXnxBJeAER3jg671E9BA"