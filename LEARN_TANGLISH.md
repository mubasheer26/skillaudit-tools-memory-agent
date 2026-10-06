# AI agent kathukalam — step by step

## 1. Namma enna build panrom?

Namma oru calculator assistant build panrom. Normal calculator-ku `250 * 3`
nu type pannanum. Namma agent-kitta `250 rupees item 3 vaangina evlo?`
nu natural language-la kekkalam. LLM question-ai purinjukittu calculation
tool-ku correct input anuppanum.

LLM = language-ai understand panni response generate panra model.
Ollama = andha model-ai unga computer-la run panna help panra software.
Python = model request-ai tool execution-oda connect panra namma program.

## 2. First setup

PowerShell open pannunga. `python --version` run pannunga. Python 3.10 illa
adhukku mela version venum. Indha project-ku extra pip packages thevai illa.

[Ollama download](https://ollama.com/download) page-la Windows installer
download panni install pannunga. App open pannunga. Pudhu PowerShell open panni:

```powershell
ollama pull llama3.2
```

Idhu model files-ai download pannum; internet-um disk space-um venum.
Download time connection-ai poruthadhu. First response slow-a irukkalam,
yenna model memory-la load aaganum. API key thevai illa.

## 3. Project run pannunga

```powershell
cd "C:\Users\hp\Documents\ChatGPT\Skillaudit Ai project"
python agent.py
```

`You:` prompt vandha `Hi` type pannunga. Model usually direct-a greet pannum;
calculation thevai illa, so tool call vara vendam.

Aduthu `What is 18 percent of 1250?` type pannunga.
Expected numerical result: **225**. Actual model wording/expression maaralam.

## 4. Agent loop-ai oru example-la purinjukalam

User: `250 rupees item 3 vaanguren. 10 percent discount. Total?`

1. **Understand/think:** model user request-ai process pannum.
2. **Decide:** calculation thevai-nu model tool call generate pannum.
3. **Act:** Python `calculate` function-ai execute pannum.
4. **Observe:** `675` result model-kku tool message-a pogum.
5. **Respond:** model `Discount apram total 675 rupees` nu sollalam.

Namma hidden thinking-ai print pannala. Tool request/result dhaan visible.
Example tool call (illustration; live model output different-a irukkalam):

```json
{"function": {"name": "calculate", "arguments": {"expression": "250 * 3 * 0.9"}}}
```

`name` = endha function? `arguments` = andha function-ku enna input?
JSON = programs structured data exchange panna use panra format.

## 5. `calculate` function padikkalam

`agent.py`-la first function paarunga:

```python
def calculate(expression: str) -> dict:
```

`expression` text input; example `"2 + 3"`. Return value dictionary;
example `{"expression": "2 + 3", "result": 5}`.

`ast.parse` expression-ai tree-a maathum. `2 + 3 * 4`-la multiplication
first nadakkanum-nu tree structure sollum. `visit` helper andha tree-ai
read panni allowed operations mattum calculate pannum.

Why `eval` illa? User/model kudutha text-ai unrestricted Python code-a
execute panna koodadhu. Namma numbers and arithmetic operators mattum allow panrom.
`10 / 0` na crash aagama error dictionary return pannum.
`**` power; `%` remainder. Percentage calculate panna `/ 100` use pannanum.

## 6. Tool schema — model-kku kudukkura instruction card

`TOOLS` list-la ore entry irukku: `calculate`.

- `name`: function name.
- `description`: eppo, edhukku use pannanum.
- `parameters`: expected input format.
- `required`: kandippa kudukkanum-na argument.

Schema-la function body illa. Model name/arguments mattum generate pannum.
Actual execution namma app responsibility. App-la helpers irundhaalum model-kku
expose pannirukkura tool **one** dhaan.

## 7. `chat` — model-kitta pesura bridge

`http://localhost:11434/api/chat` unga computer-la run aagura Ollama endpoint.
`urllib.request` Python-oda built-in HTTP client; separate SDK install thevai illa.

Request-la `model`, `messages`, `tools` anuppurom. `stream=False` na full
response vandha apram process panrom. `temperature=0` variation-ai reduce pannum;
perfect answer guarantee illa.

## 8. `run_turn` — project-oda main concept

Indha function-ai slow-a top-to-bottom padikkunga:

1. `request_chat(messages, model)` model response-ai vaangum.
2. Assistant message history-la save aagum.
3. `tool_calls` illaina text answer return aagum.
4. Tool call irundha **execute panna munnadi** raw JSON print aagum.
5. Function name and arguments validate pannuvom.
6. `calculate(**arguments)` actual arithmetic execute pannum.
7. Result `role: tool` message-a history-la add aagum.
8. Loop marubadi model-ai call pannum. Ippo model result-ai paathu reply pannum.

`**arguments` na dictionary values-ai named inputs-a pass panradhu.
Example `calculate(**{"expression": "2+3"})` and `calculate(expression="2+3")`
rendum same.

Model thodarndhu tool call pannitte irundha five rounds apram stop pannuvom.
Idhu infinite loop avoid pannum.

## 9. `messages` memory epdi work aagudhu?

`system` = assistant rules; `user` = unga question;
`assistant` = model reply/tool request; `tool` = actual function result.

Previous messages next request-layum pogum. So `Add 100 to that result`
nu ketta previous result context model-kku irukkum. App close panna history
save aagadhu. Long chat-na `/reset` use pannunga.

## 10. Test pannunga

```powershell
python -m unittest discover -s tests -v
```

Tests-la real model-ku badhila fixed fake responses use panrom. Idhu app logic-ai
repeatable-a verify pannum. Real model tool choose panradha check panna Ollama-oda
live chat run pannanum. Rendum different checks.

Practice questions:

| Input | Enna observe pannanum? |
| --- | --- |
| Hi | Direct response; tool thevai illa |
| What is 12 * 8? | calculate request; result 96 |
| Add 4 to that | History use panni result 100 |
| What is 10 / 0? | Error observation; helpful reply |
| Calculate my discount | Details missing; clarification kekkanum |
| Tell me today's weather | Calculator scope-ku redirect pannanum |

Model wrong-a behave pannina raw call paarunga: expression wrong-aa,
tool call varalaya, illa correct result-ai reply-la thappa sonnadhaa?
Indha three places-ai separate-a debug pannunga.

## 11. Neenga explain panna theriyanum

Indha questions-ku unga words-la answer try pannunga:

1. LLM calculation execute pannudha? Illa Python function execute pannudha?
2. Tool result vandha apram yen model-ai marubadi call panrom?
3. Greeting-ku tool call yen thevai illa?
4. Tool schema and actual function enna difference?
5. Test pass aana live model always correct-nu sollalama?

Answers: Python execute pannum; model result-ai plain language-la explain panna
second call; greeting-ku arithmetic illa; schema describes/function executes;
illa, live model behavior-ai separately verify pannanum.

Next: `SUBMISSION.md` steps follow panni repo, real recording, LinkedIn post ready pannunga.
