import os
import configparser
from dotenv import load_dotenv

# Load .env
load_dotenv()

# ---------- Dynamic path ----------
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
config_path = os.path.join(project_root, "configuration", "config.ini")
# ----------------------------------

config = configparser.RawConfigParser()
config.read(config_path)

class ReadConfig:

    # ---------- Non-secret config ----------
    URL = config.get("credentials", "url", fallback=None)

    # ---------- Secrets from .env / GitHub ----------
    USERNAME = os.getenv("ADMIN_USERNAME")
    PASSWORD = os.getenv("ADMIN_PASSWORD")
    ESS_USERNAME = os.getenv("ESS_USERNAME")
    ESS_PASSWORD = os.getenv("ESS_PASSWORD")

    # @staticmethod
    # def validate():
    #     missing = []
    #     for key, value in {
    #         "URL": ReadConfig.URL,
    #         "USERNAME": ReadConfig.USERNAME,
    #         "PASSWORD": ReadConfig.PASSWORD,
    #     }.items():
    #         if not value:
    #             missing.append(key)
    #
    #     if missing:
    #         raise EnvironmentError(
    #             f"Missing environment variables: {', '.join(missing)}"
    #         )




    # @staticmethod
    # def get_username():
    #     Username = config.get("credentials", "username")
    #     return Username
    #
    # @staticmethod
    # def get_password():
    #     password = config.get("credentials", "password")
    #     return password
    #
    # @staticmethod
    # def get_base_url():
    #     BASE_URL = config.get("credentials", "url")
    #     return BASE_URL
    #
    # @staticmethod
    # def get_ess_username():
    #     ess_username = config.get("credentials", "ess_username")
    #     return ess_username
    #
    # @staticmethod
    # def get_ess_password():
    #     ess_password = config.get("credentials", "ess_password")
    #     return ess_password
    #
    # @staticmethod
    # def get_emp_name():
    #     emp_name = config.get("credentials", "emp_name")
    #     return emp_name
