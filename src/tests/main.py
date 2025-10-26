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

os.makedirs("output", exist_ok=True)

def main():
    # Compile the workflow
    app = get_agent()

    # Draw and save graph as PNG
    try:
        app.get_graph().draw_mermaid_png(
            curve_style=CurveStyle.LINEAR,
            node_colors=NodeStyles(
                first="#FF6B6B",  # Vibrant red for start
                last="#4ECDC4",  # Teal for end
                default="#95E1D3",  # Mint green for regular nodes
            ),
            wrap_label_n_words=9,
            output_file_path='graph.png',
            background_color="white",
            padding=20,
        )
    except Exception as e:
        print(f"Could not generate graph image: {e}")
    
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