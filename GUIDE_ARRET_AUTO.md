# ⏱️ ARRÊT AUTOMATIQUE - Guide Rapide

## ✅ C'est fait !

Ton application s'arrête maintenant **automatiquement après 5 minutes d'inactivité**.

## 🎯 Ce qui a changé

### Avant ❌
- Le serveur tournait indéfiniment en arrière-plan
- Tu devais fermer manuellement via le Gestionnaire des tâches

### Maintenant ✅
- Le serveur se ferme automatiquement après 5 minutes sans activité
- Plus besoin de gérer manuellement l'arrêt

## 📝 Comment ça marche

**Chaque action réinitialise le timer :**
- Upload d'images
- Combinaison d'images
- Chargement de la page

**Si aucune action pendant 5 minutes :**
- 🛑 Le serveur s'arrête automatiquement
- 🗑️ L'application se ferme complètement

## 🔄 Pour utiliser la nouvelle version

1. **Remplace ton `app.py`** par le nouveau
2. **Remplace `templates/index.html`** par le nouveau
3. **Recompile l'EXE** :
   ```bash
   build_exe.bat
   ```

## 📁 Fichiers à télécharger

- [app.py](computer:///mnt/user-data/outputs/app.py) - Avec arrêt auto
- [index.html](computer:///mnt/user-data/outputs/index.html) - Avec notification
- [Documentation complète](computer:///mnt/user-data/outputs/ARRET_AUTOMATIQUE.md)

## ⚙️ Personnaliser le délai

Dans `app.py` ligne 19, change la valeur :

```python
INACTIVITY_TIMEOUT = 300  # 5 minutes (défaut)
```

**Exemples :**
- 2 minutes : `120`
- 10 minutes : `600`
- 30 minutes : `1800`

## 🧪 Test rapide

1. Lance l'app
2. Utilise-la normalement
3. Laisse-la inactive 5 minutes
4. ✅ Elle se ferme toute seule !

---

## 💡 Notes importantes

- ✅ Le timer se réinitialise à **chaque** action
- ✅ L'arrêt est **propre** (pas de crash)
- ✅ Un message apparaît dans l'interface
- ✅ Tu peux toujours fermer manuellement

---

🎉 Fini ! Plus besoin de gérer l'arrêt manuellement !
