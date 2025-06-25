using System;

namespace Bot
{
    public static class BotController
    {
        private static bool _tradingEnabled = true;

        public static bool TradingEnabled
        {
            get => _tradingEnabled;
            set => _tradingEnabled = value;
        }

        public static void Toggle() => _tradingEnabled = !_tradingEnabled;
    }
}
