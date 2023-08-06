# from os.path import realpath
# from pathlib import Path

# from robotnikmq.config import RobotnikConfig, server_config

# from tests.integration.utils import vagrant_test

# from legion_cli.cli import _watch

# try:
#     from pytest_cov.embed import cleanup_on_sigterm
# except ImportError:
#     pass
# else:
#     cleanup_on_sigterm()

# HERE = Path(realpath(__file__)).parent
# CA_CERT = HERE / 'vagrant' / 'pki' / 'robotnik-ca.crt'
# USERNAME = 'legion'
# PASSWORD = 'hackme'
# VIRTUAL_HOST = '/legion'
# CERT = HERE / 'vagrant' / 'pki' / 'issued' / 'rabbitmq-vm' / 'rabbitmq-vm.crt'
# KEY = HERE / 'vagrant' / 'pki' / 'issued' / 'rabbitmq-vm' / 'rabbitmq-vm.key'
# PORT = 5671
# LOCALHOST = '127.0.0.1'
# META_QUEUE = 'skynet.legion'
# CONFIG = RobotnikConfig(tiers=[[server_config(LOCALHOST, PORT, USERNAME, PASSWORD,
#                                 VIRTUAL_HOST, CA_CERT, CERT, KEY)]])


# # @vagrant_test
# # def test_basic_watch():
# #     print()
# #     _watch(['skynet.rabbitmq-vm.network'], msg_limit=2, config=CONFIG)


# # @vagrant_test
# # def test_big_message_watch():
# #     print()
# #     _watch(['skynet.rabbitmq-vm.system'], msg_limit=2, config=CONFIG)

# import pika
from testcontainers.rabbitmq import RabbitMqContainer


def test_basic_watch():
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        print(rabbitmq.get_connection_params())
        # connection = pika.BlockingConnection(rabbitmq.get_connection_params())
        # # channel = connection.channel()
