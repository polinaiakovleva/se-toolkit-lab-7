import sys
import json
import httpx
from config import config
from services.api import LMSClient
from services.llm import LLMClient
from services.tools import tools

llm = LLMClient()
api = LMSClient()


# ---- Tools ----
def get_items(args):
    resp = api.get_items()
    if resp.status_code == 200:
        items = resp.json()
        labs = [i["title"] for i in items if i.get("type") == "lab"]
        return f"Found {len(labs)} labs: " + ", ".join(labs)
    return f"Error fetching items: {resp.status_code}"


def get_learners(args):
    resp = api.get_learners()
    if resp.status_code == 200:
        learners = resp.json()
        return f"Total learners: {len(learners)}"
    return f"Error: {resp.status_code}"


def get_scores(args):
    lab = args.get("lab")
    if not lab:
        return "Missing lab parameter"
    resp = api._get(f"analytics/scores?lab={lab}")
    if resp.status_code == 200:
        return f"Scores for {lab}: {resp.json()}"
    return f"Error: {resp.status_code}"


def get_pass_rates(args):
    lab = args.get("lab")
    if not lab:
        return "Missing lab parameter"
    resp = api._get(f"analytics/pass-rates?lab={lab}")
    if resp.status_code == 200:
        data = resp.json()
        lines = [f"Pass rates for {lab}:"]
        for item in data:
            lines.append(f"- {item['task']}: {item['avg_score']}% ({item['attempts']} attempts)")
        return "\n".join(lines)
    return f"Error: {resp.status_code}"


def get_timeline(args):
    lab = args.get("lab")
    if not lab:
        return "Missing lab parameter"
    resp = api._get(f"analytics/timeline?lab={lab}")
    if resp.status_code == 200:
        return f"Timeline for {lab}: {len(resp.json())} days of data"
    return f"Error: {resp.status_code}"


def get_groups(args):
    lab = args.get("lab")
    if not lab:
        return "Missing lab parameter"
    resp = api._get(f"analytics/groups?lab={lab}")
    if resp.status_code == 200:
        data = resp.json()
        groups = [f"{g['group']}: {g['avg_score']}% ({g['students']} students)" for g in data]
        return "Groups performance:\n" + "\n".join(groups)
    return f"Error: {resp.status_code}"


def get_top_learners(args):
    lab = args.get("lab")
    limit = args.get("limit", 5)
    if not lab:
        return "Missing lab parameter"
    resp = api._get(f"analytics/top-learners?lab={lab}&limit={limit}")
    if resp.status_code == 200:
        data = resp.json()
        learners = [f"{i+1}. {l['name']} - {l['score']}%" for i, l in enumerate(data)]
        return f"Top {len(data)} learners in {lab}:\n" + "\n".join(learners)
    return f"Error: {resp.status_code}"


def get_completion_rate(args):
    lab = args.get("lab")
    if not lab:
        return "Missing lab parameter"
    resp = api._get(f"analytics/completion-rate?lab={lab}")
    if resp.status_code == 200:
        return f"Completion rate for {lab}: {resp.json()['completion_rate']}%"
    return f"Error: {resp.status_code}"


def trigger_sync(args):
    resp = httpx.post(
        f"{api.base_url}/pipeline/sync",
        headers=api.headers,
        json={},
        timeout=30
    )
    if resp.status_code == 200:
        return "Sync triggered successfully."
    return f"Sync failed: {resp.status_code}"


function_map = {
    "get_items": get_items,
    "get_learners": get_learners,
    "get_scores": get_scores,
    "get_pass_rates": get_pass_rates,
    "get_timeline": get_timeline,
    "get_groups": get_groups,
    "get_top_learners": get_top_learners,
    "get_completion_rate": get_completion_rate,
    "trigger_sync": trigger_sync,
}


system_prompt = (
    "You are a helpful assistant for an LMS system. "
    "You MUST use tools to answer questions. "
    "For student-related questions, use get_learners. "
    "For pass rate comparisons, call get_items and then get_pass_rates for each lab. "
    "Always compute and return a FINAL answer with numbers and lab names. "
    "Do not stop early. Do not say 'let me check'. "
    "Always produce a final conclusion."
)


def handle(user_message: str) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    max_iterations = 15
    last_tool_calls = set()

    for _ in range(max_iterations):
        try:
            response = llm.chat_completion(messages, tools=tools)
        except Exception as e:
            return f"LLM error: {e}"

        message = response["choices"][0]["message"]

        if not message.get("tool_calls"):
            content = message.get("content", "")

            if content and ("%" in content or "lab" in content.lower()):
                return content

            messages.append(message)
            continue

        # защита от зацикливания
        current_calls = tuple(
            (tc["function"]["name"], frozenset(json.loads(tc["function"]["arguments"]).items()))
            for tc in message["tool_calls"]
        )

        if current_calls in last_tool_calls:
            return "I'm having trouble getting the data. Please try again later."

        last_tool_calls.add(current_calls)

        tool_results = []

        for tool_call in message["tool_calls"]:
            func_name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["arguments"])

            print(f"[tool] LLM called: {func_name}({args})", file=sys.stderr)

            if func_name in function_map:
                result = function_map[func_name](args)
                print(f"[tool] Result: {result[:100]}...", file=sys.stderr)

                tool_results.append({
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": func_name,
                    "content": json.dumps(result)
                })
            else:
                tool_results.append({
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": func_name,
                    "content": f"Unknown tool: {func_name}"
                })

        messages.append(message)
        messages.extend(tool_results)

    return "Maximum iterations reached."


async def handle_telegram(update, context):
    user_message = update.message.text
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )
    response = handle(user_message)
    await update.message.reply_text(response)
