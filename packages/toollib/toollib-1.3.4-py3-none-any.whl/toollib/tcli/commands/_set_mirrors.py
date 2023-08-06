"""
@author axiner
@version v1.0.0
@created 2022/5/11 21:44
@abstract
@description
@history
"""
import subprocess

from toollib.decorator import sys_required
from toollib.tcli import here
from toollib.tcli.base import BaseCmd
from toollib.tcli.option import Options


class Cmd(BaseCmd):

    def __init__(self):
        super().__init__()

    def add_options(self):
        options = Options(
            name='set-mirrors',
            desc='设置镜像源',
            optional={self.set_mirrors: None}
        )
        return options

    @sys_required(r'Ubuntu|CentOS|RedHat|Rocky')
    def set_mirrors(self):
        sh = here.joinpath('commands/plugins/set_mirrors.sh').as_posix()
        cmd = 'chmod u+x {sh} && {sh}'.format(sh=sh)
        subprocess.run(cmd, shell=True)
