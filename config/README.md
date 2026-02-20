# Project Profiles

`active_project.txt` selects which profile is used on this device.

- Default file: `config/active_project.txt`
- Override for one run: set `UQ_PROJECT_ID=<profile_id>`

Profiles live in `config/projects/`.

Current profiles:
- `original.json`
- `altruism.json`

The system prompt text is externalized in `config/prompts/zeek_system_prompt.txt` and referenced from each profile.

## Conversation Turn Injections

Use `conversation.turn_injections` to add turn-dependent system instructions without editing Python code.

- `mode: "temporary"`: active only on a specific turn (`at_turn`) or optional range (`start_turn`, `end_turn`).
- `mode: "stable"`: becomes active at `activate_at_turn` (or `at_turn`) and persists for later turns.

Example:

```json
{
  "conversation": {
    "turn_injections": [
      {
        "id": "intro",
        "mode": "temporary",
        "at_turn": 1,
        "text": "Introduce yourself briefly."
      },
      {
        "id": "memory_block",
        "mode": "stable",
        "activate_at_turn": 4,
        "text": "Topic X has been introduced; answer follow-up questions when relevant."
      }
    ]
  }
}
```
