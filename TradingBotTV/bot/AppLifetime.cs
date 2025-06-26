using System.Threading;

namespace Bot
{
    public static class AppLifetime
    {
        public static readonly CancellationTokenSource Source = new();
    }
}
