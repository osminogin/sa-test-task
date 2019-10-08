import pytest

from speechanalytics_api import build_app


@pytest.fixture
def auth():
    encoded_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.19X7kKD-m0ImEdCIeDzitU10IQLQIhTkGA55FOaLUhs'
    return {'Authorization': f'Bearer {encoded_token}'}


@pytest.fixture(scope='function')
async def async_client(aiohttp_client):
    return await aiohttp_client(build_app)
