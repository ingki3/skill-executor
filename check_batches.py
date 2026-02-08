from src.services.batch_store import batch_store_service
import json

batches = batch_store_service.list_batches()
print(json.dumps([b.model_dump(mode='json') for b in batches], indent=2))
