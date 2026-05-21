from pipelines.run_pipeline import run_pipeline
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("Starting main...")
    
    try:
        merged_df = run_pipeline()
        
        if merged_df is None:
            print("\n" + "="*60)
            print(" FAILED - Pipeline returned no data")
            print("="*60)
            logger.error("Pipeline failed - check logs above")
            sys.exit(1)
        
        if merged_df.empty:
            print("\n" + "="*60)
            print(" FAILED - Pipeline returned empty dataframe")
            print("="*60)
            logger.error("Pipeline returned empty data")
            sys.exit(1)
        
        # Success
        print("\n" + "="*60)
        print(" SUCCESS - Pipeline completed!")
        print("="*60)
        print(f"\nMerged data shape: {merged_df.shape}")
        print(f"Columns: {len(merged_df.columns)}")
        print(f"\nData saved to database!")
        print("="*60)
            
    except Exception as error:
        print("\n" + "="*60)
        print(" ERROR - Pipeline crashed!")
        print("="*60)
        print(f"Error: {error}")
        logger.error(f"Pipeline failed: {error}", exc_info=True)
        sys.exit(1)
        