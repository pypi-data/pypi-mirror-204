"""
@author axiner
@version v1.0.0
@created 2022/5/4 9:17
@abstract
@description
@history
"""
import subprocess

from toollib.decorator import sys_required
from toollib.tcli import here
from toollib.tcli.base import BaseCmd
from toollib.tcli.option import Options, Arg


class Cmd(BaseCmd):

    def __init__(self):
        super().__init__()

    def add_options(self):
        options = Options(
            name='set-sshkey',
            desc='设置ssh免密',
            optional={
                self.set_sshkey: [
                    Arg('-i', '--infos', required=True, type=str, help='"ip1,user1,pass1,port1 ip2,user2,pass2,port2 ..."|也可指定文件:一行一个'),
                ]}
        )
        return options

    @sys_required(r'Ubuntu|CentOS|RedHat|Rocky')
    def set_sshkey(self):
        infos = self.parse_args.infos
        sh = here.joinpath('commands/plugins/set_sshkey.sh')
        cmd = 'chmod u+x {sh} && {sh} "{infos}"'.format(sh=sh, infos=infos)
        subprocess.run(cmd, shell=True)
