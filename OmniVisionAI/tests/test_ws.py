import pytest


@pytest.mark.asyncio
async def test_consumer_imports():
    # Basic sanity import test; full Channels tests require channels testing client
    from core.consumers import CameraStreamConsumer

    assert hasattr(CameraStreamConsumer, 'connect')
    assert hasattr(CameraStreamConsumer, 'receive')

