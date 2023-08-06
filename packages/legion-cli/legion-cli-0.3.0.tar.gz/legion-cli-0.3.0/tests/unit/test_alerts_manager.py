from time import sleep
from typing import List

from legion_utils import AlertMsg
from pytest_mock import MockerFixture
from robotnikmq import Message

from legion_cli.alerts_manager import AlertsManager


def mock_init(_, config):
    assert config is None


def mock_bind(self, exchange, binding):
    assert exchange == 'skynet'
    assert binding in {'#.warning', '#.error', '#.critical'}
    return self


def test_fire_one_alert_no_lambdas(mocker: MockerFixture):
    def mock_consume(_, inactivity_timeout):
        assert inactivity_timeout == 1
        for i in [Message({'priority': 3, 'description': 'test', 'alert_key': '[something]', 'ttl': 1},
                          routing_key='test'),
                  None,
                  Message({'priority': 3, 'description': 'test', 'alert_key': '[something]', 'ttl': 1},
                          routing_key='test'),
                  None, None, None,
                  Message({'priority': 3, 'description': 'test', 'alert_key': '[something]', 'ttl': 1},
                          routing_key='test')]:
            sleep(0.5)
            yield i

    mocker.patch('legion_cli.alerts_manager.Subscriber.__init__', mock_init)
    mocker.patch('legion_cli.alerts_manager.Subscriber.bind', mock_bind)
    mocker.patch('legion_cli.alerts_manager.Subscriber.consume', mock_consume)

    manager = AlertsManager(['skynet'],
                            num_alerts=3)
    manager.start()
    assert True


def test_fire_exceptions(mocker: MockerFixture):
    def mock_consume(_, inactivity_timeout):
        assert inactivity_timeout == 1
        for i in [Message({'priority': 3, 'description': 'test', 'alert_key': '[something]', 'ttl': 1},
                          routing_key='test'),
                  None,
                  Message({'priority': 3, 'description': 'test', 'alert_key': '[something]', 'ttl': 1},
                          routing_key='test'),
                  None, None, None,
                  Message({'priority': 3, 'description': 'test', 'alert_key': '[something]', 'ttl': 1},
                          routing_key='test')]:
            sleep(0.5)
            yield i

    mocker.patch('legion_cli.alerts_manager.Subscriber.__init__', mock_init)
    mocker.patch('legion_cli.alerts_manager.Subscriber.bind', mock_bind)
    mocker.patch('legion_cli.alerts_manager.Subscriber.consume', mock_consume)

    def bad(a: AlertMsg) -> None:
        raise ValueError(a.description)

    manager = AlertsManager(['skynet'],
                            num_alerts=3,
                            on_new=bad,
                            on_update=bad,
                            on_expire=bad)
    manager.start()
    assert True


def test_fire_one_alert(mocker: MockerFixture):
    def mock_consume(_, inactivity_timeout):
        assert inactivity_timeout == 1
        for i in [Message({'priority': 3, 'description': 'test', 'alert_key': '[something]', 'ttl': 5},
                          routing_key='test')]:
            yield i

    mocker.patch('legion_cli.alerts_manager.Subscriber.__init__', mock_init)
    mocker.patch('legion_cli.alerts_manager.Subscriber.bind', mock_bind)
    mocker.patch('legion_cli.alerts_manager.Subscriber.consume', mock_consume)

    new_alerts: List[AlertMsg] = []
    updated_alerts: List[AlertMsg] = []
    expired_alerts: List[AlertMsg] = []

    manager = AlertsManager(['skynet'],
                            num_alerts=1,
                            on_new=new_alerts.append,
                            on_update=updated_alerts.append,
                            on_expire=expired_alerts.append)
    manager.start()
    assert len(new_alerts) == 1
    assert len(updated_alerts) == 0
    assert len(expired_alerts) == 0
    assert new_alerts[0].description == 'test'


def test_fire_non_alert(mocker: MockerFixture):
    def mock_consume(_, inactivity_timeout):
        assert inactivity_timeout == 1
        for i in [Message({'priority': 0, 'description': 'test', 'alert_key': '[something]', 'ttl': 5},
                          routing_key='test')]:
            yield i

    mocker.patch('legion_cli.alerts_manager.Subscriber.__init__', mock_init)
    mocker.patch('legion_cli.alerts_manager.Subscriber.bind', mock_bind)
    mocker.patch('legion_cli.alerts_manager.Subscriber.consume', mock_consume)

    new_alerts: List[AlertMsg] = []
    updated_alerts: List[AlertMsg] = []
    expired_alerts: List[AlertMsg] = []

    manager = AlertsManager(['skynet'],
                            num_alerts=0,
                            on_new=new_alerts.append,
                            on_update=updated_alerts.append,
                            on_expire=expired_alerts.append)
    manager.start()
    assert len(new_alerts) == 0
    assert len(updated_alerts) == 0
    assert len(expired_alerts) == 0


def test_fire_one_alert_and_non_alerts(mocker: MockerFixture):
    def mock_consume(_, inactivity_timeout):
        assert inactivity_timeout == 1
        for i in [None, None, None,
                  Message({'priority': 3, 'description': 'test', 'alert_key': '[something]', 'ttl': 5},
                          routing_key='test')]:
            yield i

    mocker.patch('legion_cli.alerts_manager.Subscriber.__init__', mock_init)
    mocker.patch('legion_cli.alerts_manager.Subscriber.bind', mock_bind)
    mocker.patch('legion_cli.alerts_manager.Subscriber.consume', mock_consume)

    new_alerts: List[AlertMsg] = []
    updated_alerts: List[AlertMsg] = []
    expired_alerts: List[AlertMsg] = []

    manager = AlertsManager(['skynet'],
                            num_alerts=1,
                            on_new=new_alerts.append,
                            on_update=updated_alerts.append,
                            on_expire=expired_alerts.append)
    manager.start()
    assert len(new_alerts) == 1
    assert len(updated_alerts) == 0
    assert len(expired_alerts) == 0
    assert new_alerts[0].description == 'test'


def test_update_one_alert(mocker: MockerFixture):
    def mock_consume(_, inactivity_timeout):
        assert inactivity_timeout == 1
        for i in [Message({'priority': 3, 'description': 'test', 'alert_key': '[something]', 'ttl': 5},
                          routing_key='test'),
                  Message({'priority': 3, 'description': 'test 2', 'alert_key': '[something]', 'ttl': 5},
                          routing_key='test')]:
            yield i

    mocker.patch('legion_cli.alerts_manager.Subscriber.__init__', mock_init)
    mocker.patch('legion_cli.alerts_manager.Subscriber.bind', mock_bind)
    mocker.patch('legion_cli.alerts_manager.Subscriber.consume', mock_consume)

    new_alerts: List[AlertMsg] = []
    updated_alerts: List[AlertMsg] = []
    expired_alerts: List[AlertMsg] = []

    manager = AlertsManager(['skynet'],
                            num_alerts=2,
                            on_new=new_alerts.append,
                            on_update=updated_alerts.append,
                            on_expire=expired_alerts.append)
    manager.start()
    assert len(new_alerts) == 1
    assert len(updated_alerts) == 1
    assert len(expired_alerts) == 0
    assert new_alerts[0].description == 'test'
    assert updated_alerts[0].description == 'test 2'


def test_expire_one_alert(mocker: MockerFixture):
    def mock_consume(_, inactivity_timeout):
        assert inactivity_timeout == 1
        for i in [Message({'priority': 3, 'description': 'test', 'alert_key': '[something]', 'ttl': 1},
                          routing_key='test'),
                  None, None,
                  Message({'priority': 3, 'description': 'test', 'alert_key': '[something else]', 'ttl': 5},
                          routing_key='test'),
                  None, None]:
            sleep(0.5)
            yield i

    mocker.patch('legion_cli.alerts_manager.Subscriber.__init__', mock_init)
    mocker.patch('legion_cli.alerts_manager.Subscriber.bind', mock_bind)
    mocker.patch('legion_cli.alerts_manager.Subscriber.consume', mock_consume)

    new_alerts: List[AlertMsg] = []
    updated_alerts: List[AlertMsg] = []
    expired_alerts: List[AlertMsg] = []

    manager = AlertsManager(['skynet'],
                            num_alerts=2,
                            on_new=new_alerts.append,
                            on_update=updated_alerts.append,
                            on_expire=expired_alerts.append)
    manager.start()
    assert len(new_alerts) == 2
    assert len(updated_alerts) == 0
    assert len(expired_alerts) == 1
    assert new_alerts[0].key == '[something]'
    assert new_alerts[1].key == '[something else]'
    assert expired_alerts[0].key == '[something]'
