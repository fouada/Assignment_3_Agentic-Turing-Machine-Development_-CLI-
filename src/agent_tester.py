#!/usr/bin/env python3
"""
Agent Tester - Test Claude Agent Skills via CLI
===============================================

This module provides a command-line interface for testing individual
Claude agent skills without running the full translation pipeline.

Features:
- Test any skill in the skills/ directory
- View list of available skills
- Direct skill invocation with custom input
- Token usage and cost tracking

Usage:
    python3 test_agent.py <agent-name> <input-text>
    python3 test_agent.py --list

Examples:
    python3 test_agent.py english-to-french-translator "Hello world"
    python3 test_agent.py french-to-hebrew-translator "Bonjour le monde"
    python3 test_agent.py --list

Author: Agentic Turing Machine Team
License: MIT
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Optional
import anthropic

# Import custom modules
from logger import get_logger
from errors import SkillNotFoundError, APIError, ValidationError

# Initialize logger
logger = get_logger(__name__)


def load_skill(agent_name: str) -> Dict[str, str]:
    """
    Load an agent skill definition from the skills directory.

    Reads the SKILL.md file for the specified agent and returns
    its content along with metadata.

    Args:
        agent_name: Name of the agent (e.g., "english-to-french-translator")

    Returns:
        Dict[str, str]: Dictionary containing:
            - name: Agent name
            - content: Full content of SKILL.md file

    Raises:
        SkillNotFoundError: If the skill file doesn't exist
        IOError: If file reading fails

    Example:
        >>> skill = load_skill("english-to-french-translator")
        >>> print(skill['name'])
        english-to-french-translator
        >>> print(len(skill['content']))
        1250
    """
    logger.debug(f"Loading skill: {agent_name}")

    project_root = Path(__file__).parent.parent
    skill_path = project_root / "skills" / agent_name / "SKILL.md"

    if not skill_path.exists():
        logger.error(f"Skill not found: {skill_path}")
        raise SkillNotFoundError(
            f"Agent skill '{agent_name}' not found",
            details={"skill_path": str(skill_path)}
        )

    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        logger.info(f"Loaded skill '{agent_name}': {len(content)} characters")

        return {
            "name": agent_name,
            "content": content
        }

    except IOError as e:
        logger.error(f"Failed to read skill file: {e}")
        raise SkillNotFoundError(
            f"Cannot read skill file for '{agent_name}'",
            details={"error": str(e), "path": str(skill_path)}
        ) from e


def list_agents() -> List[str]:
    """
    List all available agent skills in the skills directory.

    Scans the skills/ directory and identifies all valid agent skills
    (directories containing a SKILL.md file).

    Returns:
        List[str]: Sorted list of agent names

    Example:
        >>> agents = list_agents()
        >>> print(agents)
        ['english-to-french-translator', 'french-to-hebrew-translator', ...]
    """
    logger.debug("Scanning for available agent skills")

    project_root = Path(__file__).parent.parent
    skills_dir = project_root / "skills"

    if not skills_dir.exists():
        logger.warning(f"Skills directory not found: {skills_dir}")
        print("❌ No skills directory found")
        return []

    agents = []
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            agents.append(skill_dir.name)
            logger.debug(f"Found agent: {skill_dir.name}")

    agents_sorted = sorted(agents)
    logger.info(f"Found {len(agents_sorted)} agent skills")
    return agents_sorted


def invoke_agent(
    client: anthropic.Anthropic,
    skill: Dict[str, str],
    input_text: str
) -> str:
    """
    Invoke a Claude agent skill with given input text.

    Constructs a prompt from the skill definition and input text,
    then sends it to the Claude API for processing.

    Args:
        client: Initialized Anthropic API client
        skill: Dictionary containing skill name and content
        input_text: Text to be processed by the agent

    Returns:
        str: Agent's response (processed output)

    Raises:
        APIError: If the API call fails
        ValidationError: If input validation fails

    Example:
        >>> client = anthropic.Anthropic(api_key="...")
        >>> skill = load_skill("english-to-french-translator")
        >>> output = invoke_agent(client, skill, "Hello world")
        >>> print(output)
        Bonjour le monde
    """
    logger.info(f"Invoking agent: {skill['name']}")
    logger.debug(f"Input text length: {len(input_text)} characters")

    if not input_text.strip():
        logger.error("Empty input text provided")
        raise ValidationError("Input text cannot be empty")

    # Construct prompt
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
        logger.debug("Sending request to Claude API")
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

        logger.info(
            f"Agent completed successfully: "
            f"{response.usage.input_tokens} input tokens, "
            f"{response.usage.output_tokens} output tokens"
        )

        print(f"✅ Output length: {len(output)} characters")
        print(f"💰 Tokens used: input={response.usage.input_tokens}, "
              f"output={response.usage.output_tokens}")

        return output

    except anthropic.APIError as e:
        logger.error(f"Claude API error: {e}", exc_info=True)
        print(f"❌ API Error: {e}")
        raise APIError(
            f"Claude API call failed for agent '{skill['name']}'",
            details={"error": str(e), "agent": skill['name']}
        ) from e

    except Exception as e:
        logger.error(f"Unexpected error during agent invocation: {e}", exc_info=True)
        print(f"❌ Error: {e}")
        raise APIError(
            f"Agent invocation failed unexpectedly",
            details={"error": str(e), "agent": skill['name']}
        ) from e


def main() -> None:
    """
    Main entry point for the agent tester CLI.

    Handles command-line arguments, validates inputs, and coordinates
    the testing of agent skills.

    Command-line Usage:
        python3 test_agent.py <agent-name> <input-text>
        python3 test_agent.py --list

    Exits:
        0: Success
        1: Error occurred

    Side Effects:
        - Prints output to console
        - Makes API calls to Claude
        - Logs operations to file
    """
    logger.info("Agent tester started")

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
        logger.info("Listing available agents")
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
        logger.info(f"Listed {len(agents)} agents")
        sys.exit(0)

    agent_name = sys.argv[1]
    logger.info(f"Testing agent: {agent_name}")

    if len(sys.argv) < 3:
        logger.error(f"No input text provided for agent '{agent_name}'")
        print(f"❌ Error: No input text provided for agent '{agent_name}'")
        print(f"Usage: python3 test_agent.py {agent_name} \"your input text\"")
        sys.exit(1)

    input_text = " ".join(sys.argv[2:])
    logger.debug(f"Input text: {input_text[:50]}...")

    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY environment variable not set")
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Run test
    logger.info("Starting agent test")
    print("\n" + "=" * 70)
    print("TESTING AGENT VIA CLI")
    print("=" * 70)

    try:
        # Load agent
        print(f"\n📂 Loading agent: {agent_name}")
        skill = load_skill(agent_name)
        print(f"✓ Skill loaded: {len(skill['content'])} characters")

        # Initialize client
        logger.debug("Initializing Anthropic API client")
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
        logger.info("Agent test completed successfully")

    except SkillNotFoundError as e:
        logger.error(f"Skill not found: {e}")
        print(f"\n❌ {e}")
        print(f"\nAvailable agents:")
        for agent in list_agents():
            print(f"  • {agent}")
        sys.exit(1)

    except (APIError, ValidationError) as e:
        logger.error(f"Agent test failed: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error during agent test: {e}", exc_info=True)
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

