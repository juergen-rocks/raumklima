# Anleitung zum Beitragen

Dies ist ein winziges Projekt, wir wollen es mit Regeln nicht übertreiben. Daher gibt es hier nur ein paar wenige Eckpunkte.


## Grundstruktur der Branches

Die Weiterentwicklung findet auf dem Branch `develop` statt. Insofern ist auch dieser Branch Anlaufstelle für die meisten Pull-Requests.

Sollte ein Pull-Request ein wichtiges Bugfix für einen schwerwiegenden Fehler darstellen, sollte er gegen den `main`-Branch gestellt werden. Der Bugfix würde dann im weiteren Verlauf nach `develop` gemerged werden.


## Kein PR ohne Tests

Code-Änderungen sollten mit Tests hinterlegt sein. Bestehende Tests sollten nicht brechen.