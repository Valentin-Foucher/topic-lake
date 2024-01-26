from topic_lake_api.interactor.interfaces.repositories.items import IItemsRepository


async def determine_rank(items_repository: IItemsRepository, requested_rank: int, topic_id: int) -> int:
    max_rank = await items_repository.get_max_rank(topic_id)
    return min(requested_rank, max_rank + 1)
