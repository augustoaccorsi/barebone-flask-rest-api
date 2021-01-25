from subprocess import Popen, PIPE
import os

RUNNING_INSTANCES = 'Running instances: '
APP_NAME = 'Application name: '
ENV_NAME = 'Environment details for:' 


def get_environment_name(output):
    aux = str(output).split(ENV_NAME)
    environmentName = aux[1].split('\\r\\n')
    return environmentName[0]

def get_application_name(output):
    aux = str(output).split(APP_NAME)
    applicationName = aux[1].split('\\r\\n')
    return applicationName[0]

def get_intances(output):
    aux = str(output).split(RUNNING_INSTANCES)
    runningIstances = aux[1].split('\\r\\n')
    return int(runningIstances[0])


p = Popen(['.\status.bat', 'arg1'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output = p.communicate()

instances = get_intances(output) + 1

os.system(r".\scale.bat " + str(instances) + " "+get_environment_name(output) )