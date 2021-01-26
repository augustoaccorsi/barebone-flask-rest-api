from subprocess import Popen, PIPE
import os
import sys

INSTANCE_ID = "InstanceId\": \""
CPU = "Idle\": "

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
        os.system(r".\scale.bat " + str(len(instances) + 1) + " "+ envName)
        scaleUp = False
    
    if scaleDown:
        if len(cpu_idle) > 1:
            os.system(r".\scale.bat " + str(len(instances) - 1) + " "+ envName)
        scaleDown = False
    
    if scaleDown == False and scaleUp == False:
        print("Aplication "+ appName +" of environment"+ envName +" should not be scaled, CPU's are working with the following capacity:")
        for i in range(len(cpu_idle)):
            print("Instace 1:")
            print("   Instance ID: "+ str(instances[i]))
            print("   CPU Usage: "+ str(100 - cpu_idle[i]))
            print("   CPU Idle: "+ str(cpu_idle[i]))

def main():

    appName = sys.argv[1]
    envName = sys.argv[2]
    plataform = sys.argv[3]
    region = sys.argv[4]

    os.system(r".\init.bat " + plataform + " " + envName + " " + region )

    p = Popen(['.\health.bat', envName, region], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output = p.communicate()[0]

    instances = get_instances_ids(output.decode('utf-8'))
    cpu_idle = get_cpu(output.decode('utf-8'))
    scale(cpu_idle, instances, envName, appName)

if __name__ == "__main__":
    main()  