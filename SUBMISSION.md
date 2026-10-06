# Submission checklist

**This is the original Week 1 guide. For the current three-tool assignment use
[SUBMISSION_WEEK2.md](SUBMISSION_WEEK2.md).**

## 1. Verify the real agent

Follow README setup, run the tests, then use `python agent.py` with Ollama running.
The model is not bundled with this repo. Do not present mocked test output as a live LLM demo.

## 2. Public GitHub repository

Sign in to [GitHub](https://github.com/new), create a **public** repository named
`one-tool-calculator-agent`. For this existing local project, leave automatic README,
license, and gitignore creation unchecked.

In the project terminal, review files before staging:

```powershell
git status
git add agent.py README.md LEARN_TANGLISH.md SUBMISSION.md .gitignore tests/test_agent.py
git commit -m "Build one-tool calculator agent with Ollama"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/one-tool-calculator-agent.git
git push -u origin main
```

Replace YOUR_USERNAME. If Git requests your author name/email, configure your own
details. If a remote already exists, inspect `git remote -v` before changing it.
Complete GitHub's sign-in when prompted. Open the public URL in a signed-out window
to verify it is accessible. This document does not mean the repo has been published.

## 3. Screen recording: 60–120 seconds

Use your screen recorder (Windows Snipping Tool supports recording on supported
Windows versions). Record the actual terminal and code; save the video and play it
back to check legibility and audio. A script alone is not the required recording.

Suggested Tanglish narration:

1. Show `TOOLS` in `agent.py`: "Idhu en calculator agent. Ollama model use panren.
   Model-kku ore Python function expose pannirukken: calculate."
2. Run `python agent.py`, type `Hi`: "Greeting-ku tool thevai illa, direct reply."
3. Type `What is 18 percent of 1250?`: "Ippo model calculate tool-ai choose pannudhu.
   Execute panna munnadi raw tool call print aagudhu."
4. Point at result 225 and final answer: "Python result-ai model observe panni
   plain language-la response kudukkudhu."
5. Type `Add 100 to that result`: "Previous conversation context use aagudhu."
6. Type `What is 10 divided by zero?`: "Error-um observation-a model-kku pogum."
7. End: "Idhu understand, decide, act, observe, respond loop."

If the model does not call the tool correctly, debug and record a successful real run.
Upload the video to your chosen sharing service and verify viewers can access it.

## 4. LinkedIn post draft

Use this after you have run and verified the project. Replace the placeholders.
Type @SkillAudit.ai in LinkedIn and select the matching page from the mention menu
so it becomes an actual tag.

> I built a single-purpose AI calculator agent using Python and Ollama!
>
> The model decides when to call one Python tool, observes its result, and replies
> in plain language. The CLI prints the raw tool call before execution, making the
> agent loop easy to inspect.
>
> What I learned: tool schemas, function calling, conversation history, safe input
> handling, and the difference between model decisions and tool execution.
>
> GitHub: [PASTE PUBLIC REPO URL]
> Demo: [PASTE RECORDING URL]
>
> Built for @SkillAudit.ai
> #Python #AIAgents #Ollama #BuildInPublic

Final deliverables: public repository URL, accessible screen recording, LinkedIn
post URL with the correct tag. Publishing/posting still needs your account access.
