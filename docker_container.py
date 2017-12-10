import os, sys
from docker import Client
from datetime import datetime
from time import mktime

from .logger import getlogger
import logging
#logger = getlogger(logging.DEBUG, logging.StreamHandler())
logger = getlogger()

from .celery import app
    
appdir = os.path.abspath(os.path.dirname(__file__))

def ghost_container(cli, image="myghost:latest"):
    cli = Client(base_url='unix://var/run/docker.sock')
    cid = None
    if cli:
        container = cli.create_container(
            image=image,
            working_dir="/myghost",
            #command="/usr/bin/run.sh",
            stdin_open=True,
            tty=True,
            volumes=['/myghost'],
            host_config=cli.create_host_config(
                binds={
                    appdir + '/ghost': {
                        'bind': '/myghost',
                        'mode': 'rw',
                    },
                },
                privileged=True,
            ),
        )
        cid = container.get('Id')
    return cid


@app.task(soft_time_limit=600)
def container_killer(ttl, image="myghost:latest"):
    cli = Client(base_url='unix://var/run/docker.sock')
    cs = cli.containers(all=True)
    for c in cs:
        try:
            n = int(mktime(datetime.now().timetuple()))
            if n - c["Created"] > ttl and c["Image"] == image:
                cli.stop(c["Id"], timeout=300)
                cli.remove_container(c["Id"], force=True)
                logger.debug("Container removed: " + str(c["Id"]))
        except Exception as e:
            logger.debug("Failed: " + str(e))
                
if __name__ == '__main__':
    container_killer()
