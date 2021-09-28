#!/usr/bin/env python3

import json

with open("cache.json", "r") as f:
    settings = json.load(f)
    
print(json.dumps(settings, indent=4, sort_keys=True))
