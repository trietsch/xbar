# Bitbar scripts

## Gitlab
Integrates with (multiple) Gitlab hosts and shows the status like CCMenu does. At the moment, Gitlab does not offer a `cc.xml` that Jenkins does, so this is a workaround.

**Note**: bugs may still exist.

To change the settings, copy the `.gitlab-config.template.ini` to `.gitlab-config.template` and adjust to your own preferences. By default, only projects are included that you've starred and of which you're a member. So if you don't change that behavior, go to the Gitlab instances and star the projects that you want to see.

**Important**: change the hashbang at the top of the file, to point to a Python 3 executable.

### Dependencies

- python-dateutil
- requests