# Jak włączyć powiadomienia Discord

1. Na swoim serwerze Discord wejdź w ustawienia kanału i wybierz **Integracje**.
2. Utwórz nowy webhook i skopiuj jego adres URL.
3. Ustaw zmienną środowiskową `DISCORD_WEBHOOK_URL` z uzyskanym adresem
   lub wpisz go w pliku `TradingBotTV/config/settings.json` w sekcji `discord`:
   
   ```json
   {
       "discord": {"webhookUrl": "https://discord.com/api/webhooks/..."}
   }
   ```
4. Po uruchomieniu bota każda transakcja i ważna zmiana zostanie wysłana
   na wskazany kanał.
