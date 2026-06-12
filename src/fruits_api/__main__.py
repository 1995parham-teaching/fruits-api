"""Entry point allowing ``python -m fruits_api`` and the ``fruits-api`` script."""

from __future__ import annotations

import os

import uvicorn


def main() -> None:
    """Run the API with uvicorn, honoring HOST/PORT environment variables."""
    uvicorn.run(
        "fruits_api.main:app",
        host=os.environ.get("HOST", "0.0.0.0"),  # noqa: S104 - intended in a container
        port=int(os.environ.get("PORT", "8000")),
    )


if __name__ == "__main__":
    main()
