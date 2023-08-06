import os
import json

def pdm_build_update_files(context, files):
    context.ensure_build_dir()
    with open(os.path.join(os.path.dirname(__file__), 'juliapkg.json')) as f:
        d = json.load(f)
        for _, info in d['packages'].items():
            del info['path']
            del info['dev']
    
    with open(os.path.join(os.path.dirname(__file__), 'src', 'bloqade', "juliapkg.json"), 'w') as target:
        json.dump(d, target)
