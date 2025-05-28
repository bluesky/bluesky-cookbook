
# This is equiavalent to 'tiled server catalog --temp --api-key=secret' on a thread.
# TODO Provide in tiled a more succinct way to do this.

import tempfile
import uvicorn
from pathlib import Path
from tiled.catalog import from_uri as catalog_from_uri
from tiled.server.app import build_app
# TODO Expose this publicly in Tiled.
from tiled._tests.test_server import Server

temp_directory = Path(tempfile.TemporaryDirectory().name)
temp_directory.mkdir()
catalog = catalog_from_uri(
    temp_directory / "catalog.db",
    writable_storage=temp_directory / "data",
    init_if_not_exists=True,
)
app = build_app(catalog, authentication={"single_user_api_key": "secret"})
server = Server(uvicorn.Config(app, port=8000))
server.run_in_thread()
