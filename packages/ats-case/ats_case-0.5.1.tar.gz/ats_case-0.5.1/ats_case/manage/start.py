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
        self._sn = self._username.upper() + self._now()

    def run(self):
        pass

    def _now(self):
        return datetime.now().strftime('%y%m%d%H%M%S%f')

    def _save(self):
        pass

    def _flush(self, **kwargs):
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
    def run(self):
        self._save()
        cases = self._data.pop('cases')
        meters = self._data.pop('meters')

        for case in cases:
            for meter in meters:
                self._flush(case=case, meter=meter)
                # i = 0 执行操作表台 传入参数index
                # th = threading.Thread(target=self._exec, daemon=True)
                # th.start()
                self._exec()

    def _exec(self):
        pytest.main(
            ["-sv", self._build(WorkMode.FORMAL), '--sn={}'.format(self._sn)])

    def _save(self):
        pass  # 存数据库

    def _flush(self, **kwargs):
        self._data['usercase'] = kwargs['case']
        self._data['meter'] = kwargs['meter']
        self._sn += ':{}:{}'.format(kwargs['case']['id'], kwargs['meter']['pos'])
        mm.Dict.put('test:log', self._sn, self._data)


class DebugMode(ExecMode):
    def __init__(self, data: dict):
        super().__init__(data)

    def run(self):
        self._flush()
        pytest.main(["-sv", self._build(WorkMode.DEBUG), '--sn={}'.format(self._sn)])

    def _flush(self):
        case = self._data.get('usercase')
        meter = self._data.get('meter')
        self._sn += ':{}:{}'.format(case['id'], meter['pos'])
        mm.Dict.put('test:log', self._sn, self._data)
