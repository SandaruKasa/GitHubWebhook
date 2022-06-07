#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

from flask import Flask, request


def decode(b: bytes) -> str:
    try:
        return b.decode()
    except:
        return repr(b)


app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    ref = request.json.get("ref")
    expected = ["refs/heads/master", "refs/heads/main"]
    if ref in expected:
        process = subprocess.run(
            args.command,
            shell=True,
            input="",
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            cwd=args.dir,
        )
        return (
            "Process {!r} finished with return code {}:\n{}".format(
                process.args,
                process.returncode,
                decode(process.stdout),
            ),
            200 if process.returncode == 0 else 418,
        )
    else:
        return f"Ref {repr(ref)} is not one of {expected}. Not doing anything.", 202


def get_parser(default_port, default_address="0.0.0.0"):
    parser = argparse.ArgumentParser(
        description="GitHub webhook handler. "
        "Automatically runs a specified command "
        "when receives a notification about a push to main/master."
    )
    parser.add_argument(
        "--bind",
        "-b",
        help=f"address to bind to (default: {default_address})",
        default=default_address,
    )
    parser.add_argument(
        "--port",
        "-p",
        default=default_port,
        type=int,
        help=f"port to listen on (default: {default_port})",
    )
    parser.add_argument(
        "--dir",
        "-d",
        default=os.getcwd(),
        type=Path,
        help="directory to execute command in",
    )
    parser.add_argument(
        "command",
        help=f"command to execute",
    )
    return parser


if __name__ == "__main__":
    import argparse
    import logging

    import waitress
    from paste.translogger import TransLogger

    logging.basicConfig(level="INFO")

    args = get_parser(default_port=11444).parse_args()
    waitress.serve(TransLogger(app), host=args.bind, port=args.port)
