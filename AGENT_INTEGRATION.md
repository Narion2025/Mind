# Custom GPT Integration Guide

Dieses Dokument beschreibt die finale Anbindung externer GPT-Agenten an das Narion Mind System anhand des "Everything-Bridge v3" Gateways.

## 1. Gateway einsetzen

Der Dienst `wirklichkeits-api/gateway.py` stellt eine FastAPI-Anwendung bereit. Er verwaltet sogenannte *Anchors*, also YAML-Dateien, die Identität und Berechtigungen eines GPT-Agenten beschreiben.

### Endpunkte

- `PUT /anchors/{gpt_id}` – legt einen Anchor an oder aktualisiert ihn.
- `GET /anchors/{gpt_id}` – ruft die Anchor-YAML ab.
- `PATCH /anchors/{gpt_id}` – partielles Update.
- `GET /state` – Health-Check.
- `WS /ws/state` – informiert bei Änderungen.

Alle Anchor-Operationen benötigen ein JWT mit dem Claim `roles` und der jeweiligen Berechtigung (`anchor.write` bzw. `anchor.read`). Optional kann ein `X-HMAC-Signature` Header genutzt werden, falls keine JWT-Unterstützung vorhanden ist.

## 2. Anchor-Datei

Ein Anchor entspricht dem Schema `AnchorV1` (siehe OpenAPI in `action/custom_gpt_manager.yaml`). Die Dateien werden unter `init/anchors/{gpt_id}.yaml` gespeichert. Ein Minimalbeispiel:

```yaml
gpt_id: my-agent
version: "1.0"
identity: "Kurzbeschreibung"
permissions:
  - thoughts
  - narrative
```

## 3. Setup-Oberfläche

Unter `/custom_gpt_setup.html` befindet sich ein einfaches Formular. Die Eingabe einer GPT-ID führt einen `PUT /anchors/{id}` aus und erzeugt damit die zugehörige Anchor-Datei auf dem Server.

## 4. Integration in ChatGPT

`action/custom_gpt_manager.yaml` beschreibt die API für ChatGPT-Functions. Binden Sie diese Datei ein und rufen Sie `createAnchor` bzw. `patchAnchor` auf, um einen Agenten zu registrieren. Anschließend kann der Agent seine YAML-Dateien für Gedanken, Narrative oder Wissenseinträge ablegen.

Für die Verbindung werden die Umgebungsvariablen `JWT_PUBLIC_KEY` und optional `HMAC_SECRET` benötigt. Ohne gültiges JWT bzw. HMAC lehnt der Gateway die Anfrage ab.
