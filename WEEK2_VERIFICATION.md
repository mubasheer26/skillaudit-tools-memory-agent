# Week 2 verification

## Rechecked on 2026-10-06

- All 18 automated tests passed after the time-reporting prompt update.
- `python demo.py` completed against the real local `llama3.2` model.
- Calculator: 250 * 3 = 750; after an intervening thanks turn, 750 + 50 = 800.
- Notes: saved and listed Practice Python daily in a temporary notebook.
- Time: tool returned 2026-10-06T22:20:04+05:30; final answer correctly reported
  06 October 2026 22:20 IST, though it reformatted despite the exact-copy instruction.
- Division by zero: error observation and readable final error, no crash.
- Four deliberately injected invalid calls returned errors without crashing.
- Remaining model limitation: Thanks! unnecessarily called notes/list and replied
  that there were no notes. This is an actual observed routing error.
- The earlier live run restated the time incorrectly; an explicit time-copy
  instruction was added and the above full demo rerun successfully.
- Actual transcript is saved locally at recordings/live-demo.txt (git ignored).
  It is a text transcript, not a screen recording.

The older report below is retained as historical context.

Checked locally on 2026-09-29 with Python 3.14 and Ollama `llama3.2`.

## Automated checks

`python -m unittest discover -s tests -v`: **18 tests passed** (7 original + 11 new).
New checks cover all three tool registrations, dispatch, malformed calls, wrong
arguments, JSON string arguments, persisted notes, duplicate notes, corrupt files,
file permission errors, clock offsets, multi-turn history, tool-free replies,
observation retention after request failure, and loop bounds.

Model replies in these tests are mocked. The memory test proves that earlier
observations reach the next model request; it does not prove every model will use them.

## Real Ollama observations

| Request | Observed behavior |
| --- | --- |
| What is 250 * 3? | calculate called; 750 returned and answered |
| Thanks! (first run) | Incorrectly repeated previous calculation |
| Add 50 to that result | Recalled 750 across intervening turn; calculate returned 800 |
| Save a note: Practice Python daily. | notes/save called and confirmed |
| List my saved notes. | notes/list returned the saved note |
| Current time (initial API design) | Model sent string instead of integer offset; validation returned an error without crashing |
| Current time (final zero-argument design) | current_time called with {}; India and UTC returned; India time answered correctly |
| Hi! (final prompt) | Unnecessary current_time call before greeting response |
| Thanks! (final prompt) | Unnecessary notes/list call |

The save/read test used a temporary notebook so it did not add test notes to the
user's real notebook. Clock output was observed at execution time; it is not a
fixed expected value.

## Remaining limitation

The installed small model still overuses tools for greetings/thanks despite
instructions. Core tool execution, error observations, and session context work,
but conversational routing is not fully reliable. No keyword filter pretends to be
the model's decision. A stronger tool-capable model can be selected with `--model`,
but alternatives have not been verified here.

Notes use a fixed, git-ignored JSON file. This educational app supports one CLI
writer at a time, keeps exact duplicate notes only once, and retains conversation
memory only during the current process. It does not implement a database,
concurrent writes, long-history summarization, or automatic daylight-saving lookup.
