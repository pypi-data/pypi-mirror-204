# ThorpyWebsite (c) Yann Thorimbert 2023

How to generate site :
* Set the root for Thorpy in generate_website.py
* Run generate_website.py

How to update elements :
* Nothing special to do for the doc description, it is automatic as long as you indicate things in docstrings
* For the image, put an image with the same name as the class (but lowercase) in the doc folder

Upload on PyPi :
1. pip install twine setuptools wheel
2. python setup.py sdist bdist_wheel
3. twine upload dist/*
Account : Thorpy
Pwd : Don't worry


***TODO***

pygame mailing list

lien vers thorpy1 website et github archivés, et dernier message thorpy


# versions + tard: ####################################################################
#TODOs
#script de tutos auto basé sur les commentaires
# detecter quels examples figurent pas dans les automatiquement proposes et faire un systeme de tags bijectifs
#lifebar vertical
# site : quand on hover un element de code d'example, un encart qui explique ce qu'est l'élément apparait
# offset du style pour effet d'appui
# flash du DDL : a cause de launch_nonblocking=True
# gen oscillating lights et autres ==> a ranger dans la lib, fair un truc du style:
# my_element.fx.add_oscillating_light(...)
# my_element.fx.add_shadow(...)
# my_element.fx.add_particle_emission(...)
# my_element.fx.add_bloom(...)
# bloom https://www.youtube.com/watch?v=ml-5OGZC7vE
#masque pour appliquer degradé sur polygone
#hyphenize autocut line
#life heart tout faits (arg : img_full and img_empty)
#TODO: inclure thornoise, et utiliser pour joli animations electriques ainsi que pour generer un fond de nuages pour exemples
#include les autre utils de thorpy
#TODO: thorpypack --> thorpy, thornoise, thorphys, thorpyfx
#miscgui du vieux thorpy ==> HUD
# * slider with text vertical ; teleport dragger of slider at click
#text input on focus : option de delete ancien contenu dès l'écriture du nouveau (comme un ctrl+A)
#shadowgen optimises pour les round rect
#texte riche peut etre augmente en changeant les attributs de font (font, fontsize, antialias, bold, italic) (prochaine version)
#italic et gras marchent que quand on appelle manuellement set_default_font()