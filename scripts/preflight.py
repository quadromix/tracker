"""Read-only cloud configuration checks. No secret values or HTTP URLs in logs."""
import json
import os
import sys
import urllib.request
import urllib.error


def request(url, headers=None):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=20) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError("HTTP status " + str(exc.code)) from None
    except Exception:
        raise RuntimeError("Network, TLS or response parsing failure") from None


def main():
    names = ("open_ai_api_tg", "telegram_codex_bot_api_token", "telegram_user_id")
    values = {name: os.environ.get(name, "").strip() for name in names}
    missing = [name for name, value in values.items() if not value]
    if missing:
        print("Missing environment variables: " + ", ".join(missing))
        return 1
    if not values["telegram_user_id"].isdigit() or int(values["telegram_user_id"]) <= 0:
        print("telegram_user_id must be a positive numeric owner ID")
        return 1
    try:
        base = "https://api.telegram.org/bot" + values["telegram_codex_bot_api_token"]
        identity = request(base + "/getMe")
        if identity.get("ok") is not True or not identity.get("result", {}).get("is_bot"):
            raise RuntimeError("Telegram bot identity check failed")
        print("Telegram bot identity: verified")
        webhook = request(base + "/getWebhookInfo")
        if webhook.get("ok") is not True:
            raise RuntimeError("Telegram webhook inspection failed")
        if webhook.get("result", {}).get("url"):
            print("Existing webhook detected: preserve it and inspect ownership before deployment")
            return 2
        print("Telegram webhook: absent; polling is not started by this check")
        models = request("https://api.openai.com/v1/models", {"Authorization": "Bearer " + values["open_ai_api_tg"]})
        if not isinstance(models.get("data"), list):
            raise RuntimeError("OpenAI models response invalid")
        print("OpenAI authentication: verified; Agents API permissions still require verification")
        print("Preflight complete. No messages sent; no agent deployed.")
        return 0
    except RuntimeError as exc:
        print("Preflight failed: " + str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
