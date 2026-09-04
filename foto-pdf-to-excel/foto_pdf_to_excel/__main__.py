"""``python -m foto_pdf_to_excel ...`` ile doğrudan çalıştırma desteği."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
