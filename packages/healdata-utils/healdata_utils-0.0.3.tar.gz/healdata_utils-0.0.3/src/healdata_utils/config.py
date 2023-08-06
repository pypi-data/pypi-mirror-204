from pathlib import Path 
import yaml

ROOT_DIR = Path(__file__).parents[2]

with open(ROOT_DIR/'studies.yaml','r') as f:
    studies = yaml.safe_load(f)


