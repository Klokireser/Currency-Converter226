import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import urllib.request
import urllib.error
from datetime import datetime


HISTORY_FILE = "history.json"
API_URL = "https://open.er-api.com/v6/latest/{base}"  
CURRENCIES = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY", "TRY", "KZT", "UAH", "BYN"]


def load_history():
    """Загружает историю конвертаций из JSON-файла."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_history(history):
    """Сохраняет историю в JSON-файл."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)


def get_exchange_rate(base_currency, target_currency):
    """
    Получает курс валюты через open.er-api.com.
    Возвращает (курс, дата) или (None, сообщение об ошибке).
    """
    url = API_URL.format(base=base_currency)
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            if data.get("result") == "success":
                rate = data["rates"].get(target_currency)
                date = data.get("time_last_update_utc", "—")
                return rate, date
            else:
                return None, "Ошибка API: неверный ответ"
    except urllib.error.URLError as e:
        return None, f"Ошибка сети: {e}"
    except Exception as e:
        return None, f"Неизвестная ошибка: {e}"


def convert():
    """Основная функция: валидация, запрос к API, вывод результата."""
    amount_str = entry_amount.get().strip().replace(",", ".")
    try:
        amount = float(amount_str)
        if amount <= 0:
            messagebox.showwarning("Ошибка", "Сумма должна быть положительным числом.")
            return
    except ValueError:
        messagebox.showwarning("Ошибка", "Введите корректное число.")
        return

    base = combo_from.get()
    target = combo_to.get()

    if not base or not target:
        messagebox.showwarning("Ошибка", "Выберите валюты.")
        return

    rate, info = get_exchange_rate(base, target)
    if rate is None:
        messagebox.showerror("Ошибка", info)
        return

    result = round(amount * rate, 4)
    label_result.config(
        text=f"{amount} {base} = {result} {target}\nКурс: 1 {base} = {rate} {target}",
        fg="#27ae60"
    )

    record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "from": base,
        "to": target,
        "amount": amount,
        "result": result,
        "rate": rate
    }
    history.insert(0, record)  # Новые записи сверху
    save_history(history)
    update_tree()


def update_tree():
    """Заполняет Treeview данными из истории."""
    for row in tree.get_children():
        tree.delete(row)
    for record in history:
        tree.insert("", "end", values=(
            record["date"],
            f"{record['amount']} {record['from']}",
            f"{record['result']} {record['to']}",
            record["rate"]
        ))

def clear_history():
    """Очищает историю конвертаций."""
    if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
        history.clear()
        save_history(history)
        update_tree()
        label_result.config(text="Результат появится здесь", fg="#7f8c8d")

window = tk.Tk()
window.title("💱 Currency Converter")
window.geometry("700x550")
window.configure(bg="#f4f6f8")
window.resizable(False, False)

tk.Label(window, text="💱 Конвертер валют",
         font=("Arial", 18, "bold"), bg="#f4f6f8", fg="#2c3e50").pack(pady=10)

input_frame = tk.Frame(window, bg="#f4f6f8")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Сумма:", font=("Arial", 11), bg="#f4f6f8").grid(row=0, column=0, padx=5)
entry_amount = tk.Entry(input_frame, font=("Arial", 12), width=15)
entry_amount.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Из:", font=("Arial", 11), bg="#f4f6f8").grid(row=0, column=2, padx=5)
combo_from = ttk.Combobox(input_frame, values=CURRENCIES, state="readonly", width=8, font=("Arial", 11))
combo_from.set("USD")
combo_from.grid(row=0, column=3, padx=5)

tk.Label(input_frame, text="В:", font=("Arial", 11), bg="#f4f6f8").grid(row=0, column=4, padx=5)
combo_to = ttk.Combobox(input_frame, values=CURRENCIES, state="readonly", width=8, font=("Arial", 11))
combo_to.set("EUR")
combo_to.grid(row=0, column=5, padx=5)


btn_convert = tk.Button(window, text="🔄 Конвертировать", command=convert,
                        bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                        width=20, relief="flat", cursor="hand2")
btn_convert.pack(pady=5)


label_result = tk.Label(window, text="Результат появится здесь",
                        font=("Arial", 12), bg="#f4f6f8", fg="#7f8c8d")
label_result.pack(pady=10)

tk.Label(window, text="📜 История конвертаций",
         font=("Arial", 12, "bold"), bg="#f4f6f8", fg="#2c3e50").pack(pady=(10, 5))

columns = ("date", "from", "to", "rate")
tree = ttk.Treeview(window, columns=columns, show="headings", height=8)
tree.heading("date", text="Дата")
tree.heading("from", text="Из")
tree.heading("to", text="В")
tree.heading("rate", text="Курс")
tree.column("date", width=160)
tree.column("from", width=120)
tree.column("to", width=120)
tree.column("rate", width=120)
tree.pack(padx=20, pady=5)

btn_clear = tk.Button(window, text="🗑 Очистить историю", command=clear_history,
                      bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                      width=20, relief="flat", cursor="hand2")
btn_clear.pack(pady=5)


history = load_history()
update_tree()

window.mainloop()
