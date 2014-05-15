#!/usr/bin/env python
# encoding: utf-8
'''
This file is part of Jailmenu program, which is a menu jail 
to provide secure access to a system.

Jailmenu program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


@author:     Harri Savolainen
@copyright:  Harri Savolainen 2014. All rights reserved.
@license:    GPLv2
@contact:    harri.savolainen@gmail.com
@deffield    updated: Updated
'''

import sys
import os

from optparse import OptionParser

__all__ = []
__version__ = 0.1
__date__ = "2014-05-15"
__updated__ = "2014-05-15"

DEBUG = 1
TESTRUN = 0
PROFILE = 0


def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__

    program_version_string = "%%prog %s (%s)" % (program_version,
                                                 program_build_date)

    program_longdesc = ("Jailmenu program, which is a menu jail to provides "
                        "secure access to a system. Licensed under GNU Public "
                        "License 2.0 "
                        "(http://www.gnu.org/licenses/gpl-2.0.html)")

    program_license = "Copyright Harri Savolainen 2014, GPLv2"

    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string,
                              epilog=program_longdesc,
                              description=program_license)

        parser.add_option('-c', '--config',
                          dest='infile',
                          help="set configuration file [default: %default]",
                          metavar='FILE')

        # set defaults
        parser.set_defaults(infile="~/jailmenu.conf")

        # process options
        (opts, args) = parser.parse_args(argv)

        if opts.verbose > 0:
            print("verbosity level = %d" % opts.verbose)
        if opts.infile:
            print("infile = %s" % opts.infile)
        if opts.outfile:
            print("outfile = %s" % opts.outfile)

        # MAIN BODY #

    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'jailmenu_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open('profile_stats.txt', 'wb')
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
