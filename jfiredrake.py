import docker
import re
import webbrowser
import time
import sys


def start_instance():

    port = 8888

    client = docker.from_env()
    client.images.pull('stephankramer/jhub-notebook-firedrake')

    try:
        volume = client.volumes.get('fd_app')
    except docker.errors.NotFound:
        print("No volume found.")
        print("Creating new volume.")
        volume = client.volumes.create('fd_app')

    name = 'firedrake%d'%port
    while True:
        try:
            print("Trying to run on port %d"%port)
            cont = client.containers.run('stephankramer/jhub-notebook-firedrake',
                                         name=name, detach=True,
                                         volumes={'fd_app': {'bind':'/home/jovyan',
                                                             'mode':'rw'}},
                                         ports={8888:port})
            break
        except docker.errors.APIError as e:
            print(e)
            cont = client.containers.get(name)
            cont.stop()
            cont.remove()
            port += 1
            name = 'firedrake%d'%port
        
    time.sleep(3)
    return cont, port
    

def open_browser(cont, port):

    booklist = cont.exec_run('jupyter notebook list')
    token=re.findall(b'(?<=\?token=)[0-9a-f]+',
                     booklist)[0]
    webbrowser.open_new('http://localhost:%s/?token=%s'%(port,
                                                         token.decode()))
