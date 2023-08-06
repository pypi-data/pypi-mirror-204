# Flask settings
import argparse
import configparser
import logging
import os

DEFAULT_FLASK_SERVER_NAME = '0.0.0.0'
DEFAULT_FLASK_SERVER_PORT = '5001'
DEFAULT_FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# tensorflow serving client settings
DEFAULT_TF_SERVER_NAME = '127.0.0.1'
DEFAULT_TF_SERVER_PORT = 8500

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description='Taichu Model Server')
    parser.add_argument('action', action="store", choices=['init', 'run', 'build'])

    parser.add_argument('--from_image', action="store",
                        default='swr.cn-central-221.ovaijisuan.com/wair/taichu-serve:latest', type=str)
    parser.add_argument('--name', action="store", default='taichu-serve-env', type=str)

    parser.add_argument('--grpc_port', action="store", default=8080, type=int)
    parser.add_argument('--http_port', action="store", default=8081, type=int)
    parser.add_argument('--grpc_only', action="store", default=False, type=bool)
    parser.add_argument('--model_path', action="store", default='./', type=str)
    parser.add_argument('--service_file', action="store", default='customize_service.py', type=str)
    parser.add_argument('--max_concurrent_requests', action="store", default=1, type=int)
    parser.add_argument('--instances_num', action="store", default=1, type=int)

    args = parser.parse_args()

    # 读取配置文件
    if not os.path.exists('config.ini'):
        logger.info('config.ini not found, use default config')
        return args

    config = configparser.ConfigParser()
    config.read('config.ini')
    args.grpc_port = config.getint('server', 'grpc_port', fallback=args.grpc_port)
    args.http_port = config.getint('server', 'http_port', fallback=args.http_port)
    args.grpc_only = config.getboolean('server', 'grpc_only', fallback=args.grpc_only)
    args.instances_num = config.getint('server', 'instances_num', fallback=args.instances_num)

    args.max_concurrent_requests = config.getint('rate-limiter', 'max_concurrent_requests', fallback=1)

    return args
