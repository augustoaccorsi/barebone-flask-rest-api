from subprocess import Popen, PIPE
import os
import sys
import yaml

INSTANCE_ID = "InstanceId\": \""
CPU = "Idle\": "


def get_config_info():
    yaml_file = open("config.yaml")
    
    config_file = yaml.load(yaml_file, Loader=yaml.FullLoader)

    envName = config_file.get('branch-defaults').get('default').get('environment')
    appName = config_file.get('global').get('application_name')
    plataform = config_file.get('global').get('default_platform')
    region = config_file.get('global').get('default_region')

    return [envName, plataform.replace(" ", "-").lower() , region, appName]


def get_instances_ids(output):
    aux = str(output).split(INSTANCE_ID)
    instances = [None] * (len(aux)-1)
    count = 0
    for i in range(len(aux)):
        if i > 0:
            instances[count] = aux[i].split('\"')[0]
            count +=1
    return instances

def get_cpu(output):
    aux = str(output).split(CPU)
    cpu_idle = [None] * (len(aux)-1)
    count = 0
    for i in range(len(aux)):
        if i > 0:
            cpu_idle[count] = float(aux[i].split(',')[0])
            count +=1
    return cpu_idle

def scale(cpu_idle, instances, envName, appName):
    scaleUp = False
    scaleDown = False
    threasholdUp = 30
    threasholDown = 70

    for i in range(len(cpu_idle)):
        if cpu_idle[i] <= threasholdUp:
            scaleUp = True
        if cpu_idle[i] >= threasholDown:
            scaleDown = True

    if scaleUp:
        os.system(r".\bat-files\scale.bat " + str(len(instances) + 1) + " "+ envName)
        scaleUp = False
    
    if scaleDown:
        if len(cpu_idle) > 1:
            os.system(r".\bat-files\scale.bat " + str(len(instances) - 1) + " "+ envName)
        scaleDown = False
    
    if scaleDown == False and scaleUp == False:
        print("Aplication "+ appName +" of environment "+ envName +" should not be scaled, CPU's are working with the following capacity:")
        for i in range(len(cpu_idle)):
            print("Instace 1:")
            print("   Instance ID: "+ str(instances[i]))
            print("   CPU Usage: "+ str(100 - cpu_idle[i]))
            print("   CPU Idle: "+ str(cpu_idle[i]))

def main():

    config_info = get_config_info()

    envName = config_info[0]
    plataform = config_info[1]
    region = config_info[2]
    appName = config_info[3]

    os.system(r".\bat-files\init.bat " + plataform + " " + envName + " " + region )

    p = Popen(['bat-files\health.bat', envName, region], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output = p.communicate()[0]

    instances = get_instances_ids(output.decode('utf-8'))
    cpu_idle = get_cpu(output.decode('utf-8'))
    scale(cpu_idle, instances, envName, appName)

if __name__ == "__main__":
    main()  