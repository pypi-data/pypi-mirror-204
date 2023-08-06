# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ultima_scraper_collection',
 'ultima_scraper_collection.managers',
 'ultima_scraper_collection.managers.database_manager',
 'ultima_scraper_collection.managers.database_manager.connections',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.databases.user_data.migration',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.databases.user_data.migration.alembic',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.databases.user_data.migration.alembic.versions',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.legacy_databases',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.legacy_databases.messages',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.legacy_databases.messages.migration',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.legacy_databases.messages.migration.alembic',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.legacy_databases.messages.migration.alembic.versions',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.legacy_databases.posts.migration',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.legacy_databases.posts.migration.alembic',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.legacy_databases.posts.migration.alembic.versions',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.legacy_databases.stories.migration',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.legacy_databases.stories.migration.alembic',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.legacy_databases.stories.migration.alembic.versions',
 'ultima_scraper_collection.managers.database_manager.connections.sqlite.models',
 'ultima_scraper_collection.managers.datascraper_manager',
 'ultima_scraper_collection.managers.datascraper_manager.datascrapers',
 'ultima_scraper_collection.managers.metadata_manager',
 'ultima_scraper_collection.modules']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.9.2,<2.0.0',
 'psycopg2>=2.9.5,<3.0.0',
 'sqlalchemy>=2.0.1,<3.0.0',
 'tqdm>=4.65.0,<5.0.0',
 'ultima-scraper-api>=1.0.0,<2.0.0',
 'ultima-scraper-renamer>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'ultima-scraper-collection',
    'version': '1.0.3',
    'description': '',
    'long_description': 'None',
    'author': 'DIGITALCRIMINALS',
    'author_email': '89371864+digitalcriminals@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
