using System;
using System.IO;

namespace Bot
{
    public static class BotLogger
    {
        private static readonly string LogFile = Path.Combine(AppContext.BaseDirectory, "logs", "bot.log");
        private static readonly object _lock = new object();

        public static void Log(string message)
        {
            var line = $"{DateTime.UtcNow:o} {message}";
            Console.WriteLine(line);
            try
            {
                Directory.CreateDirectory(Path.GetDirectoryName(LogFile)!);
                lock (_lock)
                {
                    File.AppendAllText(LogFile, line + Environment.NewLine);
                }
            }
            catch
            {
                // ignore logging errors
            }
        }
    }
}
