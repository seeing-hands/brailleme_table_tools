# LibLouis table format reverser
# This script is designed to regress a LibLouis table to an older version, specifically so that it can run on the Braille Me
# Note: This is an experimental script. There are many tables it won't work on, because functionality is only added as needed
# There is no support for this software.
import argparse
import sys
import subprocess
import os
import datetime

format_warning = f"""
# This file was automatically generated by brailleme_convert.py
# For more information, see github.com/seeing-hands/brailleme_table_tools
# This is an attempt to regress a Braille table file so that it is compatible with the version of Liblouis present on the BrailleMe display
# This file generated on {datetime.datetime.now().isoformat()}
""".strip()

def convert_table(input_fn):
    rlines = []
    with open(input_fn, encoding="utf-8") as f:
        for line in f:
            command = line.split("#")[0].strip().split(" ")
            # Handle opcodes here
            if command[0] == "include":
                # Drag any include files into this file so it is only a single one at the end
                rlines.extend(convert_table(command[1]))
            else:
                # unhandled command, emit line directly
                rlines.append(line)
    return rlines

def main(argv):
    args = argparse.ArgumentParser(
        description="Convert a modern LibLouis table to a BrailleMe-compatible version")
    args.add_argument("-i", "--input",
        help="The path to a table to be converted", action="store", required=True)
    args.add_argument("-o", "--output",
        help="The path to the file where the converted table will be written", action="store", required=True)
    args.add_argument("-sv", "--skip-verify",
        help="Skip the verification of the created table", action="store_true")
    args.add_argument("--lou-checktable-path",
        help="The path to the lou_checktable binary used for verification.",
        default="liblouis/lou_checktable")
    config = args.parse_args()
    output_file_lines = convert_table(config.input)
    with open(config.output, "w", encoding="utf-8") as f:
        f.write(format_warning)
        for l in output_file_lines:
            f.write(l)

    if config.skip_verify:
        sys.exit(1)
    verify_code = subprocess.call([config.lou_checktable_path, config.output])
    if verify_code != 0:
        print("Table has errors. Deleting generated version.")
        os.remove(config.output)
        sys.exit(-1)


if __name__ == "__main__":
    main(sys.argv)