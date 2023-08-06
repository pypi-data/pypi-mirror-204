import shutil
import os

from cgc.commands.auth import auth_utils
from cgc.utils.consts.env_consts import TMP_DIR
from cgc.utils.config_utils import get_config_path, save_to_config, user_config_file
from cgc.utils.message_utils import key_error_decorator_for_helpers


@key_error_decorator_for_helpers
def auth_register_response(response, user_id, priv_key_bytes) -> str:
    TMP_DIR_PATH = os.path.join(get_config_path(), TMP_DIR)
    unzip_dir = auth_utils.save_and_unzip_file(response)
    aes_key, password = auth_utils.get_aes_key_and_password(unzip_dir, priv_key_bytes)

    save_to_config(user_id=user_id, password=password, aes_key=aes_key)
    auth_utils.auth_create_api_key_with_save()
    shutil.rmtree(TMP_DIR_PATH)
    return f"Register successful! You can now use the CLI. Saved data to: {user_config_file}\n\
        Consider backup this file. It stores data with which you can access CGC platform."


@key_error_decorator_for_helpers
def login_successful_response():
    return f"Successfully logged in, created new API key pair.\n\
                Saved data to: {user_config_file}.\n\
                Consider backup this file. It stores data with which you can access CGC platform."
