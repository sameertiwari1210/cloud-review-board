import sys
from datetime import datetime
from agents.architect import run_architect_agent

# Why: Simple helper to generate current timestamp for tracking execution stages.
# Inputs: None
# Outputs: Current timestamp formatted as string.
def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Why: Entry point of the Cloud Security Review Board CLI. 
#      Reads user query, runs the Architect agent, and prints the result.
# Inputs: None
# Outputs: None
def main():
    print("==================================================")
    print("   Cloud Security Review Board (CSRB) — Phase 1   ")
    print("==================================================")
    
    # Check if a query was provided as a command-line argument
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter your cloud architecture question: ").strip()
        
    if not query:
        print("ERROR: Query cannot be empty. Exiting.")
        sys.exit(1)
        
    start_time = get_timestamp()
    print(f"\n[{start_time}] [System] Starting cloud review workflow...")
    
    # Run the Architect Agent
    architecture_design = run_architect_agent(query)
    
    # Output the result
    print("\n" + "=" * 50)
    print("               ARCHITECT DESIGN OUTPUT            ")
    print("=" * 50)
    print(architecture_design)
    print("=" * 50)
    
    end_time = get_timestamp()
    print(f"[{end_time}] [System] Workflow completed successfully.")

if __name__ == "__main__":
    main()
