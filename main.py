import os
import time
import sys
import re
from dotenv import load_dotenv
from google import genai
from google.api_core import exceptions # Important for catching 429s
from agent_logic import ResearchAgent
import state_manager

# Load environment variables
load_dotenv()

def initialize_ai():
    """Checks multiple keys and models to find a working combination."""
    raw_keys = [os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_API_KEY_2")]
    api_keys = [k for k in raw_keys if k]
    
    if not api_keys:
        print("❌ CRITICAL: No API keys found in .env")
        return None, None

    priority_models = ["gemini-2.5-flash", "gemini-2.0-flash"]
    
    for i, key in enumerate(api_keys):
        try:
            client = genai.Client(api_key=key)
            for model_name in priority_models:
                try:
                    time.sleep(1) 
                    client.models.generate_content(model=model_name, contents="ping")
                    print(f"🚀 AI Online! Key_{i} verified with {model_name}")
                    return key, model_name
                except Exception:
                    continue
        except Exception as e:
            print(f"❌ Key_{i} Connection Error: {e}")
            continue
            
    return None, None

def main():
    try:
        print("=== STARTING DURABLE AGENT SYSTEM ===")
        print("(Press Ctrl+C to stop safely)\n")
        
        active_key, active_model = initialize_ai()
        if not active_key:
            print("❌ Failure: No working AI configuration found.")
            return

        agent = ResearchAgent(api_key=active_key, model_id=active_model)
        goal = "The impact of AI automation on Zimbabwe's mining sector by 2030"
        
        current_state = state_manager.load_state()
        
        # --- PHASE 1: PLANNING ---
        if "plan" not in current_state:
            print("\n--- Phase 1: Planning ---")
            plan = agent.plan_task(goal)
            state_manager.save_state("plan", {"data": plan})
        else:
            plan = current_state["plan"]["data"]
            print("✅ Restored Plan from memory.")

        # --- PHASE 2: RESEARCHING ---
        if "research" not in current_state:
            print("\n--- Phase 2: Researching ---")
            research_results = agent.execute_research(plan)
            state_manager.save_state("research", {"data": research_results})
        else:
            research_results = current_state["research"]["data"]
            print("✅ Restored Research from memory.")

        # --- PHASE 3: FINALIZING ---
        if "report" not in current_state:
            print("\n--- Phase 3: Finalizing ---")
            report = agent.finalize_report(research_results)
            state_manager.save_state("report", {"data": report})
        else:
            report = current_state["report"]["data"]
            print("✅ Restored Final Report from memory.")

        print("\n" + "="*40)
        print("FINAL EXECUTIVE SUMMARY")
        print("="*40)
        print(report)

    except exceptions.ResourceExhausted as e:
        # Extract wait time from the error message
        wait_time = 60 
        match = re.search(r"retry in (\d+\.?\d*)s", str(e))
        if match:
            wait_time = int(float(match.group(1))) + 1
        
        print(f"\n\n[!] Quota Exceeded (429): Free Tier limit reached.")
        print(f"[*] Resuming in {wait_time} seconds...")
        
        for i in range(wait_time, 0, -1):
            sys.stdout.write(f"\r    ⏳ Time remaining: {i}s  ")
            sys.stdout.flush()
            time.sleep(1)
        
        print("\n\n[*] Ready! Run 'python main.py' to resume.")

    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user. Progress saved.")
        sys.exit(0)
    except Exception as fatal_error:
        print(f"\n❌ A fatal error occurred: {fatal_error}")

if __name__ == "__main__":
    main()