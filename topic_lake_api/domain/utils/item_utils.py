from topic_lake_api.domain.interfaces.repositories import IItemsRepository


def determine_rank(items_repository: IItemsRepository, requested_rank: int, topic_id: int) -> int:
    max_rank = items_repository.get_max_rank(topic_id)
    return min(requested_rank, max_rank + 1)
