# Secret Management API

The `mind_bus_api.py` server exposes endpoints to upload and manage API keys.
All operations require the role `secrets.edit` via the `X-Role` header.

## Endpoints

- `POST /secrets/upload`
  - Accepts either JSON `{ "key": "NAME", "value": "VALUE" }` or a multipart
    upload with a `.env` file (`file` field).
  - Stores each key securely and updates the running environment.

- `GET /secrets`
  - Returns a list of stored keys with masked previews and timestamps.

- `PATCH /secrets/{key}`
  - Replaces the value for the given key.

- `DELETE /secrets/{key}`
  - Removes the key from the store and environment.

## Dashboard UI

The dashboard contains a settings drawer (⚙️ button) where authorized users can
upload a `.env` file or enter key/value pairs manually. Stored secrets are listed
with a delete button. Changes propagate to all agents immediately.
