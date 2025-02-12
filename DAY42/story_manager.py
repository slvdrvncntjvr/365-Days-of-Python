from typing import Dict, Any

def load_story(filename: str) -> Dict[str, Any]:
    return {
        "start": {
            "text": "You find yourself in a dark forest. Do you go left or right?",
            "choices": {
                "left": "You encounter a friendly elf.",
                "right": "You stumble upon a sleeping dragon."
            }
        }
    }

def get_story_segment(story: Dict[str, Any], choice: str) -> str:
    return story.get("start", {}).get("choices", {}).get(choice, "The path is unclear.")