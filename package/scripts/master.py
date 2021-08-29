# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script

from common import kuduHome, kuduCliUrl, kuduCli


class Master(Script):
    def install(self, env):
        Execute('yum install -y cyrus-sasl-plain')

        Execute('mkdir -p {0}'.format(kuduHome))

        Execute('wget --no-check-certificate {0} -O {1}'.format(kuduCliUrl, kuduCli))

        Execute('chmod +x ' + kuduCli)

        self.configure(env)

    def stop(self, env):
        Execute("ps -ef |grep '" + kuduCli + " master run'|grep -v grep|awk '{print $2}'|xargs kill -9")

    def start(self, env):
        self.configure(self)
        from params import kuduMasterConfig

        config = ''
        for key, value in kuduMasterConfig.iteritems():
            config += "-" + key + "=" + value

        Execute(
            "cd " + kuduHome + " && "
                               "nohup " + kuduCli + " master run " + config + " > master.out 2>&1 &"
        )
        # Execute(
        #     "cd "+kuduHome +" && "
        #     "nohup " + kuduCli + " master run -master_addresses={0} -fs_wal_dir={1} -fs_data_dirs={2} "
        #                          "-fs_metadata_dir={3} -log_dir={4} > master.out 2>&1 &".format(
        #         kuduMasterConfig['master_addresses'],
        #         kuduMasterConfig['fs_wal_dir'],
        #         kuduMasterConfig['fs_data_dirs'],
        #         kuduMasterConfig['fs_metadata_dir'],
        #         kuduMasterConfig['log_dir'],
        #     )
        # )

    def status(self, env):
        try:
            Execute(
                'export KUDU_MASTER_COUNT=`ps -ef |grep -v grep |grep "' + kuduCli + ' master run" | wc -l` '
                                                                                     '&& `if [ $KUDU_MASTER_COUNT -ne 0 ];then exit 0;else exit 3;fi ` '
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        from params import kuduMasterConfig

        Execute('mkdir -p {0}'.format(kuduMasterConfig['fs_wal_dir']))
        Execute('mkdir -p {0}'.format(kuduMasterConfig['fs_data_dirs']))
        Execute('mkdir -p {0}'.format(kuduMasterConfig['fs_metadata_dir']))
        Execute('mkdir -p {0}'.format(kuduMasterConfig['log_dir']))


if __name__ == '__main__':
    Master().execute()
