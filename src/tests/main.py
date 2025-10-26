from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
import os
try:
    from ..agent import get_agent
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from agent.agent import get_agent


def main():
    # Compile the workflow
    app = get_agent()
    
    user_input = input("Enter your stock analysis query: ").strip()
    
    # Run analysis
    print(f"\n🔍 Processing your query: '{user_input}'...")
    print("=" * 80)
    
    result = app.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }
    )

    print("\n--- Analysis Complete ---\n")
    for m in result['messages']:
        print(m.pretty_print())
    
    print("\n" + "=" * 80)
    print("✅ Analysis complete!")

if __name__ == "__main__":
    main()