


__version__  = 0.1
__PKG_ID__   = "3r"
__PKG_NAME__ = "run"
__PKG_DESC__ = "services switches"


import argparse

import game# main module


def main():
    ap = argparse.ArgumentParser(
        prog        = __PKG_NAME__,
        description = __PKG_DESC__
    )

    ap.add_argument(
        '-v',
        "--version",
        action  = "version",
        version = 'sz%(prog)s v' + str(__version__))

    ap.add_argument(
        '-d',
        "--debug",
        action  = "store_true",
        default = False,
        help    = "debug mode")

    opts, keys = ap.parse_known_args()


    if opts.debug:
        game.app.run(debug=opts.debug, host='0.0.0.0')
        return

    game.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    game.app.run()


if __name__ == '__main__':
        main()
