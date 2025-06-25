using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;
using System.IO;
using System.Threading.Tasks;

namespace Bot
{
    public static class DashboardServer
    {
        public static void Start()
        {
            var builder = WebApplication.CreateBuilder();
            var app = builder.Build();

            app.MapGet("/", async context =>
            {
                var pnl = TradeLogger.AnalyzePnL();
                var net = TradeLogger.GetNetPosition();
                var trading = BotController.TradingEnabled ? "ON" : "OFF";

                var html = $@"<!doctype html>
<html><head><meta charset='utf-8'><style>
body {{font-family: Arial, sans-serif; margin:20px;}}
.grid {{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;}}
.tile {{padding:20px;background:#f0f0f0;border-radius:8px;text-align:center;}}
button{{padding:10px 20px;font-size:16px;}}
pre{{white-space:pre-wrap;}}
</style></head>
<body>
<h1>BinanceTraderBot Dashboard</h1>
<div class='grid'>
<div class='tile'><h3>PNL</h3><p>{pnl:F2}</p></div>
<div class='tile'><h3>Net Position</h3><p>{net:F6}</p></div>
<div class='tile'><h3>Trading</h3><p>{trading}</p>
<form method='post' action='/toggle'><button>Toggle</button></form></div>
<div class='tile'><h3>Logs</h3><a href='/logs'>View</a></div>
</div>
</body></html>";
                context.Response.ContentType = "text/html";
                await context.Response.WriteAsync(html);
            });

            app.MapGet("/logs", async context =>
            {
                var path = TradeLogger.LogPath;
                if (!File.Exists(path))
                {
                    await context.Response.WriteAsync("No logs yet.");
                    return;
                }
                var text = await File.ReadAllTextAsync(path);
                context.Response.ContentType = "text/html";
                await context.Response.WriteAsync("<pre>" + System.Net.WebUtility.HtmlEncode(text) + "</pre>");
            });

            app.MapPost("/toggle", context =>
            {
                BotController.Toggle();
                context.Response.Redirect("/");
                return Task.CompletedTask;
            });

            app.Run("http://localhost:5001");
        }
    }
}
