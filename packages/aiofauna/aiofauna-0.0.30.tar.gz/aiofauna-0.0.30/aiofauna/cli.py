#! /usr/bin/env python
import click
import os
import json
import base64
import re
import sys
from aiohttp_devtools.cli import cli

@cli.command()
def scaffold():
    """Scaffold a new AioFauna project"""