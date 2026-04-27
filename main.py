from pipelines.run_pipeline import run_pipeline
if __name__ == "__main__":
    print("--- Starter Datapipeline ---") 
vær_df, forurensning_df, merged_df = run_pipeline()
  