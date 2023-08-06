"""
Python SDK
"""

__version__ = "0.4.3"
__author__ = "Extrinsec LLC"
__credits__ = "Extrinsec LLC"

import json
import os
import pkgutil
import platform
import tempfile
from ctypes import cdll

if "extrinsec-appdefender" in os.getenv("AWS_LAMBDA_EXEC_WRAPPER", ""):
    raise ValueError("AppDefender SDK cannot be used together with the AppDefender AWS Lambda extension")

def supported():
    architectures = ["x86_64", "arm64", "aarch64" ]
    provider_envs = ["AWS_EXECUTION_ENV",           # AWS Lambda
                    "K_SERVICE",                    # Google Cloud Functions
                    "FUNCTIONS_WORKER_RUNTIME",     # Azure
                    "CATALYST_RESOURCE_ID",         # Zoho
                    "__OW_ACTION_NAME",             # DigitalOcean/OpenWhisk
                    "ES_APP_NAME"
                    ]
    return platform.system().lower() == 'linux' and platform.machine().lower() in architectures and any(map(lambda env: os.environ.get(env), provider_envs))

if supported():
    # set env vars
    os.environ["ES_RUNTIME_LANGUAGE"] = "PYTHON"
    os.environ["ES_RUNTIME_LANGUAGE_VERSION"] = platform.python_version()
    os.environ["ES_APP_DIR"] = os.getcwd()
    os.environ["ES_SDK_VERSION"] = __version__

    arch = platform.machine()
    libc = 'musl' if os.popen('. /etc/os-release && echo $ID').read().strip() == 'alpine' else 'gnu'
    suffix = f"{arch}.{libc}"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    appdefender_path = os.path.join(dir_path, "lib", f"libcore.{suffix}.so")

    if not os.path.isfile(appdefender_path):
        appdefender_path = os.path.join(tempfile.gettempdir(), f"libcore.{suffix}.so")
        with open(appdefender_path, "wb") as appdefender_lib_file:
            appdefender_lib_file.write(pkgutil.get_data(__name__, f"lib/libcore.{suffix}.so"))

    appdefender_lib = cdll.LoadLibrary(appdefender_path)
    print("[INFO] [AppDefender] Python SDK version: " + os.environ["ES_SDK_VERSION"])

else:
    err_msg_unsupported_runtime_env = "[ERROR] [AppDefender] only Linux x64/arm64 systems on AWS Lambdas, Google Cloud Functions, or Azure Functions are supported."
    print(err_msg_unsupported_runtime_env)
    raise ValueError(err_msg_unsupported_runtime_env)
