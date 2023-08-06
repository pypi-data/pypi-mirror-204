import os
import json

def pdm_build_update_files(context, files):
    context.ensure_build_dir()
    project_root = os.path.dirname(__file__)
    target = os.path.join(project_root, 'src', 'bloqade', "juliapkg.json")
    with open(os.path.join(project_root, 'juliapkg.json')) as f:
        d = json.load(f)
        for _, info in d['packages'].items():
            del info['path']
            del info['dev']
    
    with open(target, 'w') as target:
        json.dump(d, target)

def pdm_build_finalize(context, artifact):
    project_root = os.path.dirname(__file__)
    target = os.path.join(project_root, 'src', 'bloqade', "juliapkg.json")
    os.remove(target)
