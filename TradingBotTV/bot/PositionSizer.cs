using System;

namespace Bot
{
    public static class PositionSizer
    {
        public static decimal GetTradeAmount(decimal price, string side)
        {
            var pnl = TradeLogger.AnalyzePnL();
            var balance = ConfigManager.InitialCapital + pnl;
            if (balance <= 0 || price <= 0) return ConfigManager.Amount;

            decimal riskPercent = side.Equals("BUY", StringComparison.OrdinalIgnoreCase) ? 0.1m : 0.08m;
            var capital = balance * riskPercent;
            var quantity = capital / price;
            if (quantity <= 0) quantity = ConfigManager.Amount;
            return Math.Round(quantity, 6);
        }
    }
}
