# Copyright 2017 Google Inc. All Rights Reserved.
#
"""Wrapper for Gcloud-installed Schema Conversion Tool."""

import os

import bootstrapping
from googlecloudsdk.command_lib.util import java
from googlecloudsdk.core.updater import update_manager

# Path to the unpacked component
_COMPONENT_DIR = os.path.join(bootstrapping.SDK_ROOT,
                              'platform', 'schema_conversion_tool')

# Path to the directory of unpacked jars relative to the SDK root
_JAR_DIR = os.path.join(_COMPONENT_DIR, 'lib')

_COMPONENT_ID = 'schema-conversion-tool'


def main():
  """Launches the Schema Conversion Tool."""
  bootstrapping.CommandStart(_COMPONENT_ID, component_id=_COMPONENT_ID)
  bootstrapping.CheckUpdates(_COMPONENT_ID)
  update_manager.UpdateManager.EnsureInstalledAndRestart(
      [_COMPONENT_ID], command=__file__)
  java_bin = java.RequireJavaInstalled('Schema Conversion Tool')
  os.environ.setdefault('SCT_UPDATE_CHECK', 'false')
  jar_name = 'schema_conversion_gui.jar'
  main_jar = os.path.join(_JAR_DIR, jar_name)

  # Accept a platform-appropriate default added as 1st arg in sct.sh/sct.cmd.
  argv = bootstrapping.GetDecodedArgv()[1:]
  working_dir_default = argv.pop(0)

  flags = [
      '-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager',
      '-Dspring.profiles.active=production',
      '-Dgcloud.component.dir={}'.format(_COMPONENT_DIR),
      '-Dsct.working.dir.default={}'.format(working_dir_default),
      '-jar',
      main_jar,
  ]

  main_args = ['--server.address=127.0.0.1'] + argv

  bootstrapping.ExecuteJarTool(
      java_bin,
      _JAR_DIR,
      jar_name,
      None,  # No main classname for Springboot JAR. Use -jar flag instead.
      flags,
      *main_args)


if __name__ == '__main__':
  main()
