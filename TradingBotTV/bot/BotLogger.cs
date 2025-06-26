using System;
using System.IO;

namespace Bot
{
    public static class BotLogger
    {
        private static readonly string LogFile = Path.Combine(AppContext.BaseDirectory, "logs", "bot.log");
        private static readonly object _lock = new object();
        private const long MaxLogSize = 5 * 1024 * 1024; // 5 MB

        public static void Log(string message)
        {
            var line = $"{DateTime.UtcNow:o} {message}";
            Console.WriteLine(line);
            try
            {
                Directory.CreateDirectory(Path.GetDirectoryName(LogFile)!);
                lock (_lock)
                {
                    RotateIfNeeded();
                    File.AppendAllText(LogFile, line + Environment.NewLine);
                }
            }
            catch
            {
                // ignore logging errors
            }
        }

        private static void RotateIfNeeded()
        {
            try
            {
                if (File.Exists(LogFile))
                {
                    var info = new FileInfo(LogFile);
                    if (info.Length > MaxLogSize)
                    {
                        var backup = LogFile + ".old";
                        File.Copy(LogFile, backup, true);
                        File.WriteAllText(LogFile, string.Empty);
                    }
                }
            }
            catch
            {
                // ignore rotation errors
            }
        }
    }
}
