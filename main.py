"""

Author: Nelson Gonzabato

Script mode for the python package urlfix.

Free Open Source Software, Made with Love.

It is and will always be about the community.

"""


if __name__=="__main__":
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
                            help="Output file to write to. Optional, only necessary if not replacing inplace")
    # Verbosity, this is useful if you need to control whether messages are printed on
    # the console
    arg_parser.add_argument("-v", "--verbose",type=bool,required=True,
                            help="Boolean to control verbosity. Defaults to True.",
                            default=True)
    # Inplace or not?
    arg_parser.add_argument("-i", "--inplace",type=bool,
                            required=True, default=False)

    # Parse arguments
    arguments = arg_parser.parse_args()

    # Choose one of URLFix or DirURLFix

    script_mode = dirurlfix.DirURLFix(input_dir=arguments.input_file)
    if arguments.mode == "f":
        script_mode = urlfix.URLFix(input_file=arguments.input_file, output_file=arguments.output_file)


    script_mode.replace_urls(verbose=arguments.verbose, inplace=arguments.inplace)