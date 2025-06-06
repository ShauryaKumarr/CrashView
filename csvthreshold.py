import pandas as pd
import numpy as np
import os

def sample_large_csv(input_file, output_file, target_rows=1000000):
    """
    Sample a large CSV file to create a smaller version with approximately target_rows.
    Uses pandas to efficiently read and sample the data.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to save the sampled CSV file
        target_rows (int): Target number of rows in the output file
    """
    try:
        # Convert path to use forward slashes
        input_file = input_file.replace('\\', '/')
        output_file = output_file.replace('\\', '/')
        
        # Verify input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
            
        print(f"Processing file: {input_file}")
        
        # Get total number of rows in the input file
        print("Counting total rows...")
        total_rows = sum(1 for _ in open(input_file)) - 1  # Subtract 1 for header
        
        # Calculate sampling rate to get approximately target_rows
        sampling_rate = target_rows / total_rows
        
        print(f"Total rows in input file: {total_rows:,}")
        print(f"Target rows in output file: {target_rows:,}")
        print(f"Sampling rate: {sampling_rate:.4%}")
        
        # Read and sample the data in chunks to manage memory
        chunk_size = 100000  # Adjust based on available memory
        chunks = pd.read_csv(input_file, chunksize=chunk_size)
        
        # Process chunks and write sampled data
        first_chunk = True
        for chunk in chunks:
            # Sample the chunk
            sampled_chunk = chunk.sample(frac=sampling_rate, random_state=42)
            
            # Write to file
            if first_chunk:
                sampled_chunk.to_csv(output_file, index=False)
                first_chunk = False
            else:
                sampled_chunk.to_csv(output_file, mode='a', header=False, index=False)
            
            print(f"Processed chunk of {len(chunk):,} rows")
        
        # Verify final row count
        final_rows = sum(1 for _ in open(output_file)) - 1
        print(f"\nFinal output file has {final_rows:,} rows")
        print(f"Output saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    # Input file path
    input_file = "2025-06-02-16-48-10_hesai_pandar.csv"
    
    # Create output filename in the same directory as input
    input_dir = os.path.dirname(input_file)
    input_filename = os.path.basename(input_file)
    output_filename = f"sampled_{input_filename}"
    output_file = os.path.join(input_dir, output_filename)
    
    # Run the sampling
    sample_large_csv(input_file, output_file)
