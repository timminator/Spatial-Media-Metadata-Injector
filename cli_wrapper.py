# Nuitka compile commands
# nuitka-project: --standalone
# nuitka-project: --output-filename=Spatial Media Metadata Injector CLI

from spatialmedia.__main__ import main
import sys

if len(sys.argv) == 1:
    sys.argv.append("--help")

main()