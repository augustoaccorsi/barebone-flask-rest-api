from subprocess import Popen, PIPE
import os
import sys

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

def main():
    os.system(r".\init.bat " + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3] )

    p = Popen(['.\status.bat', 'arg1'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output = p.communicate()

    instances = get_intances(output) - 1
    envName = get_environment_name(output)
    appName = get_application_name(output)

    if instances == 0:
        print("Aplication "+ appName +" of environment"+ envName +" has already 1 instance, scale down cannot be executed")
    else:
        os.system(r".\scale.bat " + str(instances) + " "+ envName )

if __name__ == "__main__":
    main()