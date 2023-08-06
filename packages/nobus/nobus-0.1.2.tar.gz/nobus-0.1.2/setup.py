# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nobus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nobus',
    'version': '0.1.2',
    'description': '',
    'long_description': '# nobus\n"Nobody But Us" modules for Python\n\n## What is nobus\n[NOBUS（Nobody But Us）](https://en.wikipedia.org/wiki/NOBUS)は「我々（United States）だけが利用できる脆弱性」を意味するアメリカ国家安全保証局（NSA）の標語です。\n\n`nobus` モジュールはごく一部の変人しか使わないであろう、Python の特殊メソッドをフル活用したクラスハッキングを詰め込んだモジュールです。\n\n現在は Python のクラスアトリビュートに対して型チェックと immutable / protected 属性を追加する `safeattr` モジュールが実装されています。\n\nそのうち関数型プログラミングモジュールの `kette` を統合する予定です。\n\n本当に暇なときしか整備できないのでドキュメントはそのうち整備します。基本的に Zenn の記事をドキュメント代わりにしてください。\n\n* Zenn: [Josh Nobus (@wsuzume)](https://zenn.dev/wsuzume)\n* Twitter: [@wsuzume](https://twitter.com/wsuzume)\n\n## Usage\n```\n$ pip install nobus\n```\n',
    'author': 'Josh Nobus',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
