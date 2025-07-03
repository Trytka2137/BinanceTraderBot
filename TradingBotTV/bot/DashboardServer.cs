using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;
using System.IO;
using System.Threading.Tasks;
using System.Threading;

namespace Bot
{
    public static class DashboardServer
    {
        public static void Start(CancellationToken token)
        {
            var builder = WebApplication.CreateBuilder();
            var app = builder.Build();

            app.Use(async (context, next) =>
            {
                var user = Environment.GetEnvironmentVariable("DASHBOARD_USERNAME");
                var pass = Environment.GetEnvironmentVariable("DASHBOARD_PASSWORD");
                if (!string.IsNullOrEmpty(user) && !string.IsNullOrEmpty(pass))
                {
                    if (!context.Request.Headers.TryGetValue("Authorization", out var header) ||
                        !header.ToString().StartsWith("Basic "))
                    {
                        context.Response.Headers["WWW-Authenticate"] = "Basic";
                        context.Response.StatusCode = 401;
                        await context.Response.WriteAsync("Authentication required");
                        return;
                    }

                    var encoded = header.ToString()["Basic ".Length..].Trim();
                    var bytes = Convert.FromBase64String(encoded);
                    var credential = System.Text.Encoding.UTF8.GetString(bytes).Split(':', 2);
                    if (credential.Length != 2 || credential[0] != user || credential[1] != pass)
                    {
                        context.Response.StatusCode = 401;
                        await context.Response.WriteAsync("Invalid credentials");
                        return;
                    }
                }

                await next();
            });

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

            app.Urls.Add("http://localhost:5001");
            app.RunAsync(token).GetAwaiter().GetResult();
        }
    }
}
