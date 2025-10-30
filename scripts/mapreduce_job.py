"""
MapReduce job for log processing and aggregation
"""
import sys
from collections import defaultdict


def mapper():
    """
    Mapper function: Process input lines and emit key-value pairs
    Reads from stdin, writes to stdout
    """
    for line in sys.stdin:
        line = line.strip()
        
        if not line:
            continue
        
        try:
            # Parse log line (example: timestamp, user_id, action, value)
            parts = line.split('\t')
            
            if len(parts) < 4:
                continue
            
            timestamp, user_id, action, value = parts[:4]
            
            # Emit: user_id as key, action and value as value
            print(f"{user_id}\t{action},{value}")
            
        except Exception as e:
            # Log errors to stderr (won't interfere with output)
            sys.stderr.write(f"Mapper error: {str(e)}\n")


def reducer():
    """
    Reducer function: Aggregate values for each key
    Reads from stdin, writes to stdout
    """
    current_key = None
    action_counts = defaultdict(int)
    value_sums = defaultdict(float)
    
    for line in sys.stdin:
        line = line.strip()
        
        if not line:
            continue
        
        try:
            # Parse mapper output
            key, value = line.split('\t', 1)
            action, val = value.split(',')
            
            # If new key, output previous aggregation
            if current_key and current_key != key:
                output_aggregation(current_key, action_counts, value_sums)
                action_counts.clear()
                value_sums.clear()
            
            # Aggregate current key
            current_key = key
            action_counts[action] += 1
            value_sums[action] += float(val)
            
        except Exception as e:
            sys.stderr.write(f"Reducer error: {str(e)}\n")
    
    # Output final aggregation
    if current_key:
        output_aggregation(current_key, action_counts, value_sums)


def output_aggregation(key, counts, sums):
    """Output aggregated results"""
    for action in counts:
        count = counts[action]
        total = sums[action]
        avg = total / count if count > 0 else 0
        
        print(f"{key}\t{action}\t{count}\t{total:.2f}\t{avg:.2f}")


if __name__ == "__main__":
    # Determine if running as mapper or reducer
    if len(sys.argv) > 1 and sys.argv[1] == "reduce":
        reducer()
    else:
        mapper()
