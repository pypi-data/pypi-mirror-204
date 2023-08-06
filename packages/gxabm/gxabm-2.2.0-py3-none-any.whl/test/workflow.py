import sys
import json

workflow_path = '/Users/suderman/Workspaces/JHU/Experiments/assets/workflows/De_novo_transcriptome_reconstruction_with_RNA-Seq.ga'

with open(workflow_path) as f:
    workflow = json.load(f)

print(workflow['workflow_id'])
print(workflow['runs'])

