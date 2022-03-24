Feature: Config Provider (Zugriff auf Konfig-Files)
  Als Entwickler brauche ich einen komfortablen Weg, um auf Konfigurationsdateien zuzugreifen.

  Scenario: Zugriff auf eine existierende Datei
    Given eine existierende Datei, z. B. 'check_rs500.ini'
    When das ConfigProvider-Objekt für die genannte Datei erzeugt wird
    Then entsteht ein Objekt (es ist nicht None)
    Then Objekt ist vom Typ ConfigProvider
    Then enthält das Objekt Schlüssel

  Scenario: Zugriff auf eine nicht existierende Datei
    Given eine nicht-existierende Datei, z. B. 'gibtesnicht.null'
    When das ConfigProvider-Objekt für die genannte Datei erzeugt wird
    Then wird eine Exception vom Typ 'FileNotFoundError' geworfen
