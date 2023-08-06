import os
import json

def pdm_build_initialize(context):
    context.ensure_build_dir()
    print('aaaa')
    with open(os.path.join(os.path.dirname(__file__), 'juliapkg.json')) as f:
        d = json.load(f)
        for _, info in d['packages'].items():
            del info['path']
            del info['dev']
    
    with open(os.path.join(context.build_dir, "juliapkg.json"), 'w') as target:
        json.dump(d, target)
