#!/usr/bin/env python


def opts():
    import optparse
    parser = optparse.OptionParser()
    parser.add_option("--file1", dest="file1", default="", help="REQUIRED: .root file over which to run")
    parser.add_option("--feds1", dest="feds1", default="", help="REQUIRED: FEDs to use in file1, e.g. 714,722 or e.g. HBHE")
    parser.add_option("--file2", dest="file2", default="", help=".root file to compare with file1")
    parser.add_option("--feds2", dest="feds2", default="", help="FEDs to use in file2, e.g. 931")
    parser.add_option("--patterns", dest="patterns", default=False, action="store_true", help="interpret QIE data as FE patterns")
    parser.add_option("--nevents", dest="nevents", default="", metavar="N", help="stop after N events")
    parser.add_option("--dump", dest="dump", default=0, metavar="D", help="dump level (0-6; higher is more verbose)")
    parser.add_option("--no-color", dest="noColor", default=False, action="store_true", help="disable color in stdout")

    options, args = parser.parse_args()

    if not all([options.file1, options.feds1]):
        parser.print_help()
        exit()
    return options


def integer(value="", tag=""):
    if value:
        try:
            return int(value)
        except ValueError:
            printer.error("%s '%s' cannot be converted to an int." % (tag, value))
            exit()
    else:
        return None


def fedList(s=""):
    if s in ["HCAL", "hcal"]:
        return range(700, 732)
    if s in ["HBHE", "hbhe"]:
        return range(700, 718)
    if s in ["HF", "hf"]:
        return range(718, 724)
    if s in ["HO", "ho"]:
        return range(724, 732)
    if not s:
        return []
    out = [int(x) for x in s.split(",")]
    return out


def checkModules():
    import types
    names = []
    for key, value in globals().iteritems():
        if isinstance(value, types.ModuleType):
            names.append(key)
    if names != ["__builtins__"]:
        print names
        print "Please put imports after this block, to prevent PyROOT from stealing '--help'."


options = opts()
checkModules()

import analyze
import printer
if options.noColor:
    printer.__color = False

label = "latest"
analyze.oneRun(file1=options.file1,
               feds1=fedList(options.feds1),
               file2=options.file2,
               feds2=fedList(options.feds2),
               nEvents=integer(options.nevents, "nevents"),
               patternMode=options.patterns,
               label=label,
               dump=integer(options.dump, "dump"),
               )

if not options.patterns:
    if options.file2:
        analyze.printHisto(label)
    import graphs
    graphs.makeSummaryPdf(labels=[label])
