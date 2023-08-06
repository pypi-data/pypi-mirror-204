from collections import namedtuple

from rich.panel import Panel

from legion_cli.tui.detail_list import DetailList, DetailElement


TestDetail = namedtuple('TestDetail', ['title', 'overview', 'details'])


def element_of(test: TestDetail) -> DetailElement:
    return DetailElement(f'{test.title}~{test.overview}', test,
                         render_details=lambda e: Panel(e.details),
                         render_overview=lambda e: Panel(e.overview),
                         style='white on black', focus_style='black on white')


def test_detail_list_initialization():
    detail1 = TestDetail('#1', 'The First Test', 'Pretty much the same as the other ones, but first')
    detail2 = TestDetail('#2', 'The Second Test', 'Pretty much the same as the other ones, but second')
    detail3 = TestDetail('#3', 'The Third Test', 'Pretty much the same as the other ones, but third')
    element1 = element_of(detail1)
    element2 = element_of(detail2)
    element3 = element_of(detail3)
    detail_list = DetailList[TestDetail](title='Tests',
                                         elements=[element1, element3, element2],
                                         sort_key=lambda e: e.title)
    assert detail_list.elements == [element1, element2, element3]
    assert not detail_list.display['details'].visible


def test_detail_list_add_elements():
    detail1 = TestDetail('#1', 'The First Test', 'Pretty much the same as the other ones, but first')
    detail2 = TestDetail('#2', 'The Second Test', 'Pretty much the same as the other ones, but second')
    detail3 = TestDetail('#3', 'The Third Test', 'Pretty much the same as the other ones, but third')
    element1 = element_of(detail1)
    element2 = element_of(detail2)
    element3 = element_of(detail3)
    detail_list = DetailList[TestDetail](title='Tests',
                                         sort_key=lambda e: e.title)
    assert detail_list.elements == []
    detail_list.add_element(element2)
    assert detail_list.elements == [element2]
    detail_list.add_element(element3)
    assert detail_list.elements == [element2, element3]
    detail_list.add_element(element1)
    assert detail_list.elements == [element1, element2, element3]


def test_detail_list_update_element():
    detail1 = TestDetail('#1', 'The First Test', 'Pretty much the same as the other ones, but first')
    detail2 = TestDetail('#2', 'The Second Test', 'Pretty much the same as the other ones, but second')
    detail3 = TestDetail('#3', 'The Third Test', 'Pretty much the same as the other ones, but third')
    detail4 = TestDetail('#4', 'The Fourth Test', 'Pretty much the same as the other ones, but fourth')
    element1 = element_of(detail1)
    element2 = element_of(detail2)
    element3 = element_of(detail3)
    element4 = element_of(detail4)
    detail_list = DetailList[TestDetail](title='Tests',
                                         elements=[element1, element3, element4],
                                         sort_key=lambda e: e.title)
    assert detail_list.elements == [element1, element3, element4]
    detail_list.update_element('#4~The Fourth Test', detail2)
    assert detail_list.elements[1].element is detail2


def test_detail_list_add_and_remove_elements():
    detail1 = TestDetail('#1', 'The First Test', 'Pretty much the same as the other ones, but first')
    detail2 = TestDetail('#2', 'The Second Test', 'Pretty much the same as the other ones, but second')
    detail3 = TestDetail('#3', 'The Third Test', 'Pretty much the same as the other ones, but third')
    element1 = element_of(detail1)
    element2 = element_of(detail2)
    element3 = element_of(detail3)
    detail_list = DetailList[TestDetail](title='Tests',
                                         sort_key=lambda e: e.title)
    assert detail_list.elements == []
    detail_list.add_element(element2)
    assert detail_list.elements == [element2]
    detail_list.add_element(element3)
    assert detail_list.elements == [element2, element3]
    detail_list.add_element(element1)
    assert detail_list.elements == [element1, element2, element3]
    detail_list.remove_element('#2~The Second Test')
    assert detail_list.elements == [element1, element3]


def test_detail_list_remove_none():
    detail1 = TestDetail('#1', 'The First Test', 'Pretty much the same as the other ones, but first')
    detail2 = TestDetail('#2', 'The Second Test', 'Pretty much the same as the other ones, but second')
    detail3 = TestDetail('#3', 'The Third Test', 'Pretty much the same as the other ones, but third')
    element1 = element_of(detail1)
    element2 = element_of(detail2)
    element3 = element_of(detail3)
    detail_list = DetailList[TestDetail](title='Tests',
                                         elements=[element1, element3, element2],
                                         sort_key=lambda e: e.title)
    detail_list.remove_element('not an element identifier')
    assert detail_list.elements == [element1, element2, element3]


def test_detail_list_remove_element():
    detail1 = TestDetail('#1', 'The First Test', 'Pretty much the same as the other ones, but first')
    detail2 = TestDetail('#2', 'The Second Test', 'Pretty much the same as the other ones, but second')
    detail3 = TestDetail('#3', 'The Third Test', 'Pretty much the same as the other ones, but third')
    element1 = element_of(detail1)
    element2 = element_of(detail2)
    element3 = element_of(detail3)
    detail_list = DetailList[TestDetail](title='Tests',
                                         elements=[element1, element3, element2],
                                         sort_key=lambda e: e.title)
    detail_list.remove_element(element1)
    assert detail_list.elements == [element2, element3]


def test_detail_list_basic_focus_down():
    detail1 = TestDetail('#1', 'The First Test', 'Pretty much the same as the other ones, but first')
    detail2 = TestDetail('#2', 'The Second Test', 'Pretty much the same as the other ones, but second')
    detail3 = TestDetail('#3', 'The Third Test', 'Pretty much the same as the other ones, but third')
    element1 = element_of(detail1)
    element2 = element_of(detail2)
    element3 = element_of(detail3)
    detail_list = DetailList[TestDetail](title='Tests',
                                         elements=[element1, element3, element2],
                                         sort_key=lambda e: e.title)
    assert not detail_list.display['details'].visible
    detail_list.move_focus_down()
    assert detail_list.focus.element is detail1
    assert detail_list.display['details'].visible
    assert str(detail_list.display['details'].renderable.renderable) == 'Pretty much the same as the other ones, but first'


def test_detail_list_basic_focus_up():
    detail1 = TestDetail('#1', 'The First Test', 'Pretty much the same as the other ones, but first')
    detail2 = TestDetail('#2', 'The Second Test', 'Pretty much the same as the other ones, but second')
    detail3 = TestDetail('#3', 'The Third Test', 'Pretty much the same as the other ones, but third')
    element1 = element_of(detail1)
    element2 = element_of(detail2)
    element3 = element_of(detail3)
    detail_list = DetailList[TestDetail](title='Tests',
                                         elements=[element1, element3, element2],
                                         sort_key=lambda e: e.title)
    detail_list.move_focus_up()
    assert detail_list.focus.element is detail3


def test_detail_list_remove_focus_element():
    detail1 = TestDetail('#1', 'The First Test', 'Pretty much the same as the other ones, but first')
    detail2 = TestDetail('#2', 'The Second Test', 'Pretty much the same as the other ones, but second')
    detail3 = TestDetail('#3', 'The Third Test', 'Pretty much the same as the other ones, but third')
    element1 = element_of(detail1)
    element2 = element_of(detail2)
    element3 = element_of(detail3)
    detail_list = DetailList[TestDetail](title='Tests',
                                         elements=[element1, element3, element2],
                                         sort_key=lambda e: e.title)
    detail_list.move_focus_up()
    assert detail_list.focus.element is detail3
    detail_list.remove_element(detail3)
    assert detail_list.focus is None
    assert not detail_list.display['details'].visible
    assert detail_list.element(detail3) is None


def test_detail_list_update_focus_element():
    detail1 = TestDetail('#1', 'The First Test', 'Pretty much the same as the other ones, but first')
    detail2 = TestDetail('#2', 'The Second Test', 'Pretty much the same as the other ones, but second')
    detail3 = TestDetail('#3', 'The Third Test', 'Pretty much the same as the other ones, but third')
    detail4 = TestDetail('#4', 'The Fourth Test', 'Pretty much the same as the other ones, but fourth')
    element1 = element_of(detail1)
    element2 = element_of(detail2)
    element3 = element_of(detail3)
    element4 = element_of(detail4)
    detail_list = DetailList[TestDetail](title='Tests',
                                         elements=[element1, element3, element4],
                                         sort_key=lambda e: e.title)
    assert detail_list.elements == [element1, element3, element4]
    detail_list.move_focus_up()
    detail_list.update_element('#4~The Fourth Test', detail2)
    assert detail_list.focus.element is detail2
    assert detail_list.display['details'].visible
    assert str(detail_list.display['details'].renderable.renderable) == 'Pretty much the same as the other ones, but second'


def test_detail_list_basic_focus_scroll_up():
    detail1 = TestDetail('#1', 'The First Test', 'Pretty much the same as the other ones, but first')
    detail2 = TestDetail('#2', 'The Second Test', 'Pretty much the same as the other ones, but second')
    detail3 = TestDetail('#3', 'The Third Test', 'Pretty much the same as the other ones, but third')
    element1 = element_of(detail1)
    element2 = element_of(detail2)
    element3 = element_of(detail3)
    detail_list = DetailList[TestDetail](title='Tests',
                                         elements=[element1, element3, element2],
                                         sort_key=lambda e: e.title)
    detail_list.move_focus_up()
    assert detail_list.focus.element is detail3
    detail_list.move_focus_up()
    assert detail_list.focus.element is detail2
    detail_list.move_focus_up()
    assert detail_list.focus.element is detail1
    detail_list.move_focus_up()
    assert detail_list.focus is None


def test_detail_list_basic_focus_scroll_down():
    detail1 = TestDetail('#1', 'The First Test', 'Pretty much the same as the other ones, but first')
    detail2 = TestDetail('#2', 'The Second Test', 'Pretty much the same as the other ones, but second')
    detail3 = TestDetail('#3', 'The Third Test', 'Pretty much the same as the other ones, but third')
    element1 = element_of(detail1)
    element2 = element_of(detail2)
    element3 = element_of(detail3)
    detail_list = DetailList[TestDetail](title='Tests',
                                         elements=[element1, element3, element2],
                                         sort_key=lambda e: e.title)
    detail_list.move_focus_down()
    assert detail_list.focus.element is detail1
    detail_list.move_focus_down()
    assert detail_list.focus.element is detail2
    detail_list.move_focus_down()
    assert detail_list.focus.element is detail3
    detail_list.move_focus_down()
    assert detail_list.focus is None