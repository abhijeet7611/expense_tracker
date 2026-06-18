import sys
from pathlib import Path

log = Path('verify_runtime.log')

lines = []
lines.append(f'python={sys.executable}')

mods = ['fastapi', 'uvicorn', 'sqlalchemy', 'passlib', 'bcrypt', 'jose', 'dotenv']
for name in mods:
    try:
        __import__(name)
        lines.append(f'{name}=OK')
    except Exception as e:
        lines.append(f'{name}=FAIL:{e}')

log.write_text('\n'.join(lines), encoding='utf-8')
print('WROTE', log)
