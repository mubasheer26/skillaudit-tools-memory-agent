# Mudhal-la idhai padinga

Assignment main file `multi_agent.py`. Existing three-tool implementation-ai
preserve panni verify pannirukkom. Pudhusa repeatable live demo and updated
submission guide add pannirukkom.

## Agent epdi work aagum?

Question -> model tool choose pannum -> Python execute pannum -> tool result
memory-la add aagum -> model final answer sollum.

Restaurant example: customer = neenga; waiter = model; kitchen = Python tools;
menu card = schema; order notebook = messages memory.

- `calculate`: 250 * 3 maths-ku; answer 750.
- `notes`: save action JSON file-la ezhudhum; list action notes padikkum.
- `current_time`: computer clock-la irundhu India/UTC time edukkum.

Currency converter optional example dhaan. Indha moonu tools requirement-ai meet
pannum; euro conversion indha app support pannaadhu.

## Mukkiyamaana lines

`messages = [{"role": "system", "content": SYSTEM}]`

List create panrom. System message model epdi behave pannanum-nu sollum.

`messages.append({"role": "user", "content": question})`

Question list-la add aagum. Existing messages delete aagadhu.

`message = request_chat(messages, model)`

Full conversation model-kku pogum. Two turns munnadi result-um model paakum.
Memory-na inga magic illa; pazhaya messages thirumba anuppuradhu.

`calls = message.get("tool_calls") or []`

Model tool ketta andha list eduppom. Illaina empty list.

`name, result = dispatch(call)`

Tool name/input sariyaa-nu check panni actual Python function run pannuvom.

`messages.append({"role": "tool", "tool_name": name, "content": json.dumps(result)})`

Tool answer-aiyum memory-la add panrom. Next model request idhaiyum paakum.

`except ...` and `return {"error": str(exc)}`

Thappu input vandha app stop aagama readable error return pannum.

## Line by line padikka order

1. WEEK2_START_HERE.md: Python basics, functions, JSON, agent loop.
2. WEEK2_LINE_BY_LINE.md: every nonblank line of multi_agent.py + calculator.
3. multi_agent.py: explanation pakkathula actual code compare pannunga.
4. SUBMISSION_WEEK2.md: recording, GitHub, LinkedIn draft.

## Run pannunga

```powershell
python multi_agent.py
```

Ollama running-a irukkanum. `What is 250 * 3?`, `Thanks!`, `Add 50 to that result.`
sequential-a try pannunga. Expected 800. Model wrong/extra tool choose pannalaam;
actual logs paarthu verify pannunga.

## demo.py helper purinjukalam

Idhu main agent replacement illa. `PROMPTS` recording questions store pannum.
`Tee.write` output-ai terminal-kum text file-kum anuppum. `error_examples` wrong
inputs deliberately dispatch-kku anuppum. `TemporaryDirectory` demo notes-ai
separate-a vaikkum. `patch.object` notes path mattum maathum; model response fake
pannaadhu. `app.run_turn` real Ollama-kku request anuppum. Error vandha demo stop
aagi reason print aagum. `--errors-only` use pannina Ollama thevai illa.

Transcript = text. Screen recording = actual video. Submission-ku video venum.
