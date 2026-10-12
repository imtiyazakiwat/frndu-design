"""Render frames in a folder to PNG and tile them into a contact sheet for review.

Usage: python3 sheet.py <folder-glob> <out.png> [scale]
"""
import glob
import os
import subprocess
import sys

from PIL import Image, ImageDraw

PHOTOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_assets', 'photos')
PHOTO_BASE = 'https://frndu-prototype.vercel.app/img/'
pat, out = sys.argv[1], sys.argv[2]
scale = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
files = sorted(glob.glob(pat))
w, h = int(390 * scale), int(844 * scale)
cols = min(6, len(files)) or 1
rows = (len(files) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (w + 10) + 10, rows * (h + 30) + 10), 'white')
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    png = '/tmp/_frndu_tile.png'
    # rsvg can't fetch remote photos: point them at design/_assets/photos (temp copy lives there)
    tmp = os.path.join(PHOTOS, '_tile.svg')
    open(tmp, 'w').write(open(f).read().replace(PHOTO_BASE, ''))
    subprocess.run(['rsvg-convert', '-w', str(w), tmp, '-o', png], check=True)
    os.remove(tmp)
    im = Image.open(png).convert('RGB')
    r, c = divmod(i, cols)
    x, y = 10 + c * (w + 10), 10 + r * (h + 30)
    sheet.paste(im, (x, y + 20))
    d.text((x, y + 4), os.path.basename(f).replace('.svg', '')[-40:], fill='black')
sheet.save(out)
os.remove('/tmp/_frndu_tile.png') if os.path.exists('/tmp/_frndu_tile.png') else None
print(out, len(files))
