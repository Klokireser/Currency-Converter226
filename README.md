# Currency-Converter226
Графическое приложение для конвертации валют с использованием актуальных курсов и сохранением истории операций.

## Автор
**Николай Замараев**  

## API-ключ
В проекте используется **бесплатный публичный API** [ExchangeRate-API (open.er-api.com)](https://www.exchangerate-api.com/), который **не требует регистрации и API-ключа**.

Если вы хотите использовать другой сервис (например, `exchangerate-api.com` с ключом):
1. Зарегистрируйтесь на [exchangerate-api.com](https://www.exchangerate-api.com/).
2. Получите бесплатный API-ключ в личном кабинете.
3. Замените в коде `API_URL` на:  
   `https://v6.exchangerate-api.com/v6/ВАШ_КЛЮЧ/latest/{base}`

## Как запустить
1. Убедитесь, что установлен Python 3.8+.
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш_логин/currency-converter.git
   cd currency-converter
