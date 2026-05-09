from pipelines.run_pipeline import run_pipeline
import logging

# ✅ Configure logging (THIS IS WHAT YOU'RE MISSING!)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info("Starting main...")
    
    # Run pipeline
    vær_df, forurensning_df, merged_df = run_pipeline()
    
    # Check if successful
    if merged_df is not None:
        print("\n" + "="*60)
        print("✅ SUCCESS - Pipeline completed!")
        print("="*60)
        print(f"\nMerged data shape: {merged_df.shape}")
        print(f"\nFirst few columns: {list(merged_df.columns[:5])}")
        print(f"\nData preview:")
        print(merged_df.head())
    else:
        print("\n" + "="*60)
        print("❌ FAILED - Pipeline returned no data")
        print("="*60)
        print("Check logs above for details")