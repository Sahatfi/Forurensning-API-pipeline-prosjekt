from pipelines.run_pipeline import run_pipeline
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("Starting main...")
    
    try:
        # Run pipeline
        merged_df = run_pipeline()
        
        # Check if successful
        if merged_df is not None and not merged_df.empty:
            print("\n" + "="*60)
            print("✅ SUCCESS - Pipeline completed!")
            print("="*60)
            print(f"\nMerged data shape: {merged_df.shape}")
            print(f"Columns: {len(merged_df.columns)}")
            print(f"\nData saved to database!")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("❌ FAILED - Pipeline returned no data")
            print("="*60)
            
    except Exception as error:  # ← error, ikke e
        print("\n" + "="*60)
        print("❌ ERROR - Pipeline crashed!")
        print("="*60)
        print(f"Error: {error}")
        logger.error(f"Pipeline failed: {error}", exc_info=True)