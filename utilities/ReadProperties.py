import os
import configparser

config = configparser.RawConfigParser()

# -------- FIXED PATH (Works on Windows + Linux + GitHub Actions) --------
# Get project root dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))       # utilities/
project_root = os.path.dirname(current_dir)                    # OrangeHRM_TC root
config_path = os.path.join(project_root, "configuration", "config.ini")
# ------------------------------------------------------------------------

# Read the config.ini file
config.read(config_path)


class ReadConfig:
    @staticmethod
    def get_username():
        Username = config.get("credentials", "username")
        return Username

    @staticmethod
    def get_password():
        password = config.get("credentials", "password")
        return password

    @staticmethod
    def get_base_url():
        BASE_URL = config.get("credentials", "url")
        return BASE_URL

    @staticmethod
    def get_ess_username():
        ess_username = config.get("credentials", "ess_username")
        return ess_username

    @staticmethod
    def get_ess_password():
        ess_password = config.get("credentials", "ess_password")
        return ess_password

    @staticmethod
    def get_emp_name():
        emp_name = config.get("credentials", "emp_name")
        return emp_name
