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

def get_health_output(envName, region):
    p = Popen(['bat-files\health.bat', envName, region], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output = p.communicate()[0]

    return output.decode('utf-8')
    
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

def print_output(appName, envName, instances, cpu_idle):
    if scaleDown == False and scaleUp == False:
        print("Aplication "+ appName +" of environment "+ envName +" should not be scaled, CPU's are working with the following capacity:")
    else:
         print("Aplication "+ appName +" of environment "+ envName +" scaled to "+ str(len(instances)) +" instance(s), CPU's are working with the following capacity:")
    for i in range(len(cpu_idle)):
        print("Instace "+str(i)+":")
        print("   Instance ID: "+ str(instances[i]))
        print("   CPU Usage: "+ str(100 - cpu_idle[i]))
        print("   CPU Idle: "+ str(cpu_idle[i]))

def scale(envName, appName, region):
    scaleUp = False
    scaleDown = False
    threasholdUp = 30
    threasholDown = 70

    output = get_health_output(envName, region)
    instances = get_instances_ids(output)
    cpu_idle = get_cpu(output)

    count = 0
    for i in range(len(cpu_idle)):
        if cpu_idle[i] <= threasholdUp:
            scaleUp = True
            count += 1
        if cpu_idle[i] >= threasholDown:
            scaleDown = True
            count += 1

    if scaleUp:
        os.system(r".\bat-files\scale.bat " + str(len(instances) + count) + " "+ envName)
        scaleUp = False
    
    if scaleDown:
        if len(cpu_idle) > 1:
            if count == len(instances):
                count =- 1
            os.system(r".\bat-files\scale.bat " + str(len(instances) - count) + " "+ envName)
        scaleDown = False

    output = get_health_output(envName, region)
    instances = get_instances_ids(output)
    cpu_idle = get_cpu(output)
    


def main():
    config_info = get_config_info()

    envName = config_info[0]
    plataform = config_info[1]
    region = config_info[2]
    appName = config_info[3]

    os.system(r".\bat-files\init.bat " + plataform + " " + envName + " " + region )
    
    scale(envName, appName, region)

if __name__ == "__main__":
    main()  