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
    print("Aplication "+ appName +" of environment "+ envName +" scaled up to "+ str(len(instances) - 1) +" instance(s) with sucess")
    print("Instances view:")
    for i in range(len(cpu_idle)):
        print("Instace "+str(i+1)+":")
        print(" - Instance ID: "+ str(instances[i]))
        print(" - CPU Usage: "+ str(100 - cpu_idle[i]))
        print(" - CPU Idle: "+ str(cpu_idle[i]))


def scale_down(envName, appName, region):
    output = get_health_output(envName, region)
    instances = get_instances_ids(output)
    cpu_idle = get_cpu(output)

    os.system(r".\bat-files\scale.bat " + str(len(instances) - 1) + " "+ envName)

    output = get_health_output(envName, region)
    instances = get_instances_ids(output)
    cpu_idle = get_cpu(output)
    
    print_output(appName, envName, instances, cpu_idle)

def main():
    config_info = get_config_info()

    envName = config_info[0]
    plataform = config_info[1]
    region = config_info[2]
    appName = config_info[3]

    os.system(r".\bat-files\init.bat " + plataform + " " + envName + " " + region )
    
    scale_down(envName, appName, region)

if __name__ == "__main__":
    main()  