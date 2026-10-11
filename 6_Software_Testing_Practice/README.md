# Software Testing Practice: Lab 4 (Vibe Coding)

Assigned repository: [SETAPESU26/59_rock_paper_scissor](https://github.com/SETAPESU26/59_rock_paper_scissor)

| File | Contents |
|---|---|
| [before.mp4](59_rock_paper_scissor/before.mp4) | Gameplay before changes, showing the bug (winning hands awarded to the CPU) |
| [after.mp4](59_rock_paper_scissor/after.mp4) | Gameplay after changes, showing the fix and the new features |
| [59_rock_paper_scissor/](59_rock_paper_scissor) | Updated code |
| [chat_history.docx](59_rock_paper_scissor/chat_history.docx) | Exported chat history with the LLM |

Chat link: https://claude.ai/share/016772a5-65c3-4861-b35e-590293ab3337
## Changes

1. Fixed the inverted outcome bug in `determine_winner` (Rock beats Scissors, Scissors beats Paper, Paper beats Rock).
2. Added a "first to 5 wins" match with a victory banner; press R to restart.
3. Added an adaptive CPU (`game/adaptive_cpu.py`) that tracks the player's last 8 moves and biases toward the counter-move, while keeping some randomness.
4. Added drawn Rock, Paper and Scissors icons (`game/icons.py`) with a "Rock... Paper... Scissors..." countdown, a shaking fist animation and a pop-in reveal.