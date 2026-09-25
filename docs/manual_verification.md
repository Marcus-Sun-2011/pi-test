# Manual Verification Guide (Manual Testing)

This document provides a guide for manually verifying core agent features via the CLI interface. Use this when you have time to perform interactive testing.

## Preparation
Ensure your local environment is set up:
1. Start LM Studio or your preferred local inference server.
2. Ensure `src/agent/engine.py` and other modules are updated.
3. Run the setup commands (if any) as per instructions.

## Test Cases

### 1. Multi-Tool Chain Verification
**Goal:** Verify that the agent can recognize, call, and process multiple tools in a single turn or sequential turns.
- **Input Prompt:** "What is the current time, and what day of the week is it today?"
- **Expected Behavior:**
    1. The model should identify the need for `time_tool` (or similar).
    2. If multiple actions are needed (e.g., checking date from a tool output), it should execute them sequentially or in a loop.
    3. **Logs to Check:** Look for multiple `SUCCESS | Tool: ...` entries in `logs/agent_studio.log`.
- **Success Criteria:** The agent provides the correct time and day without failing during multi-step logic.

### 2. Error Feedback Loop (Self-Correction)
**Goal:** Verify that the agent can handle tool errors gracefully and attempt to correct its actions when a tool fails.
- **Input Prompt:** "Read the contents of a system file or non-existent file, e.g., 'missing_file.txt'."
- **Expected Behavior:**
    1. The `file_tool` will fail with a `ToolExecutionError`.
    2. The engine will catch this and provide an error message back to the model (e.g., "File not found").
    3. The model should recognize it was a failure, explain why, or ask for clarification instead of just crashing.
- **Logs to Check:** Look for `FAILURE | Tool: ...` in the logs followed by a revised response from the model.
- **Success Criteria:** The agent acknowledges the error and provides a coherent explanation or corrective step rather than outputting a raw Python stack trace to the user.

### 3. Complex Reasoning & Logic Integration
**Goal:** Test if the agent can integrate tool outputs into complex reasoning calculations.
- **Input Prompt:** "What is the current time, and then calculate how many seconds are in that day."
- **Expected Behavior:**
    1. Agent calls `time_tool`.
    2. Agent receives a result (e.g., "2023-10-27 10:00:00").
    3. Agent performs a math calculation based on the string/data received.
- **Success Criteria:** The agent successfully completes the multi-step logic involving tool output as an intermediate variable for calculation.

## Troubleshooting
If any test fails:
- Check `logs/agent_studio.log` for the full trace of the interaction.
- Verify that the LLM model is correctly following the system prompt's instructions regarding tools.
- Ensure all required dependencies are installed and LM Studio is connected properly.
