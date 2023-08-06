import os
import threading

import pytest

from datetime import datetime

from ats_base.common import func
from ats_base.service import mm

from ats_case.common.enum import WorkMode


def run(**kwargs):
    try:
        mode = WorkMode(kwargs.get('mode'))
        if mode == WorkMode.FORMAL:
            pt = FormalMode(kwargs)
        else:
            pt = DebugMode(kwargs)
        pt.run()
    except:
        pass


class ExecMode(object):
    def __init__(self, data: dict):
        self._data = data
        self._username = self._data.get('tester').get('username', '')
        self._now = datetime.now().strftime('%y%m%d%H%M%S%f')

        self._init()

    def run(self):
        pass

    def _init(self):
        pass

    def _build(self, work_mode: WorkMode, code: str = None):
        if code is None:
            code = 'case'

        user_dir = func.makeDir(func.project_dir(), 'testcase', work_mode.value.lower(), self._username)
        template_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'template', 'testcase_v1.tmp')
        script_file = os.path.join(user_dir, 'test_{}.py'.format(code))

        with open(template_file, 'r', encoding='UTF-8') as file:
            content = file.read()
            content = content.replace('{script}', code.upper())
        with open(script_file, 'w', encoding='UTF-8') as file:
            file.write(content)

        return script_file


class FormalMode(ExecMode):
    def _init(self):
        self._sn = self._data.get('test_sn')
        if self._sn is None or len(self._sn) == 0:
            self._sn = self._username.upper() + self._now
            mm.Dict.put('test:log', self._sn, self._data)
            self._save()
        else:  # 断点续测
            self._data = mm.Dict.get('test:log', self._sn)
            self._data['renew'] = 1

        self._cases = self._data.pop('cases')
        self._meters = self._data.pop('meters')

        self._test_sn = None

    def run(self):
        for case in self._cases:
            test_task = self.TestTask(self, case, self._meters)
            test_task.start()
            test_task.join()

    class TestTask(threading.Thread):
        def __init__(self, parent, case, meters):
            super(FormalMode.TestTask, self).__init__()
            self._parent = parent
            self._case = case
            self._meters = meters

        def run(self):
            for meter in self._meters:
                self._parent.flush(case=self._case, meter=meter)
                # i = 0 执行操作表台 传入参数index
                th = threading.Thread(target=self._parent.exec, daemon=True)
                th.start()

    def exec(self):
        pytest.main(
            ["-sv", self._build(WorkMode.FORMAL), '--sn={}'.format(self._test_sn)])

    def _save(self):
        pass  # 存数据库

    def flush(self, case, meter):
        self._data['usercase'] = case
        self._data['meter'] = meter
        self._test_sn = '{}:{}:{}'.format(self._sn, case['id'], meter['pos'])
        mm.Dict.put('test:log', '{}:{}:{}'.format(self._sn, case['id'], meter['pos']), self._data)


class DebugMode(ExecMode):
    def _init(self):
        self._sn = '{}:{}:{}'.format(self._username.upper() + self._now,
                                     self._data['usercase']['id'], self._data['meter']['pos'])
        mm.Dict.put('test:log', self._sn, self._data)

    def run(self):
        pytest.main(["-sv", self._build(WorkMode.DEBUG), '--sn={}'.format(self._sn)])
