using System;
using System.Threading.Tasks;

namespace Bot
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("🚀 Bot uruchomiony. Oczekuję na sygnały z TradingView...");

            ConfigManager.Load();

            // Start serwera webhook i silnika strategii w tle
            Task.Run(() => WebhookServer.Start());
            Task.Run(() => StrategyEngine.StartAsync());

            // Odpalamy optymalizację ML co np. 1h i przeładowujemy config
            while (true)
            {
                Console.WriteLine("🧠 Uruchamiam optymalizację ML...");
                await OptimizerRunner.RunOptimizationAndReloadAsync(ConfigManager.Symbol);

                Console.WriteLine("⏳ Czekam 1h na kolejną optymalizację...");
                await Task.Delay(TimeSpan.FromHours(1));
            }
        }
    }
}
