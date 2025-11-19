import os
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from full_prompt import build_prompt

LMSTUDIO_URL = "http://127.0.0.1:12345/v1/chat/completions"
LMSTUDIO_MODEL = "google/gemma-3-4b"
MATERIAL_FILE = "z5.txt"


def load_material() -> str:
    if not os.path.exists(MATERIAL_FILE):
        return f"❌ Файл {MATERIAL_FILE} не найден!"

    with open(MATERIAL_FILE, "r", encoding="utf-8") as f:
        return f.read()


def generate_test_from_text(max_retries=2):
    material_text = load_material()
    if material_text.startswith("❌"):
        return material_text
    prompt = build_prompt(material_text)

    payload = {
        "model": LMSTUDIO_MODEL,
        "messages": [
            {"role": "system",
             "content": "Ты — генератор тестов. Ты создаешь вопросы строго по требованиям пользователя."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 4000
    }

    for attempt in range(max_retries + 1):
        try:
            response = requests.post(LMSTUDIO_URL, json=payload, timeout=240)

            if response.status_code == 503:
                if attempt < max_retries:
                    continue
                return "❌ LM Studio ответил 503 (модель не готова или перегружена)."

            if response.status_code == 404:
                return "❌ Модель не найдена. Проверь название модели в LM Studio."

            if response.status_code == 500:
                return "❌ Внутренняя ошибка LM Studio (500). Перезапусти модель."

            response.raise_for_status()

            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not content:
                return "❌ Ошибка: пустой ответ от модели."

            return content.strip()

        except ConnectionError:
            if attempt < max_retries:
                continue
            return "❌ Ошибка подключения: LM Studio не отвечает."

        except Timeout:
            if attempt < max_retries:
                continue
            return "❌ Таймаут: модель слишком долго формирует ответ."

        except RequestException as e:
            return f"❌ Ошибка HTTP: {str(e)}"

        except Exception as e:
            return f"❌ Неожиданная ошибка: {str(e)}"

    return "❌ Ошибка: не удалось получить ответ от модели."
