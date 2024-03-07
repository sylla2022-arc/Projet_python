from pathlib import Path

"""Trier les fichiers contenus dans le dossier data selon les associations suivantes :
mp3, wav, flac : Musique
avi, mp4, gif : Videos
bmp, png, jpg : Images
txt, pptx, csv, xls, odp, pages : Documents
autres : Divers
"""

dics = {'.png': 'Images', '.jpep': 'Images', '.jpg': 'Images', '.gif': 'Images','.JPG': 'Images',
        '.mp4': 'Videos', '.mov': 'Videos', ".avi": "Videos", ".mpeg": "Videos",
        '.zip': 'Archives', '.tar': 'Archives', ".mp3" : 'Musique', '.wav': 'Musique', ".flac" : "Musique",
        '.pdf': 'Documents', '.txt': 'Documents', '.docx': 'Documents' , '.doc': 'Documents',
        '.odt': 'Documents', '.xlsx': 'Documents',
        '.json': 'Documents'}

p = Path.cwd() / "data"  
files = [f for f in p.iterdir() if f.is_file()]

for f in files:
    output_dir = p / dics.get(f.suffix, "Autres")
    output_dir.mkdir(exist_ok=True)
    f.rename(output_dir / f.name)  
