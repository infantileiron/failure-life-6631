from src.services import rule as service
def list_items():return service.list_rules()
def create(data):return service.create(data)
