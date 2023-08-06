Table of contents
~~~~~~~~~~~~~~~~~

1.  `About <#About>`__
2.  `Screenshots <#Screenshots>`__
3.  `Installation <#Installation>`__
4.  `Requirements <#Requirements>`__
5.  `Recommended <#Recommended>`__
6.  `Testing <#Testing>`__
7.  `Command Line Tool Usage <#Command-Line-Tool-Usage>`__
8.  `How to start <#How-to-start>`__
9.  `Configuration files <#Configuration-files>`__
10. `Repositories <#Repositories>`__
11. `Multilib Packages <#Multilib-Packages>`__
12. `Issues <#Issues>`__
13. `Donate <#Donate>`__
14. `Support <#Support>`__
15. `Copyright <#Copyright>`__

About
~~~~~

Slpkg is a software package manager that installs, updates and removes
packages on `Slackware <https://www.slackware.com>`__-based systems. It
automatically calculates dependencies and figures out what things need
to happen to install packages. Slpkg makes it easier to manage groups of
machines without the need for manual updates. Slpkg works in accordance
with the standards of the
`slackbuilds.org <https://www.slackbuilds.org>`__ organization to build
packages. It also uses the Slackware Linux instructions for installing,
upgrading or removing packages.

Screenshots
~~~~~~~~~~~

::

   $ slpkg repo-info

::

   $ slpkg install audacity --bin-repo=alien

::

   $ slpkg remove audacity

::

   $ slpkg dependees --pkg-version --full-reverse greenlet

::

   $ slpkg tracking --pkg-version slpkg Flask awscli

Installation
~~~~~~~~~~~~

::

   $ tar xvf slpkg-4.8.0.tar.gz
   $ cd slpkg-4.8.0
   $ ./install.sh

Requirements
~~~~~~~~~~~~

::

   SQLAlchemy >= 1.4.46
   pythondialog >= 3.5.3
   progress >= 1.6

Recommended
~~~~~~~~~~~

Stay always updated, see my other project SUN `(Slackware Update
Notifier) <https://gitlab.com/dslackw/sun>`__

Testing
~~~~~~~

The majority of trials have been made in Slackware x86_64 ‘stable’
environment.

Command Line Tool Usage
~~~~~~~~~~~~~~~~~~~~~~~

::

   USAGE: slpkg [OPTIONS] [COMMAND] [FILELIST|PACKAGES...]

   DESCRIPTION: Package manager utility for Slackware.

   COMMANDS:
     -u, update                    Update the package lists.
     -U, upgrade                   Upgrade all the packages.
     -c, check-updates             Check for news on ChangeLog.txt.
     -I, repo-info                 Prints the repositories information.
     -g, configs                   Edit the configuration file.
     -L, clean-logs                Clean dependencies log tracking.
     -T, clean-data                Clean all the repositories data.
     -D, clean-tmp                 Delete all the downloaded sources.
     -b, build [packages...]       Build only the packages.
     -i, install [packages...]     Build and install the packages.
     -d, download [packages...]    Download only the scripts and sources.
     -R, remove [packages...]      Remove installed packages.
     -f, find [packages...]        Find installed packages.
     -w, view [packages...]        View packages from the repository.
     -s, search [packages...]      Search packages from the repository.
     -e, dependees [packages...]   Show which packages depend.
     -t, tracking [packages...]    Tracking the packages dependencies.

   OPTIONS:
     -y, --yes                     Answer Yes to all questions.
     -j, --jobs                    Set it for multicore systems.
     -o, --resolve-off             Turns off dependency resolving.
     -r, --reinstall               Upgrade packages of the same version.
     -k, --skip-installed          Skip installed packages.
     -E, --full-reverse            Full reverse dependency.
     -S, --search                  Search packages from the repository.
     -n, --no-silent               Disable silent mode.
     -p, --pkg-version             Print the repository package version.
     -G, --generate-only           Generates only the SLACKBUILDS.TXT file.
     -B, --bin-repo=[REPO]         Set a binary repository.
     -z, --directory=[PATH]        Download files to a specific path.

     -h, --help                    Show this message and exit.
     -v, --version                 Print version and exit.

How to start
~~~~~~~~~~~~

If you are going to use only the
`SlackBuilds.org <https://slackbuilds.org>`__ repository, you don’t need
to edit the ``/etc/slpkg/repositories.toml`` file, otherwise edit the
file and set ``true`` the repositories you want.

The second step is to update the package lists and install the data to
the database, just run:

::

       $ slpkg update

or for binary repositories:

::

       $ slpkg update --bin-repo='*'

Now you are ready to start!

To install a package from the
`SlackBuilds.org <https://slackbuilds.org>`__ or
`Ponce <https://cgit.ponce.cc/slackbuilds>`__ repository, run:

::

       $ slpkg install <package_name>

or from a binary repository:

::

       $ slpkg install <package_name> --bin-repo=<repo_name>

You can install a whole repository with the command:

::

       $ slpkg install '*' --bin-repo=<repository_name> --resolve-off

To remove a package with the dependencies:

::

       $ slpkg remove <package_name>

If you want to search a package from all binaries repositories, run:

::

       $ slpkg search <package_name> --bin-repo='*'

Edit the configuration ``/etc/slpkg/slpkg.toml`` file:

::

       $ slpkg configs

For further information, please read the manpage:

::

       $ man slpkg

Configuration files
~~~~~~~~~~~~~~~~~~~

::

   /etc/slpkg/slpkg.toml
       General configuration of slpkg
       
   /etc/slpkg/repositories.toml
       Repositories configuration

   /etc/slpkg/blacklist.toml
       Blacklist of packages

Repositories
~~~~~~~~~~~~

This is the list of the supported repositories:

-  `Slackbuilds <https://slackbuilds.org/>`__
-  `Ponce <https://cgit.ponce.cc/slackbuilds/>`__
-  `Slackware <https://slackware.uk/slackware/slackware64-15.0/>`__
-  `Slackware
   Extra <https://slackware.uk/slackware/slackware64-15.0/extra/>`__
-  `Slackware
   Patches <https://slackware.uk/slackware/slackware64-15.0/patches/>`__
-  `Alien <http://slackware.uk/people/alien/sbrepos/15.0/x86_64/>`__
-  `Multilib <https://slackware.nl/people/alien/multilib/15.0/>`__
-  `Restricted <https://slackware.nl/people/alien/restricted_sbrepos/15.0/x86_64/>`__
-  `Gnome <https://reddoglinux.ddns.net/linux/gnome/41.x/x86_64/>`__
-  `Msb <https://slackware.uk/msb/15.0/1.26/x86_64/>`__
-  `Csb <https://slackware.uk/csb/15.0/x86_64/>`__
-  `Conraid <https://slack.conraid.net/repository/slackware64-current/>`__
-  `Slackonly <https://packages.slackonly.com/pub/packages/15.0-x86_64/>`__
-  `SalixOS <https://download.salixos.org/x86_64/slackware-15.0/>`__
-  `SalixOS
   Extra <https://download.salixos.org/x86_64/slackware-15.0/extra/>`__
-  `SalixOS
   Patches <https://download.salixos.org/x86_64/slackware-15.0/patches/>`__
-  `Slackel <http://www.slackel.gr/repo/x86_64/current/>`__
-  `Slint <https://slackware.uk/slint/x86_64/slint-15.0/>`__

Multilib Packages
~~~~~~~~~~~~~~~~~

Slackware for x86_64 - multilib packages & install instructions:

Please read the file
`README <https://gitlab.com/dslackw/slpkg/-/raw/master/filelists/multilib/README>`__
you will find in the folder
`multlib <https://gitlab.com/dslackw/slpkg/-/tree/master/filelists/multilib>`__

Issues
~~~~~~

Please report any bugs in
`ISSUES <https://gitlab.com/dslackw/slpkg/issues>`__

Donate
~~~~~~

If you feel satisfied with this project and want to thank me, treat me
to a coffee ☕ !

` <https://www.paypal.me/dslackw>`__

Support
~~~~~~~

Please support:

-  `Slackware <https://www.patreon.com/slackwarelinux>`__ project.
-  `SlackBuilds <https://slackbuilds.org/contributors/>`__ repository.
-  `AlienBob <https://alien.slackbook.org/blog/>`__ Eric Hameleers.

Thank you all for your support!

Copyright
~~~~~~~~~

Copyright 2014-2023 © Dimitris Zlatanidis. Slackware® is a Registered
Trademark of Patrick Volkerding. Linux is a Registered Trademark of
Linus Torvalds.
