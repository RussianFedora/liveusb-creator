#!/usr/bin/env python

from pprint import pprint
from liveusb.releases import *
all_releases = get_fedora_releases(RFREMIX_RELEASES) + get_fedora_releases(FEDORA_RELEASES)
pprint(all_releases)
