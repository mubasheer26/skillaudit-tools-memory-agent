# Week 2 — zero-la irundhu multi-tool agent kathukalam

Indha guide-ai ore sitting-la mudikkanum-nu pressure illa. Oru lesson padichu,
command run panni, output purinja apram next lesson ponga. Copy-paste work aaguradhu
first step; adhu yen work aagudhu-nu explain panna theriyuradhu learning.

## Lesson 1: Program-na enna?

Program = computer follow panra instructions. Python = andha instructions ezhudha
use panra language. File = instructions save panra place. Terminal = command type
panni program run panra window.

```python
price = 250
quantity = 3
total = price * quantity
print(total)
```

- `price`: namma choose panna variable name. Variable-na value-ku oru label.
- `=`: right side value-ai left side name-kku assign pannum. Idhu equality check illa.
- `250`: whole number; Python-la `int`.
- `quantity = 3`: innoru number-ku name kudukkurom.
- `*`: multiplication. `price * quantity` means `250 * 3`.
- `total`: calculation result store panra variable.
- `print(total)`: terminal-la result show pannum. Output `750`.
- Parentheses `(...)`: function-ku input pass panna use panrom.

**Neenga try pannunga:** quantity-ai `4`-a maathina output enna? Answer: `1000`.

## Lesson 2: Function-na enna? Yen use pannanum?

```python
def add(a, b):
    return a + b

answer = add(10, 20)
print(answer)
```

`def` = oru function define panrom. Function = name kudutha reusable instructions.
`add` = namma function name. `a, b` = input receive panra parameter names.
`:` apram indented lines function-oda body. **Four spaces** use pannunga.
`return` result-ai function-ai call pannina place-kku thiruppi kudukkum.
`add(10, 20)` actual call. Ippo `a=10`, `b=20`, return `30`.

`print` and `return` same illa: print screen-la kaattum; return value-ai other code
use panna kudukkum. Agent-ku result-ai model-kku anuppanum, so tools return values.

**Yen function?** Calculation code-ai pala places-la rewrite panna vendam.
Namma `calculate`, `notes`, `current_time` ellam functions.

## Lesson 3: List, dictionary, JSON

```python
names = ["Asha", "Ravi"]
message = {"role": "user", "content": "Hi"}
messages = [message]
messages.append({"role": "assistant", "content": "Hello"})
```

`"..."` = text/string. `[]` = ordered list; shopping list madhiri.
`{}` = dictionary; key/value pairs. `role` key-ku `user` value irukku.
Dictionary-la `:` key-ai value-oda connect pannum; `,` entries-ai separate pannum.
`messages.append(...)` list end-la pudhu item add pannum.

JSON = data exchange panra text format. Python dictionary memory-la object;
`json.dumps(dictionary)` adhai JSON text-a maathum. `json.loads(text)` reverse.
JSON itself AI illa. Request and result share panna common format mattum.

## Lesson 4: Agent-oda three tools

| User request | Tool | Why? |
| --- | --- | --- |
| `250 * 3 evlo?` | `calculate` | Arithmetic execute panna |
| `Save a note: Practice Python daily` | `notes` with save | Text disk-la store panna |
| `List my saved notes` | `notes` with list | Saved text read panna |
| `India-la current time enna?` | `current_time` | Computer clock-la actual time eduka |
| `Hi` / `Thanks` | No tool needed | External action/calculation thevai illa |

Save/list rendu actions, aana `notes` ore exposed function. Total **3 tools**.
Currency converter indha version-la illa. Date/time India and UTC rendu time-um
return pannum; arguments thevai illa. Worldwide city timezone lookup illa.

**Analogy:** restaurant-la customer request-ai waiter understand pannuvaar.
Kitchen actual food prepare pannum. Inga model request select pannum;
Python function actual work pannum. Model execute panniduchu-nu sonna mattum
podhaadhu; `[tool result]` log-la actual result irukkanum.

## Lesson 5: First AI illaama tool-ai test pannunga

Project folder-la PowerShell open panni:

```powershell
python -c "from agent import calculate; print(calculate('250 * 3'))"
python -c "from multi_agent import current_time; print(current_time())"
python -c "from multi_agent import notes; print(notes('save', 'Practice Python daily'))"
python -c "from multi_agent import notes; print(notes('list'))"
```

`python` Python interpreter-ai start pannum. `-c` next text-ai Python code-a run
pannum. `from ... import ...` file-la irukkura function-ai use panna edukkum.
`';'` same command-la two Python statements separate pannum.
Idhu direct tool test; **LLM tool choose pannala**. Tools correct-a work aagudha-nu
first isolate panni check panrom.

Expected: calculation `750`, actual current timestamp, note saved status,
then saved notes list. Note file `data/notes.json`-la create aagum.

## Lesson 6: Tool schema-na enna?

Schema = model-kku kudukkura tool instruction card. `TOOLS` list-la each function-ku
`name`, `description`, `parameters` irukku.

```json
{
  "name": "notes",
  "description": "Save a note or list notes",
  "parameters": {
    "type": "object",
    "properties": {"action": {"type": "string", "enum": ["save", "list"]}},
    "required": ["action"],
    "additionalProperties": false
  }
}
```

Idhu simplified illustration; actual schema-la `text`-um irukku.
`name`: execute panna function name. `description`: eppo use pannanum.
`parameters`: arguments structure. `object`: key/value object venum.
`properties`: allowed input names. `enum`: indha values mattum allowed.
`required`: action miss aaga koodadhu. `additionalProperties: false`:
`filename`, `password` madhiri extra inputs accept panna koodadhu.

**Yen schema mattum podhaadhu?** Model wrong arguments generate pannalam.
Adhan `dispatch` Python-side validation-um panrom. Schema is guidance;
validation is actual enforcement. Rendum useful.

## Lesson 7: Routing-na enna?

```python
FUNCTIONS = {"calculate": agent.calculate, "notes": notes, "current_time": current_time}
```

Dictionary left side model sollura name; right side actual Python function.
Function name pakkathula `()` illa—ippo execute pannala, reference save panrom.

```python
result = FUNCTIONS[name](**arguments)
```

If `name="notes"`, `arguments={"action":"save", "text":"Study"}`:
idhu `notes(action="save", text="Study")` madhiri work aagum.
`**` inga dictionary unpacking; calculation expression-la `**` power. Context different.

Namma code user question-la keywords search panni tool choose pannala.
Model native `tool_calls` response-la function name choose pannum.

## Lesson 8: Conversation memory — indha assignment-oda core

```python
messages = [{"role": "system", "content": SYSTEM}]
messages.append({"role": "user", "content": question})
```

First line **chat loop-ku outside** irukku. Once initialize panrom.
Loop inside initialize pannina old conversation ovvoru turn-layum erase aagidum!

Every request-la same running list model-kku send panrom:

```python
payload = {"model": model, "messages": messages, "tools": TOOLS}
```

Roles:

| Role | Yaar / enna? |
| --- | --- |
| system | Assistant-ku rules |
| user | Unga question |
| assistant | Model response or tool request |
| tool | Python function actual result |

Example conversation:

1. User: `250 * 3?` -> tool result `750`.
2. User: `Thanks` -> normal reply.
3. User: `Add 50 to that result` -> earlier `750` still history-la irukku; expected `800`.

**Important:** history anuppuradhu namma responsibility. Andha context-ai correct-a
use panradhu model ability. List irundhaalum model mistake panna mudiyum.
App exit panna chat memory pogum. `/reset` system message mattum keep pannum.
Saved notes separate disk file; `/reset` avatrai delete pannaadhu.
Chat grow aaga model context limit reach aagalam; indha learning app summary/DB use pannala.

## Lesson 9: Complete loop dry-run

Request: `Calculate 250 * 3 and save the result as a note`.

```text
user question -> model
model tool call -> calculate(expression="250 * 3")
Python result -> {"result": 750, ...}
result appended to messages -> model
model tool call -> notes(action="save", text="250 * 3 = 750")
Python result -> {"status": "saved", ...}
result appended to messages -> model
final response -> user
```

Idhu expected flow illustration; actual model live output-nu assume panna vendam.
Dependent action-ku first result wait pannanum. Guess panna save aagura note wrong aagalam.
`run_turn` one question-ku several model/tool rounds handle pannum.
`while True` CLI-la several user questions handle pannum. **Two loops, two purposes.**

## Lesson 10: Errors without crash

Model `delete_everything` nu unknown tool ketta, lookup panna munnadi
`name not in FUNCTIONS` check reject pannum.
`current_time(city="Chennai")` na indha tool arguments accept pannaadhu;
validation error result return pannum. `notes(action=123)` na text venum,
number vandhirukku; adhaiyum reject pannum.

```python
try:
    result = FUNCTIONS[name](**arguments)
except (KeyError, TypeError, ValueError, OSError) as exc:
    return safe_name, {"error": str(exc)}
```

`try`: fail aagalaam-ngra work. `except`: expected failure vandha handle panra branch.
`KeyError`: key missing. `TypeError`: wrong data shape/type. `ValueError`: value invalid.
`OSError`: disk/network-related operation failure. `exc`: error object-ku name.
`str(exc)` readable text. Error-um model-kku `tool` observation-a send aagum.

Unknown programming bugs ellathayum silently hide pannala; known invalid inputs
and operational failures handle panrom. Error message vandha success-nu solla koodadhu.

## Lesson 11: Run the actual agent

Ollama open irukkanum; `llama3.2` downloaded irukkanum.

```powershell
python multi_agent.py
```

Alternative already-installed tools-capable model use panna:

```powershell
python multi_agent.py --model MODEL_NAME
```

Indha questions one by one type pannunga:

```text
Hi!
What is 250 * 3?
Thanks!
Add 50 to that result.
Save a note: Practice Python daily.
List my saved notes.
What is the current time in India?
/reset
List my saved notes.
/exit
```

Every call-ku `[tool call]` and `[tool result]` log varum. These are visible actions
and observations; **model-oda complete private thinking trace illa**.
Slow response-na CPU/model loading reason-a irukkalam; request 180 seconds wait pannum.

## Lesson 12: Tests, practice, and explanation

```powershell
python -m unittest discover -s tests -v
```

`-m unittest`: Python test module run pannum. `discover`: tests find pannum.
`-s tests`: indha folder-la start pannu. `-v`: each test name/result show pannu.
Mock model = fixed pretend response, so app logic repeatably check pannalam.
Adhu real model intelligence test illa; live chat separate-a check pannanum.
Tests temporary folder use pannum, unga saved notes-ai modify pannaadhu.

Practice tasks:

1. Greeting message-ai unga name include panna maathunga. Run panni paarunga.
2. `current_time()` result-la `india` and `utc` compare pannunga. Yen different? UTC offset.
3. Empty note save panna try pannunga. Error enga generate aagudhu?
4. `messages = ...` line-ai loop inside move pannina memory yen fail aagum-nu explain pannunga; actual source-ai maatha thevai illa.
5. Two calculations ketta, `that` ambiguous-a irundha model enna pannanum? Clarification kekkanum.

**Next reading:** `WEEK2_LINE_BY_LINE.md`-la `multi_agent.py`-oda every non-empty line-ku
explanation irukku. Old calculator internals-um adhe guide-la explain pannirukken.
