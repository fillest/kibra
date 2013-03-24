from fabric.api import local, env, sudo, run, put
from fabric.utils import abort
from fabric.context_managers import lcd, prefix, settings
from fabric.utils import warn, puts
from fabric.contrib.console import confirm
from glob import glob
from os.path import basename, exists


BUILD_DIR = '/tmp/kibra_build'
REPO_URL = "https://bitbucket.org/fillest/kibra"


def bookmarklet ():
    local('yui-compressor --type js'
#        ' -o js.js'
        ' --nomunge kibra/static/js/bookmarklet.js'
    )


def create_schema ():
    if confirm('really run schema sql? this normally should be done initially and only once', default = False):
        remote_file = '/tmp/kibra_schema.sql'
        put(BUILD_DIR + '/schema.sql', remote_file)
        run('psql --dbname kibra --file %s --host localhost --port 5432 --username postgres' % remote_file)
        run('rm ' + remote_file)


def restart_supervisord ():
    if confirm('really restart supervisord? this will also restart all programs', default = False):
        sudo('sudo kill -HUP `sudo supervisorctl pid`')


def prepare (source):
    if source == 'repo':
        puts("Gonna build using repo %s" % REPO_URL)

        tmp_dir = '/tmp/kibra_checkout'

        local('hg clone %s %s' % (REPO_URL, tmp_dir))
        local('cd %s && hg archive %s' % (tmp_dir, BUILD_DIR))

        local('rm -r ' + tmp_dir)
    elif source == 'raw':
        puts("Gonna build using raw source %s" % BUILD_DIR)
        
        local('cp -r . ' + BUILD_DIR)
        local('rm -r %s/kibra.egg-info' % BUILD_DIR)
    else:
        raise NotImplementedError('source "%s" handling is not implemented' % source)

def build (source):
    prepare(source)

    with lcd(BUILD_DIR):
        local('tar czf /tmp/kibra_static.tar.gz -C kibra static')
        local('rm -r kibra/static')

        local('python setup.py sdist --formats=gztar --dist-dir sdist')


def clean ():
    local('rm -rf ' + BUILD_DIR)
    local('rm -f /tmp/kibra_static.tar.gz')

def upload_config ():
    #TODO improve
    if exists('production.ini'):
        put('production.ini', '/opt/kibra/', use_sudo = True, mode = 0400)
        sudo('chown kibra:kibra /opt/kibra/production.ini')
    else:
        warn('no production.ini found')

def upload_static ():
    put('/tmp/kibra_static.tar.gz', '/tmp/')
    sudo('rm -rf /opt/kibra/static')
    sudo('mkdir /opt/kibra/static', user = 'kibra')
    sudo('tar xzf /tmp/kibra_static.tar.gz -C /opt/kibra', user = 'kibra')
    sudo('rm /tmp/kibra_static.tar.gz')

def start ():
    sudo('supervisorctl start kibra')

def stop ():
    sudo('supervisorctl stop kibra')

def deploy (source = 'repo'):
    clean()
    build(source)

    # upload package
    sdist_path = glob(BUILD_DIR + '/sdist/kibra*.tar.gz')[0]
    sdist_fname = basename(sdist_path)
    sdist_remote_path = '/tmp/' + sdist_fname
    put(sdist_path, sdist_remote_path)

    stop()
    
    # install package
    with prefix('source /opt/kibra/venv/bin/activate'):
        # delete old package and force update
        sudo('(pip freeze | grep kibra) && pip uninstall --yes kibra || :', user = 'kibra')
        sudo('pip install ' + sdist_remote_path, user = 'kibra')
    run('rm ' + sdist_remote_path)

    upload_config()
    upload_static()

    start()

    clean()


def restart ():
#    sudo('kill -HUP `cat /opt/kibra/gunicorn.pid`')  # it's weirdly broken
    stop()
    start()
