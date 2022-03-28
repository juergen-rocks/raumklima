#language: de

Funktionalität: Zugriff auf eine Raumklimastation (Manueller Testlauf)

  @manual
  Szenario: Ablesen der Werte für die ersten beiden Kanäle
      Gegeben sei ein Raspberry Pi mit einer Installation gemäß Anleitung
              Und eine verbundene Raumklimastation
              Und mindestens zwei verbundene Sensoren
             Wenn das Python-Skript 'read_rs500.py' ausgeführt wird
             Dann wird für den ersten Kanal richtige Werte ausgegeben
              Und wird für den zweiten Kanal richtige Werte ausgegeben
