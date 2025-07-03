from pathlib import Path
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOT_CSPROJ = PROJECT_ROOT / 'TradingBotTV' / 'bot' / 'BinanceTraderBot.csproj'
BOT_NAME = 'Trytonator2137'
# entry point for optimizer CLI
PY_ENTRY = PROJECT_ROOT / 'TradingBotTV' / 'ml_optimizer' / 'auto_optimizer.py'
GUI_ENTRY = PROJECT_ROOT / 'TradingBotTV' / 'gui_panel.py'


def run(cmd):
    cmd = [str(c) for c in cmd]
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
        '-o', str(dist_dir / BOT_NAME)
    ])

    exe_path = dist_dir / BOT_NAME / 'BinanceTraderBot.exe'
    if exe_path.exists():
        exe_path.rename(dist_dir / BOT_NAME / f'{BOT_NAME}.exe')

    # Build Python optimizer executable
    run([
        'python', '-m', 'PyInstaller', '--onefile',
        '--name', BOT_NAME,
        '--distpath', str(dist_dir / 'python'),
        str(PY_ENTRY)
    ])

    # Build GUI executable
    run([
        'python', '-m', 'PyInstaller', '--onefile',
        '--name', f'{BOT_NAME}_gui',
        '--distpath', str(dist_dir / 'python'),
        str(GUI_ENTRY)
    ])

    print('Installer artifacts created in', dist_dir)


if __name__ == '__main__':
    main()
