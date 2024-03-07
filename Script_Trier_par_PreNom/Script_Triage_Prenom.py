"""
Dans cet exercice vous devez :
Ouvrir le fichier prenoms.txt et lire son contenu.
Récupérer chaque prénom séparément dans une liste.
Nettoyer les prénoms pour enlever les virgules, points ou espace.
Écrire la liste ordonnée et nettoyée dans un nouveau fichier texte.
"""
# Methode_1: Débutant

from pathlib import Path
p = Path.cwd()
p = p / "prenoms.txt"
# Ouvrir le fichier prenoms.txt et lire son contenu.
text = p.read_text(encoding='utf-8')
print(text)
print('--'*50)
# Récupérer chaque prénom séparément dans une liste 
liste_prenoms = []
for mot in text.split(', '): # Supprimer les virgules
    mot = mot.strip()
    liste_prenoms.append(mot)
    # Nettoyer les prénoms pour enlever le retour à la ligne et les espace
    if '\n' in mot:
        mot_1, mot_2 = mot.split('\n')
        liste_prenoms.remove(mot)
        liste_prenoms.append(mot_1.strip())
        liste_prenoms.append(mot_2.strip())
    if '' in liste_prenoms :
        liste_prenoms.remove('')
# Nettoyage finale des prénoms pour enlever les virgules, points ou espace.
for mot in liste_prenoms:
    if ' ' in mot :
        mot_1, mot_2 = mot.split(' ')
        liste_prenoms.remove(mot)
        liste_prenoms.append(mot_1.strip().strip('.'))
        liste_prenoms.append(mot_2.strip().strip('.'))
liste_prenoms.sort()

for i, mot in enumerate(liste_prenoms, start=1):
    print(f"{i}. {mot}")
    

# Methiode 2: Expert
    
with open("prenoms.txt", "r") as f:
    lines = f.read().splitlines()

prenoms = []
for line in lines:
    prenoms.extend(line.split())

prenoms_final = [prenom.strip(",. ") for prenom in prenoms]

with open("prenoms_final.txt", "w") as f:
    f.write("\n".join(sorted(prenoms_final)))
print(prenoms_final)
    