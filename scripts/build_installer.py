from pathlib import Path
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOT_CSPROJ = PROJECT_ROOT / 'TradingBotTV' / 'bot' / 'BinanceTraderBot.csproj'
PY_ENTRY = PROJECT_ROOT / 'TradingBotTV' / 'ml_optimizer' / '__main__.py'
GUI_ENTRY = PROJECT_ROOT / 'TradingBotTV' / 'gui_panel.py'


def run(cmd):
    print('Running:', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def main():
    dist_dir = PROJECT_ROOT / 'dist'
    dist_dir.mkdir(parents=True, exist_ok=True)

    # Build C# binary
    run([
        'dotnet', 'publish', BOT_CSPROJ,
        '-c', 'Release',
        '-r', 'win-x64',
        '-p:PublishSingleFile=true',
        '--self-contained', 'false',
        '-o', str(dist_dir / 'binancebot')
    ])

    # Build Python optimizer executable
    run([
        'pyinstaller', '--onefile',
        '--distpath', str(dist_dir / 'python'),
        str(PY_ENTRY)
    ])

    # Build GUI executable
    run([
        'pyinstaller', '--onefile',
        '--distpath', str(dist_dir / 'python'),
        str(GUI_ENTRY)
    ])

    print('Installer artifacts created in', dist_dir)


if __name__ == '__main__':
    main()
