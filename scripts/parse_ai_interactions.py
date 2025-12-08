import json
import datetime
import argparse
from typing import Dict, List, Any

def convert_timestamp_to_readable(timestamp_ms: int) -> str:
    """Convert millisecond timestamp to human-readable format."""
    # Convert milliseconds to seconds
    timestamp_s = timestamp_ms / 1000
    # Convert to datetime
    dt = datetime.datetime.fromtimestamp(timestamp_s)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def parse_ai_interactions(data_str: str) -> List[Dict[str, Any]]:
    """Parse AI interaction data and extract individual interactions."""
    try:
        # Parse the JSON data
        data = json.loads(data_str)
        
        interactions = []
        
        # Extract chat options
        chat_options = data.get("chat_options", {})
        
        # Extract responses
        responses = data.get("responses", [])
        
        for i, response in enumerate(responses):
            interaction = {
                "interaction_id": i + 1,
                "message_id": response.get("id", ""),
                "user_message": response.get("message", {}).get("message", ""),
                "user_message_id": response.get("message", {}).get("id", ""),
                "user_timestamp_ms": response.get("message", {}).get("timestamp", 0),
                "user_timestamp_readable": convert_timestamp_to_readable(
                    response.get("message", {}).get("timestamp", 0)
                ),
                "response_timestamp_ms": response.get("timestamp", 0),
                "response_timestamp_readable": convert_timestamp_to_readable(
                    response.get("timestamp", 0)
                ),
                "relevance": response.get("relevance", 0),
                "error": response.get("error", False),
                "model": "",
                "completion_tokens": 0,
                "prompt_tokens": 0,
                "total_tokens": 0,
                "finish_reason": "",
                "assistant_content": ""
            }
            
            # Parse the nested JSON in the "json" field
            try:
                json_data = json.loads(response.get("json", "{}"))
                choices = json_data.get("choices", [])
                if choices:
                    choice = choices[0]
                    interaction["finish_reason"] = choice.get("finish_reason", "")
                    interaction["assistant_content"] = choice.get("message", {}).get("content", "")
                
                # Extract usage information
                usage = json_data.get("usage", {})
                interaction["completion_tokens"] = usage.get("completion_tokens", 0)
                interaction["prompt_tokens"] = usage.get("prompt_tokens", 0)
                interaction["total_tokens"] = usage.get("total_tokens", 0)
                
                # Extract model information
                interaction["model"] = json_data.get("model", "")
                
            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse JSON for interaction {i+1}: {e}")
            
            interactions.append(interaction)
        
        return interactions
    
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
        return []

def print_interactions_summary(interactions: List[Dict[str, Any]]):
    """Print a summary of all interactions."""
    print(f"\n=== AI INTERACTION SUMMARY ===")
    print(f"Total interactions: {len(interactions)}")
    
    if not interactions:
        return
    
    # Calculate statistics
    total_tokens = sum(interaction["total_tokens"] for interaction in interactions)
    total_completion_tokens = sum(interaction["completion_tokens"] for interaction in interactions)
    total_prompt_tokens = sum(interaction["prompt_tokens"] for interaction in interactions)
    
    print(f"Total tokens used: {total_tokens}")
    print(f"Total completion tokens: {total_completion_tokens}")
    print(f"Total prompt tokens: {total_prompt_tokens}")
    
    # Show time range
    first_timestamp = interactions[0]["user_timestamp_readable"]
    last_timestamp = interactions[-1]["response_timestamp_readable"]
    print(f"Time range: {first_timestamp} to {last_timestamp}")
    
    print("\n=== INDIVIDUAL INTERACTIONS ===")
    
    for i, interaction in enumerate(interactions):
        print(f"\n--- Interaction {interaction['interaction_id']} ---")
        print(f"User Message: {interaction['user_message']}")
        print(f"User Time: {interaction['user_timestamp_readable']}")
        print(f"Response Time: {interaction['response_timestamp_readable']}")
        print(f"Model: {interaction['model']}")
        print(f"Tokens: {interaction['prompt_tokens']} prompt + {interaction['completion_tokens']} completion = {interaction['total_tokens']} total")
        print(f"Finish Reason: {interaction['finish_reason']}")
        print(f"Relevance: {interaction['relevance']}")
        print(f"Error: {interaction['error']}")
        
        # Show first 200 characters of assistant response
        content = interaction['assistant_content']
        if len(content) > 200:
            content = content[:200] + "..."
        print(f"Assistant Response: {content}")

def save_interactions_to_csv(interactions: List[Dict[str, Any]], output_file: str):
    """Save interactions to a CSV file."""
    import pandas as pd
    
    df = pd.DataFrame(interactions)
    df.to_csv(output_file, index=False)
    print(f"\nInteractions saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Parse AI interaction data and convert timestamps to human-readable format.')
    parser.add_argument('input_file', help='Path to the input JSON file containing AI interaction data.')
    parser.add_argument('--output', '-o', help='Output CSV file path (optional).')
    parser.add_argument('--summary-only', action='store_true', help='Only print summary, not individual interactions.')
    
    args = parser.parse_args()
    
    # Read the input file
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            data_str = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Parse the interactions
    interactions = parse_ai_interactions(data_str)
    
    if not interactions:
        print("No interactions found in the data.")
        return
    
    # Print summary
    print_interactions_summary(interactions)
    
    # Print individual interactions if not summary-only
    if not args.summary_only:
        print_interactions_summary(interactions)
    
    # Save to CSV if output file specified
    if args.output:
        save_interactions_to_csv(interactions, args.output)

if __name__ == '__main__':
    main() 