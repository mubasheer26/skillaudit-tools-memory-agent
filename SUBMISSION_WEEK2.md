# Week 2 submission: three tools and memory

This replaces the old one-tool submission instructions in SUBMISSION.md.

## Run and understand

Open Ollama, then run in this folder:

```powershell
python -m unittest discover -s tests -v
python multi_agent.py
```

Use `ollama pull llama3.2` if the model is missing. No paid API key is required.
Read WEEK2_START_HERE.md first, then WEEK2_LINE_BY_LINE.md alongside the code.
multi_agent.py is one model with multiple tools, not several independent agents.

## Screen recording

Open Windows Snipping Tool, choose Record and New, select the terminal/code area,
and start recording. Run `python demo.py` to show seven real-model prompts plus
deliberately injected invalid-call examples. The demo uses a temporary notebook
and saves actual output to recordings/live-demo.txt. A text transcript is NOT a video.

For an interactive demo, run `python multi_agent.py` and type:

```text
What is 250 * 3?
Thanks!
Add 50 to that result.
Save a note: Practice Python daily.
List my saved notes.
What is the current date and time in India?
What is 10 divided by zero?
/exit
```

Expected calculator results: 750 then 800. Current time changes with the clock.
Use `python demo.py --errors-only` to show unknown-tool and invalid-argument
handling. Say explicitly that those bad calls are injected tests.

Tanglish narration:

1. "Idhu Python and Ollama use panna three-tool AI agent."
2. "Calculator, note saver, date-time helper nu moonu tools irukku."
3. "TOOLS-la name, description, parameters irukku. Model-kku menu card madhiri."
4. "250 into 3-ku model calculate choose pannudhu. Python 750 return pannudhu."
5. "Thanks sonna apram add 50 to that result ketkuren. Earlier 750 messages-la irukkuradhaal 800 calculate panna mudiyum."
6. "Note JSON file-la store aagum. App close pannalum note irukkum. Chat memory mattum session mudinja clear aagum."
7. "Wrong tool name or input vandha error return pannuvom; app crash aagadhu."
8. "Tool calls/results terminal-la paakalam. Idhu execution log; private thinking illa."

Stop recording, save the MP4, and play it back to verify readable text. Upload
it to your chosen service and check viewer access. Small models can make extra
tool calls; describe observed behaviour honestly.

## Public GitHub repository

Create a public repo named `skillaudit-tools-memory-agent` at https://github.com/new.
Leave automatic README creation unchecked for this existing project.

```powershell
git add .gitignore agent.py multi_agent.py demo.py tests README.md LEARN_TANGLISH.md WEEK2_START_HERE.md WEEK2_LINE_BY_LINE.md WEEK2_VERIFICATION.md SUBMISSION_WEEK2.md START_HERE_TANGLISH.md
git commit -m "Build three-tool agent with memory and Tanglish guides"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/skillaudit-tools-memory-agent.git
git push -u origin main
```

Replace YOUR_USERNAME. If origin exists, inspect it before changing it. Configure
your own Git author name/email if requested; never paste credentials in chat.
Notes, recordings, and environment secrets are excluded by .gitignore. Verify
that the public repository opens while signed out.

## LinkedIn draft

Replace links before posting. Type @SkillAudit.ai and select the matching company
page from LinkedIn's menu so it becomes an actual tag.

I extended my Python AI agent with three tools and conversation memory!

Built with Python and Ollama, it calculates, saves/reads local notes, and fetches
the current date and time. The model receives clear schemas and chooses a tool.

My favourite part: after a calculation and another conversation turn, I can say
"Add 50 to that result" because previous messages and tool results stay in context.

I added validation for unknown tools and invalid arguments, plus terminal logs
for every tool call and result. Small-model tool selection is still imperfect,
which has been a useful lesson in testing real agent behaviour.

GitHub: [ADD PUBLIC REPOSITORY LINK]
Demo: [ADD SCREEN RECORDING LINK]

Built as part of my learning with @SkillAudit.ai
#Python #AIAgents #Ollama #BuildInPublic #LearningInPublic

## Submit these three items

- Public GitHub URL
- Accessible screen-recording URL or required video upload
- LinkedIn post URL with the actual SkillAudit.ai tag

This guide is preparation; it does not mean publication or recording has happened.
