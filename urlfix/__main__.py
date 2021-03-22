"""

Author: Nelson Gonzabato

Script mode for the python package urlfix.

Free Open Source Software, Made with Love.

It is and will always be about the community.

"""

def main():
    from argparse import ArgumentParser
    from urlfix import urlfix, dirurlfix
    arg_parser = ArgumentParser()

    # Add relevant options
    # Mode one of file or directory str
    arg_parser.add_argument("-m", "--mode", type=str,
                            help="Mode to use. One of f for file or d for directory",
                            required=True, default="d")
    # Input file
    arg_parser.add_argument("-in","--input-file", type=str,
                            help="Input file for which link updates are required.",
                            required=True)
    # Output file [optional] because we may need to do inplace replacement
    arg_parser.add_argument("-o", "--output-file", type=str,
                            help="Output file to write to. Optional, only necessary if not replacing inplace",
                            default=None)
    # Verbosity, this is useful if you need to control whether messages are printed on
    # the console
    arg_parser.add_argument("-v", "--verbose",type=str,required=True,
                            help="String to control verbosity. Defaults to True.",
                            default="True", choices=["False", "false", "0","True", "true", "1"])
    # Inplace or not?
    arg_parser.add_argument("-i", "--inplace",type=str,
                            required=True, default="False",
                            help="Should links be replaced inplace? This should be safe but to be sure"
                                 ", test with an output file first.",
                            choices=["False", "false", "0","True", "true", "1"])

    # Parse arguments
    arguments = arg_parser.parse_args()

    # Choose one of URLFix or DirURLFix

    script_mode = dirurlfix.DirURLFix(input_dir=arguments.input_file)
    if arguments.mode == "f":
        script_mode = urlfix.URLFix(input_file=arguments.input_file, output_file=arguments.output_file)

    # For some reason boolean doesn't work out of the box with argparse
    # One could use action="store_true" or False but I find that less convenient

    # You could use distutils.util str2bool but this assumes you will have tolower() which is not always true
    # At least it isn't true here.

    def make_bool(obj_to_convert):
        if isinstance(obj_to_convert, bool):
            return obj_to_convert
        else:
            choices_to_use = {"True": True,
                              "true": True,
                              1: True,
                              "1": True,
                              "False": False,
                              0: False,
                              "0": False}
            return choices_to_use[obj_to_convert]




    script_mode.replace_urls(verbose=make_bool(arguments.verbose), inplace=make_bool(arguments.inplace))

if __name__=="__main__":
    main()
