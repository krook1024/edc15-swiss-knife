pyinstaller --clean^
  --collect-all tools^
  --add-data tools/lib/*;tools/lib/^
  --noconfirm^
  --noconsole^
  .\main.py