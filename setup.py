from distutils.core import setup
import glob
import sys

NAME = 'argo-probe-ams-push-server'
NAGIOSPLUGINS = '/usr/libexec/argo/probes/ams-push-server'


def get_ver():
    try:
        for line in open(NAME + '.spec'):
            if "Version:" in line:
                return line.split()[1]
    except IOError:
        print("Make sure that %s is in directory" % (NAME + '.spec'))
        sys.exit(1)


setup(name=NAME,
      version=get_ver(),
      license='ASL 2.0',
      author='SRCE, GRNET',
      author_email='agelostsal@admin.grnet.gr',
      description='Package include probes for ARGO AMS Push Server component',
      platforms='noarch',
      url='https://github.com/ARGOeu-Metrics/argo-probe-ams-push-server',
      data_files=[(NAGIOSPLUGINS, glob.glob('src/*'))],
      packages=['argo_probe_ams_push_server'],
      package_dir={'argo_probe_ams_push_server': 'modules/'},
    )