alembic 1.12.1 A database migration tool for SQLAlchemy.
├── mako *
│   └── markupsafe >=0.9.2 
├── sqlalchemy >=1.3.0
│   ├── greenlet !=0.4.17 
│   └── typing-extensions >=4.2.0 
└── typing-extensions >=4
alpaca-trade-api 3.0.2 Alpaca API python client
├── aiohttp 3.8.2
│   ├── aiosignal >=1.1.2 
│   │   └── frozenlist >=1.1.0 
│   ├── async-timeout >=4.0.0a3,<5.0 
│   ├── attrs >=17.3.0 
│   ├── charset-normalizer >=2.0,<3.0 
│   ├── frozenlist >=1.1.1 (circular dependency aborted here)
│   ├── multidict >=4.5,<6.0 
│   └── yarl >=1.0,<2.0 
│       ├── idna >=2.0 
│       └── multidict >=4.0 (circular dependency aborted here)
├── deprecation 2.1.0
│   └── packaging * 
├── msgpack 1.0.3
├── numpy >=1.11.1
├── pandas >=0.18.1
│   ├── numpy >=1.23.2,<2 
│   ├── numpy >=1.26.0,<2 (circular dependency aborted here)
│   ├── python-dateutil >=2.8.2 
│   │   └── six >=1.5 
│   ├── pytz >=2020.1 
│   └── tzdata >=2022.1 
├── pyyaml 6.0
├── requests >2,<3
│   ├── certifi >=2017.4.17 
│   ├── charset-normalizer >=2,<4 
│   ├── idna >=2.5,<4 
│   └── urllib3 >=1.21.1,<3 
├── urllib3 >1.24,<2
├── websocket-client >=0.56.0,<2
└── websockets >=9.0,<11
asyncpg 0.29.0 An asyncio PostgreSQL driver
└── async-timeout >=4.0.3
beautifulsoup4 4.12.2 Screen-scraping library
└── soupsieve >1.2
black 23.11.0 The uncompromising code formatter.
├── click >=8.0.0
│   └── colorama * 
├── mypy-extensions >=0.4.3
├── packaging >=22.0
├── pathspec >=0.9.0
└── platformdirs >=2
ccxt 4.1.81 A JavaScript / TypeScript / Python / C# / PHP cryptocurrency trading library with support for 130+ exchanges
├── aiodns >=1.1.1
│   └── pycares >=4.0.0 
│       └── cffi >=1.5.0 
│           └── pycparser * 
├── aiohttp >=3.8
│   ├── aiosignal >=1.1.2 
│   │   └── frozenlist >=1.1.0 
│   ├── async-timeout >=4.0.0a3,<5.0 
│   ├── attrs >=17.3.0 
│   ├── charset-normalizer >=2.0,<3.0 
│   ├── frozenlist >=1.1.1 (circular dependency aborted here)
│   ├── multidict >=4.5,<6.0 
│   └── yarl >=1.0,<2.0 
│       ├── idna >=2.0 
│       └── multidict >=4.0 (circular dependency aborted here)
├── certifi >=2018.1.18
├── cryptography >=2.6.1
│   └── cffi >=1.12 
│       └── pycparser * 
├── requests >=2.18.4
│   ├── certifi >=2017.4.17 
│   ├── charset-normalizer >=2,<4 
│   ├── idna >=2.5,<4 
│   └── urllib3 >=1.21.1,<3 
├── setuptools >=60.9.0
├── typing-extensions >=4.4.0
└── yarl >=1.7.2
    ├── idna >=2.0 
    └── multidict >=4.0 
fastapi 0.104.1 FastAPI framework, high performance, easy to learn, fast to code, ready for production
├── anyio >=3.7.1,<4.0.0
│   ├── idna >=2.8 
│   └── sniffio >=1.1 
├── email-validator >=2.0.0
│   ├── dnspython >=2.0.0 
│   └── idna >=2.0.0 
├── httpx >=0.23.0
│   ├── anyio * 
│   │   ├── idna >=2.8 
│   │   └── sniffio >=1.1 
│   ├── certifi * 
│   ├── httpcore ==1.* 
│   │   ├── certifi * (circular dependency aborted here)
│   │   └── h11 >=0.13,<0.15 
│   ├── idna * (circular dependency aborted here)
│   └── sniffio * (circular dependency aborted here)
├── itsdangerous >=1.1.0
├── jinja2 >=2.11.2
│   └── markupsafe >=2.0 
├── orjson >=3.2.1
├── pydantic >=1.7.4,<1.8 || >1.8,<1.8.1 || >1.8.1,<2.0.0 || >2.0.0,<2.0.1 || >2.0.1,<2.1.0 || >2.1.0,<3.0.0
│   ├── annotated-types >=0.4.0 
│   ├── pydantic-core 2.14.5 
│   │   └── typing-extensions >=4.6.0,<4.7.0 || >4.7.0 
│   └── typing-extensions >=4.6.1 (circular dependency aborted here)
├── pydantic-extra-types >=2.0.0
│   └── pydantic >=2.0.3 
│       ├── annotated-types >=0.4.0 
│       ├── pydantic-core 2.14.5 
│       │   └── typing-extensions >=4.6.0,<4.7.0 || >4.7.0 
│       └── typing-extensions >=4.6.1 (circular dependency aborted here)
├── pydantic-settings >=2.0.0
│   ├── pydantic >=2.3.0 
│   │   ├── annotated-types >=0.4.0 
│   │   ├── pydantic-core 2.14.5 
│   │   │   └── typing-extensions >=4.6.0,<4.7.0 || >4.7.0 
│   │   └── typing-extensions >=4.6.1 (circular dependency aborted here)
│   └── python-dotenv >=0.21.0 
├── python-multipart >=0.0.5
├── pyyaml >=5.3.1
├── starlette >=0.27.0,<0.28.0
│   └── anyio >=3.4.0,<5 
│       ├── idna >=2.8 
│       └── sniffio >=1.1 
├── typing-extensions >=4.8.0
├── ujson >=4.0.1,<4.0.2 || >4.0.2,<4.1.0 || >4.1.0,<4.2.0 || >4.2.0,<4.3.0 || >4.3.0,<5.0.0 || >5.0.0,<5.1.0 || >5.1.0
└── uvicorn >=0.12.0
    ├── click >=7.0 
    │   └── colorama * 
    ├── colorama >=0.4 (circular dependency aborted here)
    ├── h11 >=0.8 
    ├── httptools >=0.5.0 
    ├── python-dotenv >=0.13 
    ├── pyyaml >=5.1 
    ├── uvloop >=0.14.0,<0.15.0 || >0.15.0,<0.15.1 || >0.15.1 
    ├── watchfiles >=0.13 
    │   └── anyio >=3.0.0 
    │       ├── idna >=2.8 
    │       └── sniffio >=1.1 
    └── websockets >=10.4 
jupyter 1.0.0 Jupyter metapackage. Install all the Jupyter components in one go.
├── ipykernel *
│   ├── appnope * 
│   ├── comm >=0.1.1 
│   │   └── traitlets >=4 
│   ├── debugpy >=1.6.5 
│   ├── ipython >=7.23.1 
│   │   ├── colorama * 
│   │   ├── decorator * 
│   │   ├── jedi >=0.16 
│   │   │   └── parso >=0.8.3,<0.9.0 
│   │   ├── matplotlib-inline * 
│   │   │   └── traitlets * (circular dependency aborted here)
│   │   ├── pexpect >4.3 
│   │   │   └── ptyprocess >=0.5 
│   │   ├── prompt-toolkit >=3.0.41,<3.1.0 
│   │   │   └── wcwidth * 
│   │   ├── pygments >=2.4.0 
│   │   ├── stack-data * 
│   │   │   ├── asttokens >=2.1.0 
│   │   │   │   └── six >=1.12.0 
│   │   │   ├── executing >=1.2.0 
│   │   │   └── pure-eval * 
│   │   └── traitlets >=5 (circular dependency aborted here)
│   ├── jupyter-client >=6.1.12 
│   │   ├── jupyter-core >=4.12,<5.0.dev0 || >=5.1.dev0 
│   │   │   ├── platformdirs >=2.5 
│   │   │   ├── pywin32 >=300 
│   │   │   └── traitlets >=5.3 (circular dependency aborted here)
│   │   ├── python-dateutil >=2.8.2 
│   │   │   └── six >=1.5 (circular dependency aborted here)
│   │   ├── pyzmq >=23.0 
│   │   │   └── cffi * 
│   │   │       └── pycparser * 
│   │   ├── tornado >=6.2 
│   │   └── traitlets >=5.3 (circular dependency aborted here)
│   ├── jupyter-core >=4.12,<5.0.dev0 || >=5.1.dev0 (circular dependency aborted here)
│   ├── matplotlib-inline >=0.1 (circular dependency aborted here)
│   ├── nest-asyncio * 
│   ├── packaging * 
│   ├── psutil * 
│   ├── pyzmq >=20 (circular dependency aborted here)
│   ├── tornado >=6.1 (circular dependency aborted here)
│   └── traitlets >=5.4.0 (circular dependency aborted here)
├── ipywidgets *
│   ├── comm >=0.1.3 
│   │   └── traitlets >=4 
│   ├── ipython >=6.1.0 
│   │   ├── colorama * 
│   │   ├── decorator * 
│   │   ├── jedi >=0.16 
│   │   │   └── parso >=0.8.3,<0.9.0 
│   │   ├── matplotlib-inline * 
│   │   │   └── traitlets * (circular dependency aborted here)
│   │   ├── pexpect >4.3 
│   │   │   └── ptyprocess >=0.5 
│   │   ├── prompt-toolkit >=3.0.41,<3.1.0 
│   │   │   └── wcwidth * 
│   │   ├── pygments >=2.4.0 
│   │   ├── stack-data * 
│   │   │   ├── asttokens >=2.1.0 
│   │   │   │   └── six >=1.12.0 
│   │   │   ├── executing >=1.2.0 
│   │   │   └── pure-eval * 
│   │   └── traitlets >=5 (circular dependency aborted here)
│   ├── jupyterlab-widgets >=3.0.9,<3.1.0 
│   ├── traitlets >=4.3.1 (circular dependency aborted here)
│   └── widgetsnbextension >=4.0.9,<4.1.0 
├── jupyter-console *
│   ├── ipykernel >=6.14 
│   │   ├── appnope * 
│   │   ├── comm >=0.1.1 
│   │   │   └── traitlets >=4 
│   │   ├── debugpy >=1.6.5 
│   │   ├── ipython >=7.23.1 
│   │   │   ├── colorama * 
│   │   │   ├── decorator * 
│   │   │   ├── jedi >=0.16 
│   │   │   │   └── parso >=0.8.3,<0.9.0 
│   │   │   ├── matplotlib-inline * 
│   │   │   │   └── traitlets * (circular dependency aborted here)
│   │   │   ├── pexpect >4.3 
│   │   │   │   └── ptyprocess >=0.5 
│   │   │   ├── prompt-toolkit >=3.0.41,<3.1.0 
│   │   │   │   └── wcwidth * 
│   │   │   ├── pygments >=2.4.0 
│   │   │   ├── stack-data * 
│   │   │   │   ├── asttokens >=2.1.0 
│   │   │   │   │   └── six >=1.12.0 
│   │   │   │   ├── executing >=1.2.0 
│   │   │   │   └── pure-eval * 
│   │   │   └── traitlets >=5 (circular dependency aborted here)
│   │   ├── jupyter-client >=6.1.12 
│   │   │   ├── jupyter-core >=4.12,<5.0.dev0 || >=5.1.dev0 
│   │   │   │   ├── platformdirs >=2.5 
│   │   │   │   ├── pywin32 >=300 
│   │   │   │   └── traitlets >=5.3 (circular dependency aborted here)
│   │   │   ├── python-dateutil >=2.8.2 
│   │   │   │   └── six >=1.5 (circular dependency aborted here)
│   │   │   ├── pyzmq >=23.0 
│   │   │   │   └── cffi * 
│   │   │   │       └── pycparser * 
│   │   │   ├── tornado >=6.2 
│   │   │   └── traitlets >=5.3 (circular dependency aborted here)
│   │   ├── jupyter-core >=4.12,<5.0.dev0 || >=5.1.dev0 (circular dependency aborted here)
│   │   ├── matplotlib-inline >=0.1 (circular dependency aborted here)
│   │   ├── nest-asyncio * 
│   │   ├── packaging * 
│   │   ├── psutil * 
│   │   ├── pyzmq >=20 (circular dependency aborted here)
│   │   ├── tornado >=6.1 (circular dependency aborted here)
│   │   └── traitlets >=5.4.0 (circular dependency aborted here)
│   ├── ipython * (circular dependency aborted here)
│   ├── jupyter-client >=7.0.0 (circular dependency aborted here)
│   ├── jupyter-core >=4.12,<5.0.dev0 || >=5.1.dev0 (circular dependency aborted here)
│   ├── prompt-toolkit >=3.0.30 (circular dependency aborted here)
│   ├── pygments * (circular dependency aborted here)
│   ├── pyzmq >=17 (circular dependency aborted here)
│   └── traitlets >=5.4 (circular dependency aborted here)
├── nbconvert *
│   ├── beautifulsoup4 * 
│   │   └── soupsieve >1.2 
│   ├── bleach !=5.0.0 
│   │   ├── six >=1.9.0 
│   │   └── webencodings * 
│   ├── defusedxml * 
│   ├── jinja2 >=3.0 
│   │   └── markupsafe >=2.0 
│   ├── jupyter-core >=4.7 
│   │   ├── platformdirs >=2.5 
│   │   ├── pywin32 >=300 
│   │   └── traitlets >=5.3 
│   ├── jupyterlab-pygments * 
│   ├── markupsafe >=2.0 (circular dependency aborted here)
│   ├── mistune >=2.0.3,<4 
│   ├── nbclient >=0.5.0 
│   │   ├── jupyter-client >=6.1.12 
│   │   │   ├── jupyter-core >=4.12,<5.0.dev0 || >=5.1.dev0 (circular dependency aborted here)
│   │   │   ├── python-dateutil >=2.8.2 
│   │   │   │   └── six >=1.5 (circular dependency aborted here)
│   │   │   ├── pyzmq >=23.0 
│   │   │   │   └── cffi * 
│   │   │   │       └── pycparser * 
│   │   │   ├── tornado >=6.2 
│   │   │   └── traitlets >=5.3 (circular dependency aborted here)
│   │   ├── jupyter-core >=4.12,<5.0.dev0 || >=5.1.dev0 (circular dependency aborted here)
│   │   ├── nbformat >=5.1 
│   │   │   ├── fastjsonschema * 
│   │   │   ├── jsonschema >=2.6 
│   │   │   │   ├── attrs >=22.2.0 
│   │   │   │   ├── fqdn * 
│   │   │   │   ├── idna * 
│   │   │   │   ├── isoduration * 
│   │   │   │   │   └── arrow >=0.15.0 
│   │   │   │   │       ├── python-dateutil >=2.7.0 (circular dependency aborted here)
│   │   │   │   │       └── types-python-dateutil >=2.8.10 
│   │   │   │   ├── jsonpointer >1.13 
│   │   │   │   ├── jsonschema-specifications >=2023.03.6 
│   │   │   │   │   └── referencing >=0.31.0 
│   │   │   │   │       ├── attrs >=22.2.0 (circular dependency aborted here)
│   │   │   │   │       └── rpds-py >=0.7.0 
│   │   │   │   ├── referencing >=0.28.4 (circular dependency aborted here)
│   │   │   │   ├── rfc3339-validator * 
│   │   │   │   │   └── six * (circular dependency aborted here)
│   │   │   │   ├── rfc3986-validator >0.1.0 
│   │   │   │   ├── rpds-py >=0.7.1 (circular dependency aborted here)
│   │   │   │   ├── uri-template * 
│   │   │   │   └── webcolors >=1.11 
│   │   │   ├── jupyter-core * (circular dependency aborted here)
│   │   │   └── traitlets >=5.1 (circular dependency aborted here)
│   │   └── traitlets >=5.4 (circular dependency aborted here)
│   ├── nbformat >=5.7 (circular dependency aborted here)
│   ├── packaging * 
│   ├── pandocfilters >=1.4.1 
│   ├── pygments >=2.4.1 
│   ├── tinycss2 * 
│   │   └── webencodings >=0.4 (circular dependency aborted here)
│   └── traitlets >=5.1 (circular dependency aborted here)
├── notebook *
│   ├── jupyter-server >=2.4.0,<3 
│   │   ├── anyio >=3.1.0 
│   │   │   ├── idna >=2.8 
│   │   │   └── sniffio >=1.1 
│   │   ├── argon2-cffi * 
│   │   │   └── argon2-cffi-bindings * 
│   │   │       └── cffi >=1.0.1 
│   │   │           └── pycparser * 
│   │   ├── jinja2 * 
│   │   │   └── markupsafe >=2.0 
│   │   ├── jupyter-client >=7.4.4 
│   │   │   ├── jupyter-core >=4.12,<5.0.dev0 || >=5.1.dev0 
│   │   │   │   ├── platformdirs >=2.5 
│   │   │   │   ├── pywin32 >=300 
│   │   │   │   └── traitlets >=5.3 
│   │   │   ├── python-dateutil >=2.8.2 
│   │   │   │   └── six >=1.5 
│   │   │   ├── pyzmq >=23.0 
│   │   │   │   └── cffi * (circular dependency aborted here)
│   │   │   ├── tornado >=6.2 
│   │   │   └── traitlets >=5.3 (circular dependency aborted here)
│   │   ├── jupyter-core >=4.12,<5.0.dev0 || >=5.1.dev0 (circular dependency aborted here)
│   │   ├── jupyter-events >=0.9.0 
│   │   │   ├── jsonschema >=4.18.0 
│   │   │   │   ├── attrs >=22.2.0 
│   │   │   │   ├── fqdn * 
│   │   │   │   ├── idna * (circular dependency aborted here)
│   │   │   │   ├── isoduration * 
│   │   │   │   │   └── arrow >=0.15.0 
│   │   │   │   │       ├── python-dateutil >=2.7.0 (circular dependency aborted here)
│   │   │   │   │       └── types-python-dateutil >=2.8.10 
│   │   │   │   ├── jsonpointer >1.13 
│   │   │   │   ├── jsonschema-specifications >=2023.03.6 
│   │   │   │   │   └── referencing >=0.31.0 
│   │   │   │   │       ├── attrs >=22.2.0 (circular dependency aborted here)
│   │   │   │   │       └── rpds-py >=0.7.0 
│   │   │   │   ├── referencing >=0.28.4 (circular dependency aborted here)
│   │   │   │   ├── rfc3339-validator * 
│   │   │   │   │   └── six * (circular dependency aborted here)
│   │   │   │   ├── rfc3986-validator >0.1.0 
│   │   │   │   ├── rpds-py >=0.7.1 (circular dependency aborted here)
│   │   │   │   ├── uri-template * 
│   │   │   │   └── webcolors >=1.11 
│   │   │   ├── python-json-logger >=2.0.4 
│   │   │   ├── pyyaml >=5.3 
│   │   │   ├── referencing * (circular dependency aborted here)
│   │   │   ├── rfc3339-validator * (circular dependency aborted here)
│   │   │   ├── rfc3986-validator >=0.1.1 (circular dependency aborted here)
│   │   │   └── traitlets >=5.3 (circular dependency aborted here)
│   │   ├── jupyter-server-terminals * 
│   │   │   ├── pywinpty >=2.0.3 
│   │   │   └── terminado >=0.8.3 
│   │   │       ├── ptyprocess * 
│   │   │       ├── pywinpty >=1.1.0 (circular dependency aborted here)
│   │   │       └── tornado >=6.1.0 (circular dependency aborted here)
│   │   ├── nbconvert >=6.4.4 
│   │   │   ├── beautifulsoup4 * 
│   │   │   │   └── soupsieve >1.2 
│   │   │   ├── bleach !=5.0.0 
│   │   │   │   ├── six >=1.9.0 (circular dependency aborted here)
│   │   │   │   └── webencodings * 
│   │   │   ├── defusedxml * 
│   │   │   ├── jinja2 >=3.0 (circular dependency aborted here)
│   │   │   ├── jupyter-core >=4.7 (circular dependency aborted here)
│   │   │   ├── jupyterlab-pygments * 
│   │   │   ├── markupsafe >=2.0 (circular dependency aborted here)
│   │   │   ├── mistune >=2.0.3,<4 
│   │   │   ├── nbclient >=0.5.0 
│   │   │   │   ├── jupyter-client >=6.1.12 (circular dependency aborted here)
│   │   │   │   ├── jupyter-core >=4.12,<5.0.dev0 || >=5.1.dev0 (circular dependency aborted here)
│   │   │   │   ├── nbformat >=5.1 
│   │   │   │   │   ├── fastjsonschema * 
│   │   │   │   │   ├── jsonschema >=2.6 (circular dependency aborted here)
│   │   │   │   │   ├── jupyter-core * (circular dependency aborted here)
│   │   │   │   │   └── traitlets >=5.1 (circular dependency aborted here)
│   │   │   │   └── traitlets >=5.4 (circular dependency aborted here)
│   │   │   ├── nbformat >=5.7 (circular dependency aborted here)
│   │   │   ├── packaging * 
│   │   │   ├── pandocfilters >=1.4.1 
│   │   │   ├── pygments >=2.4.1 
│   │   │   ├── tinycss2 * 
│   │   │   │   └── webencodings >=0.4 (circular dependency aborted here)
│   │   │   └── traitlets >=5.1 (circular dependency aborted here)
│   │   ├── nbformat >=5.3.0 (circular dependency aborted here)
│   │   ├── overrides * 
│   │   ├── packaging * (circular dependency aborted here)
│   │   ├── prometheus-client * 
│   │   ├── pywinpty * (circular dependency aborted here)
│   │   ├── pyzmq >=24 (circular dependency aborted here)
│   │   ├── send2trash >=1.8.2 
│   │   ├── terminado >=0.8.3 (circular dependency aborted here)
│   │   ├── tornado >=6.2.0 (circular dependency aborted here)
│   │   ├── traitlets >=5.6.0 (circular dependency aborted here)
│   │   └── websocket-client * 
│   ├── jupyterlab >=4.0.2,<5 
│   │   ├── async-lru >=1.0.0 
│   │   ├── ipykernel * 
│   │   │   ├── appnope * 
│   │   │   ├── comm >=0.1.1 
│   │   │   │   └── traitlets >=4 (circular dependency aborted here)
│   │   │   ├── debugpy >=1.6.5 
│   │   │   ├── ipython >=7.23.1 
│   │   │   │   ├── colorama * 
│   │   │   │   ├── decorator * 
│   │   │   │   ├── jedi >=0.16 
│   │   │   │   │   └── parso >=0.8.3,<0.9.0 
│   │   │   │   ├── matplotlib-inline * 
│   │   │   │   │   └── traitlets * (circular dependency aborted here)
│   │   │   │   ├── pexpect >4.3 
│   │   │   │   │   └── ptyprocess >=0.5 (circular dependency aborted here)
│   │   │   │   ├── prompt-toolkit >=3.0.41,<3.1.0 
│   │   │   │   │   └── wcwidth * 
│   │   │   │   ├── pygments >=2.4.0 (circular dependency aborted here)
│   │   │   │   ├── stack-data * 
│   │   │   │   │   ├── asttokens >=2.1.0 
│   │   │   │   │   │   └── six >=1.12.0 (circular dependency aborted here)
│   │   │   │   │   ├── executing >=1.2.0 
│   │   │   │   │   └── pure-eval * 
│   │   │   │   └── traitlets >=5 (circular dependency aborted here)
│   │   │   ├── jupyter-client >=6.1.12 (circular dependency aborted here)
│   │   │   ├── jupyter-core >=4.12,<5.0.dev0 || >=5.1.dev0 (circular dependency aborted here)
│   │   │   ├── matplotlib-inline >=0.1 (circular dependency aborted here)
│   │   │   ├── nest-asyncio * 
│   │   │   ├── packaging * (circular dependency aborted here)
│   │   │   ├── psutil * 
│   │   │   ├── pyzmq >=20 (circular dependency aborted here)
│   │   │   ├── tornado >=6.1 (circular dependency aborted here)
│   │   │   └── traitlets >=5.4.0 (circular dependency aborted here)
│   │   ├── jinja2 >=3.0.3 (circular dependency aborted here)
│   │   ├── jupyter-core * (circular dependency aborted here)
│   │   ├── jupyter-lsp >=2.0.0 
│   │   │   └── jupyter-server >=1.1.2 (circular dependency aborted here)
│   │   ├── jupyter-server >=2.4.0,<3 (circular dependency aborted here)
│   │   ├── jupyterlab-server >=2.19.0,<3 
│   │   │   ├── babel >=2.10 
│   │   │   │   └── setuptools * 
│   │   │   ├── jinja2 >=3.0.3 (circular dependency aborted here)
│   │   │   ├── json5 >=0.9.0 
│   │   │   ├── jsonschema >=4.18.0 (circular dependency aborted here)
│   │   │   ├── jupyter-server >=1.21,<3 (circular dependency aborted here)
│   │   │   ├── packaging >=21.3 (circular dependency aborted here)
│   │   │   └── requests >=2.31 
│   │   │       ├── certifi >=2017.4.17 
│   │   │       ├── charset-normalizer >=2,<4 
│   │   │       ├── idna >=2.5,<4 (circular dependency aborted here)
│   │   │       └── urllib3 >=1.21.1,<3 
│   │   ├── notebook-shim >=0.2 
│   │   │   └── jupyter-server >=1.8,<3 (circular dependency aborted here)
│   │   ├── packaging * (circular dependency aborted here)
│   │   ├── tornado >=6.2.0 (circular dependency aborted here)
│   │   └── traitlets * (circular dependency aborted here)
│   ├── jupyterlab-server >=2.22.1,<3 (circular dependency aborted here)
│   ├── notebook-shim >=0.2,<0.3 (circular dependency aborted here)
│   └── tornado >=6.2.0 (circular dependency aborted here)
└── qtconsole *
    ├── ipykernel >=4.1 
    │   ├── appnope * 
    │   ├── comm >=0.1.1 
    │   │   └── traitlets >=4 
    │   ├── debugpy >=1.6.5 
    │   ├── ipython >=7.23.1 
    │   │   ├── colorama * 
    │   │   ├── decorator * 
    │   │   ├── jedi >=0.16 
    │   │   │   └── parso >=0.8.3,<0.9.0 
    │   │   ├── matplotlib-inline * 
    │   │   │   └── traitlets * (circular dependency aborted here)
    │   │   ├── pexpect >4.3 
    │   │   │   └── ptyprocess >=0.5 
    │   │   ├── prompt-toolkit >=3.0.41,<3.1.0 
    │   │   │   └── wcwidth * 
    │   │   ├── pygments >=2.4.0 
    │   │   ├── stack-data * 
    │   │   │   ├── asttokens >=2.1.0 
    │   │   │   │   └── six >=1.12.0 
    │   │   │   ├── executing >=1.2.0 
    │   │   │   └── pure-eval * 
    │   │   └── traitlets >=5 (circular dependency aborted here)
    │   ├── jupyter-client >=6.1.12 
    │   │   ├── jupyter-core >=4.12,<5.0.dev0 || >=5.1.dev0 
    │   │   │   ├── platformdirs >=2.5 
    │   │   │   ├── pywin32 >=300 
    │   │   │   └── traitlets >=5.3 (circular dependency aborted here)
    │   │   ├── python-dateutil >=2.8.2 
    │   │   │   └── six >=1.5 (circular dependency aborted here)
    │   │   ├── pyzmq >=23.0 
    │   │   │   └── cffi * 
    │   │   │       └── pycparser * 
    │   │   ├── tornado >=6.2 
    │   │   └── traitlets >=5.3 (circular dependency aborted here)
    │   ├── jupyter-core >=4.12,<5.0.dev0 || >=5.1.dev0 (circular dependency aborted here)
    │   ├── matplotlib-inline >=0.1 (circular dependency aborted here)
    │   ├── nest-asyncio * 
    │   ├── packaging * 
    │   ├── psutil * 
    │   ├── pyzmq >=20 (circular dependency aborted here)
    │   ├── tornado >=6.1 (circular dependency aborted here)
    │   └── traitlets >=5.4.0 (circular dependency aborted here)
    ├── jupyter-client >=4.1 (circular dependency aborted here)
    ├── jupyter-core * (circular dependency aborted here)
    ├── packaging * (circular dependency aborted here)
    ├── pygments * (circular dependency aborted here)
    ├── pyzmq >=17.1 (circular dependency aborted here)
    ├── qtpy >=2.4.0 
    │   └── packaging * (circular dependency aborted here)
    └── traitlets <5.2.1 || >5.2.1,<5.2.2 || >5.2.2 (circular dependency aborted here)
lean 1.0.175 A CLI aimed at making it easier to run QuantConnect's LEAN engine locally and in the cloud
├── click >=8.0.4
│   └── colorama * 
├── cryptography >=41.0.4,<41.1.0
│   └── cffi >=1.12 
│       └── pycparser * 
├── docker >=6.0.0
│   ├── packaging >=14.0 
│   ├── pywin32 >=304 
│   ├── requests >=2.26.0 
│   │   ├── certifi >=2017.4.17 
│   │   ├── charset-normalizer >=2,<4 
│   │   ├── idna >=2.5,<4 
│   │   └── urllib3 >=1.21.1,<3 
│   ├── urllib3 >=1.26.0 (circular dependency aborted here)
│   └── websocket-client >=0.32.0 
├── joblib >=1.1.0
├── json5 >=0.9.8
├── lxml >=4.9.0
├── maskpass >=0.3.6
│   └── pynput * 
│       ├── evdev >=1.3 
│       ├── pyobjc-framework-applicationservices >=8.0 
│       │   ├── pyobjc-core >=10.0 
│       │   ├── pyobjc-framework-cocoa >=10.0 
│       │   │   └── pyobjc-core >=10.0 (circular dependency aborted here)
│       │   └── pyobjc-framework-quartz >=10.0 
│       │       ├── pyobjc-core >=10.0 (circular dependency aborted here)
│       │       └── pyobjc-framework-cocoa >=10.0 (circular dependency aborted here)
│       ├── pyobjc-framework-quartz >=8.0 (circular dependency aborted here)
│       ├── python-xlib >=0.17 
│       │   └── six >=1.10.0 
│       └── six * (circular dependency aborted here)
├── pydantic >=1.8.2
│   ├── annotated-types >=0.4.0 
│   ├── pydantic-core 2.14.5 
│   │   └── typing-extensions >=4.6.0,<4.7.0 || >4.7.0 
│   └── typing-extensions >=4.6.1 (circular dependency aborted here)
├── python-dateutil >=2.8.2
│   └── six >=1.5 
├── quantconnect-stubs >=16066
│   ├── matplotlib >=3.7.3 
│   │   ├── contourpy >=1.0.1 
│   │   │   └── numpy >=1.20,<2.0 
│   │   ├── cycler >=0.10 
│   │   ├── fonttools >=4.22.0 
│   │   ├── kiwisolver >=1.3.1 
│   │   ├── numpy >=1.21,<2 (circular dependency aborted here)
│   │   ├── packaging >=20.0 
│   │   ├── pillow >=8 
│   │   ├── pyparsing >=2.3.1 
│   │   └── python-dateutil >=2.7 
│   │       └── six >=1.5 
│   └── pandas >=1.5.3 
│       ├── numpy >=1.23.2,<2 (circular dependency aborted here)
│       ├── numpy >=1.26.0,<2 (circular dependency aborted here)
│       ├── python-dateutil >=2.8.2 (circular dependency aborted here)
│       ├── pytz >=2020.1 
│       └── tzdata >=2022.1 
├── requests >=2.27.1
│   ├── certifi >=2017.4.17 
│   ├── charset-normalizer >=2,<4 
│   ├── idna >=2.5,<4 
│   └── urllib3 >=1.21.1,<3 
├── rich >=9.10.0
│   ├── markdown-it-py >=2.2.0 
│   │   └── mdurl >=0.1,<1.0 
│   └── pygments >=2.13.0,<3.0.0 
├── setuptools *
└── wrapt >=1.14.1,<1.15.0
polygon-api-client 1.13.3 Official Polygon.io REST and Websocket client.
├── certifi >=2022.5.18,<2024.0.0
├── urllib3 >=1.26.9,<2.0.0
└── websockets >=10.3,<13.0
psycopg2 2.9.9 psycopg2 - Python-PostgreSQL Database Adapter
psycopg2-binary 2.9.9 psycopg2 - Python-PostgreSQL Database Adapter
ptvsd 4.3.2 Remote debugging server for Python support in Visual Studio and Visual Studio Code
pydantic 2.5.2 Data validation using Python type hints
├── annotated-types >=0.4.0
├── pydantic-core 2.14.5
│   └── typing-extensions >=4.6.0,<4.7.0 || >4.7.0 
└── typing-extensions >=4.6.1
pydantic-settings 2.1.0 Settings management using Pydantic
├── pydantic >=2.3.0
│   ├── annotated-types >=0.4.0 
│   ├── pydantic-core 2.14.5 
│   │   └── typing-extensions >=4.6.0,<4.7.0 || >4.7.0 
│   └── typing-extensions >=4.6.1 (circular dependency aborted here)
└── python-dotenv >=0.21.0
pydevd-pycharm 233.11799.259 PyCharm Debugger (used in PyCharm and PyDev)
quantconnect-stubs 16075 Type stubs for QuantConnect's Lean
├── matplotlib >=3.7.3
│   ├── contourpy >=1.0.1 
│   │   └── numpy >=1.20,<2.0 
│   ├── cycler >=0.10 
│   ├── fonttools >=4.22.0 
│   ├── kiwisolver >=1.3.1 
│   ├── numpy >=1.21,<2 (circular dependency aborted here)
│   ├── packaging >=20.0 
│   ├── pillow >=8 
│   ├── pyparsing >=2.3.1 
│   └── python-dateutil >=2.7 
│       └── six >=1.5 
└── pandas >=1.5.3
    ├── numpy >=1.23.2,<2 
    ├── numpy >=1.26.0,<2 (circular dependency aborted here)
    ├── python-dateutil >=2.8.2 
    │   └── six >=1.5 
    ├── pytz >=2020.1 
    └── tzdata >=2022.1 
sqlalchemy 2.0.23 Database Abstraction Library
├── greenlet !=0.4.17
└── typing-extensions >=4.2.0
tqdm 4.66.1 Fast, Extensible Progress Meter
└── colorama *
tulipy 0.4.0 Financial Technical Analysis Indicator Library. Python bindings for https://github.com/TulipCharts/tulipindicators
└── numpy *
yahoo-fin 0.8.9.1 Download historical stock prices (daily / weekly / monthly), realtime-prices, fundamentals data, income statements, cash flows, analyst info, current cryptocurrency prices, option chains, earnings history, and more with yahoo_fin.
├── feedparser *
│   └── sgmllib3k * 
├── pandas *
│   ├── numpy >=1.23.2,<2 
│   ├── numpy >=1.26.0,<2 (circular dependency aborted here)
│   ├── python-dateutil >=2.8.2 
│   │   └── six >=1.5 
│   ├── pytz >=2020.1 
│   └── tzdata >=2022.1 
├── requests *
│   ├── certifi >=2017.4.17 
│   ├── charset-normalizer >=2,<4 
│   ├── idna >=2.5,<4 
│   └── urllib3 >=1.21.1,<3 
└── requests-html *
    ├── bs4 * 
    │   └── beautifulsoup4 * 
    │       └── soupsieve >1.2 
    ├── fake-useragent * 
    ├── parse * 
    ├── pyppeteer >=0.0.14 
    │   ├── appdirs >=1.4.3,<2.0.0 
    │   ├── certifi >=2021 
    │   ├── importlib-metadata >=1.4 
    │   │   └── zipp >=0.5 
    │   ├── pyee >=8.1.0,<9.0.0 
    │   ├── tqdm >=4.42.1,<5.0.0 
    │   │   └── colorama * 
    │   ├── urllib3 >=1.25.8,<2.0.0 
    │   └── websockets >=10.0,<11.0 
    ├── pyquery * 
    │   ├── cssselect >=1.2.0 
    │   └── lxml >=2.1 
    ├── requests * 
    │   ├── certifi >=2017.4.17 (circular dependency aborted here)
    │   ├── charset-normalizer >=2,<4 
    │   ├── idna >=2.5,<4 
    │   └── urllib3 >=1.21.1,<3 (circular dependency aborted here)
    └── w3lib * 
