# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import table_format
import pprint


def proceed_executions(client, logger, operation, deployment_id, workflow_id,
                       parameters, execution_id, force):
    operations = {'list': _list,
                  'start': _start,
                  'cancel': _cancel,
                  'get': _get}
    try:
        operations[operation](
            client, logger, deployment_id, workflow_id, parameters,
            execution_id, force)
    except KeyError:
        logger.error('Unknown operation')


def _list(client, logger, deployment_id, *args):
    logger.info('Getting executions list... for {}'.format(deployment_id))
    format_struct = (
        ('id', 40),
        ('deployment_id', 20),
        ('status', 30),
        ('workflow_id', 30),
        ('created_at', 27)
    )
    executions = client.executions.list(deployment_id)
    if executions:
        table_format.print_header(format_struct)
        for execution in executions:
            table_format.print_row(execution, format_struct)


def _start(client, logger, deployment_id, workflow_id, parameters, *args):
    if not deployment_id or not workflow_id:
        logger.info("Please specify -w for workflow and -d for deployment")
        return
    logger.info('Executions start {0}'.format(deployment_id))
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(client.executions.start(deployment_id, workflow_id, parameters))


def _cancel(client, logger, deployment_id, workflow_id,
            parameters, execution_id, force):
    logger.info('Executions cancel {0}'.format(execution_id))
    if not execution_id:
        logger.info("Execution not specified")
        return
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(client.executions.cancel(execution_id, force))


def _get(client, logger, workflow_id, deployment, parameters,
         execution_id, force):
    logger.info('Executions get {0}'.format(execution_id))
    if not execution_id:
        logger.info("Execution not specified")
        return
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(client.executions.get(execution_id))
