# Cloud Telegram Assistant

Проект самостоятельного Telegram-помощника по принципам оригинального ChatGPT Dots.

**Статус: подготовка облачной среды. Бот ещё не реализован и не запущен.**

Целевая среда Codex Cloud: `tracker`. Репозиторий: `quadromix/tracker`.
Работа должна выполняться в облаке OpenAI, без зависимости от локального компьютера или стороннего VPS.

## Продолжение в Codex Cloud

Откройте задачу в среде tracker с этим репозиторием и поручите:

> Реализуй и запусти Telegram-помощника согласно AGENTS.md. Сначала выполни python3 scripts/preflight.py. Используй три уже сохранённых секрета среды, не показывая их. Проверь реальную доступность Agents API и облачного механизма приёма сообщений и пробуждений. Заверши проверкой ответа бота в Telegram и сохранения контекста после перезапуска. Не называй подготовку или запуск процесса работающим постоянным сервисом.

## Конфигурация

Среда должна предоставлять `open_ai_api_tg`, `telegram_codex_bot_api_token`, `telegram_user_id`.
Разрешённые HTTPS-сервисы: api.openai.com и api.telegram.org.
Секреты Codex Cloud не становятся автоматически секретами GitHub Actions.

Этот репозиторий публичный. Здесь хранится только код. Секреты, история сообщений, память и результаты личных задач должны оставаться в приватном облачном хранилище.

## Проверка

`python3 scripts/preflight.py` проверяет наличие переменных, getMe/getWebhookInfo Telegram и доступ к списку моделей OpenAI. Не получает сообщения, не отправляет их, не сбрасывает webhook и не запускает платную генерацию. Успех проверки ещё не подтверждает доступ к Agents API.

## Документация

- https://learn.chatgpt.com/docs/dots
- https://developers.openai.com/api/docs/guides/agents-api/overview
- https://developers.openai.com/api/docs/guides/agents-api/quickstart
- https://developers.openai.com/api/docs/guides/agents-api/sessions/automations
