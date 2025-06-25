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

        public static void CheckDrawdown()
        {
            var pnl = TradeLogger.AnalyzePnL();
            var limit = -(ConfigManager.InitialCapital * ConfigManager.MaxDrawdownPercent / 100m);
            if (pnl <= limit && _tradingEnabled)
            {
                _tradingEnabled = false;
                BotLogger.Log($"\u26D4 Osi\u0105gni\u0119to drawdown {pnl:F2}, limit {-limit:F2}. Handel wy\u0142\u0105czony.");
            }
        }
    }
}
