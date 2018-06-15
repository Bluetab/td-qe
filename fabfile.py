from fabric.api import (local, put, run, env, serial)

# the user to use for the remote commands
env.user = 'ec2-user'
# the servers where the commands are executed
env.hosts = ['truedat.bluetab.net']

@serial
def pack():
    # build the package
    local('pip install -e .', capture=False)
    local('python setup.py sdist --formats=gztar', capture=False)

@serial
def deploy():
    # figure out the package name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    filename = '%s.tar.gz' % dist

    # upload the package to the temporary folder on the server
    put('dist/%s' % filename, '/tmp/%s' % filename)

    # upload env
    run('mkdir -p /home/ec2-user/td_qe')
    run('mkdir -p /home/ec2-user/td_qe/scripts')
    run('mkdir -p /home/ec2-user/td_qe/results')
    run('sudo rm -rf /home/ec2-user/td_qe/venv')
    run('virtualenv -p python3 /home/ec2-user/td_qe/venv')

    # install the package in the application's virtualenv with pip
    run('/home/ec2-user/td_qe/venv/bin/pip install /tmp/%s' % filename, timeout=40)

    # remove the uploaded package
    run('rm -r /tmp/%s' % filename)

    # restart lineage service
    run('touch /home/ec2-user/td_qe/wsgi.py && \
         rm /home/ec2-user/td_qe/wsgi.py')
    put("wsgi.py", "/home/ec2-user/td_qe/wsgi.py")
    put("scripts/launchApp.sh",
        "/home/ec2-user/td_qe/scripts/launchApp.sh")
    run("chmod 755 /home/ec2-user/td_qe/scripts/launchApp.sh")

    run("/home/ec2-user/td_qe/scripts/launchApp.sh stop && \
        /home/ec2-user/td_qe/scripts/launchApp.sh start")
