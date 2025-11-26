#!/usr/bin/env python3
"""
Quick Agent Tester - Test any agent skill via CLI

Usage:
    python3 test_agent.py <agent-name> <input-text>
    
Examples:
    python3 test_agent.py english-to-french-translator "Hello world"
    python3 test_agent.py french-to-hebrew-translator "Bonjour le monde"
"""

import sys
import os
from pathlib import Path
import anthropic


def load_skill(agent_name: str) -> dict:
    """Load an agent skill from skills directory."""
    project_root = Path(__file__).parent.parent
    skill_path = project_root / "skills" / agent_name / "SKILL.md"
    
    if not skill_path.exists():
        raise FileNotFoundError(f"Agent skill not found: {skill_path}")
    
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {
        "name": agent_name,
        "content": content
    }


def list_agents():
    """List all available agents."""
    project_root = Path(__file__).parent.parent
    skills_dir = project_root / "skills"
    if not skills_dir.exists():
        print("❌ No skills directory found")
        return []
    
    agents = []
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            agents.append(skill_dir.name)
    
    return sorted(agents)


def invoke_agent(client: anthropic.Anthropic, skill: dict, input_text: str) -> str:
    """Invoke an agent with input text."""
    prompt = f"""{skill['content']}

---

Please process the following input according to the skill instructions above.
Return ONLY the result, with no explanations or additional text.

Input:
{input_text}"""

    print(f"\n📤 Invoking agent: {skill['name']}")
    print(f"📝 Input length: {len(input_text)} characters")
    print("⏳ Processing...")
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            temperature=0,  # Deterministic
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        output = response.content[0].text.strip()
        
        print(f"✅ Output length: {len(output)} characters")
        print(f"💰 Tokens used: input={response.usage.input_tokens}, output={response.usage.output_tokens}")
        
        return output
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


def main():
    # Check arguments
    if len(sys.argv) < 2:
        print("=" * 70)
        print("Agent Tester - Test Claude Agent Skills via CLI")
        print("=" * 70)
        print()
        print("Usage:")
        print("  python3 test_agent.py <agent-name> <input-text>")
        print("  python3 test_agent.py --list")
        print()
        print("Examples:")
        print('  python3 test_agent.py english-to-french-translator "Hello world"')
        print('  python3 test_agent.py french-to-hebrew-translator "Bonjour"')
        print()
        
        # Show available agents
        print("Available agents:")
        agents = list_agents()
        if agents:
            for agent in agents:
                print(f"  • {agent}")
        else:
            print("  (No agents found in skills/ directory)")
        print()
        sys.exit(1)
    
    # List agents
    if sys.argv[1] == "--list":
        print("\n📋 Available Agents:")
        print("=" * 70)
        agents = list_agents()
        project_root = Path(__file__).parent.parent
        for i, agent in enumerate(agents, 1):
            skill_path = project_root / "skills" / agent / "SKILL.md"
            size = skill_path.stat().st_size / 1024  # KB
            print(f"{i}. {agent:<40} ({size:.1f} KB)")
        print("=" * 70)
        print(f"\nTotal: {len(agents)} agents")
        sys.exit(0)
    
    agent_name = sys.argv[1]
    
    if len(sys.argv) < 3:
        print(f"❌ Error: No input text provided for agent '{agent_name}'")
        print(f"Usage: python3 test_agent.py {agent_name} \"your input text\"")
        sys.exit(1)
    
    input_text = " ".join(sys.argv[2:])
    
    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Run test
    print("\n" + "=" * 70)
    print("TESTING AGENT VIA CLI")
    print("=" * 70)
    
    try:
        # Load agent
        print(f"\n📂 Loading agent: {agent_name}")
        skill = load_skill(agent_name)
        print(f"✓ Skill loaded: {len(skill['content'])} characters")
        
        # Initialize client
        client = anthropic.Anthropic(api_key=api_key)
        
        # Invoke agent
        output = invoke_agent(client, skill, input_text)
        
        # Display result
        print("\n" + "=" * 70)
        print("RESULT")
        print("=" * 70)
        print()
        print(output)
        print()
        print("=" * 70)
        print("✅ Test complete!")
        
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print(f"\nAvailable agents:")
        for agent in list_agents():
            print(f"  • {agent}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

