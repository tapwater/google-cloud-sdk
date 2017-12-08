#!/usr/bin/env python
#
# Copyright 2015 Google Inc. All Rights Reserved.
#

"""A convenience wrapper for starting dev_appserver for appengine for python."""

import os

import bootstrapping.bootstrapping as bootstrapping

from googlecloudsdk.core.updater import update_manager


def main():
  """Launches dev_appserver.py."""
  update_manager.UpdateManager.EnsureInstalledAndRestart(
      ['app-engine-java', 'app-engine-python', 'app-engine-php'],
      command=__file__)

  args = [
      '--skip_sdk_update_check=True'
  ]

  bootstrapping.ExecutePythonTool(
      os.path.join('platform', 'google_appengine'), 'dev_appserver.py', *args)


if __name__ == '__main__':
  bootstrapping.CommandStart('dev_appserver', component_id='core')
  bootstrapping.CheckUpdates('dev_appserver')
  main()
