"""Read the instructions file from Cloud Storage.

The file is fetched on every request so that updating it in the bucket takes effect
without redeploying. If the bucket/object is missing or GCS is unreachable, the
read is skipped (logged as WARNING) and Sage falls back to answering without
extra instructions, the same way Firestore/BigQuery are optional.
"""

import logging

from google.api_core.exceptions import GoogleAPICallError
from google.cloud import storage

log = logging.getLogger(__name__)

_INSTRUCTIONS_BLOB = "istruzioni.md"


def read_instructions(bucket_name: str, blob_name: str = _INSTRUCTIONS_BLOB) -> str | None:
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        if not blob.exists():
            log.warning("File istruzioni non trovato: gs://%s/%s", bucket_name, blob_name)
            return None
        return blob.download_as_text(encoding="utf-8")
    except (GoogleAPICallError, Exception) as exc:  # noqa: BLE001
        log.warning("Impossibile leggere le istruzioni da GCS: %s", exc)
        return None
