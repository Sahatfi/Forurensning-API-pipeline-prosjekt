import sys
sys.path.append('..')
from pipelines.run_pipeline import run_pipeline

a, b, c, d  = run_pipeline()
print(d)