# Jak włączyć powiadomienia Discord

1. Na swoim serwerze Discord wejdź w ustawienia kanału i wybierz **Integracje**.
2. Utwórz nowy webhook i skopiuj jego adres URL.
3. Wpisz adres w zmiennej `DISCORD_WEBHOOK_URL` lub w polu
   `webhookUrl` w `TradingBotTV/config/settings.json`:
   
   ```json
   {
       "discord": {"webhookUrl": "https://discord.com/api/webhooks/..."}
   }
   ```
4. Zapisz plik `.env` i uruchom bota lub przetestuj połączenie poleceniem:

   ```bash
   python -c "from TradingBotTV.ml_optimizer.alerts import send_discord_message; send_discord_message('test')"
   ```

   Jeśli widzisz wiadomość testową, integracja działa.
