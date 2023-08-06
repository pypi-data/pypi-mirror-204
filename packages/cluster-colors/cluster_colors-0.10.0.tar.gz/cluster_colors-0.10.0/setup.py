# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cluster_colors']

package_data = \
{'': ['*']}

install_requires = \
['colormath>=3.0.0,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'paragraphs>=0.2.0,<0.3.0',
 'stacked-quantile>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'cluster-colors',
    'version': '0.10.0',
    'description': 'Cluster color vectors with kmedians',
    'long_description': 'Divisive (but not hierarchical) clustering.\n\nSlow, but clustering exactly how I want it. Iteratively split cluster with highest SSE. Splits are used to find new exemplars, which are thrown into k-medians with existing exemplars. Takes pretty extreme measures to avoid not only non-determinism but also non-arbitrary-ism:\n\n* a Supercluster instance, when asked to split, will split the cluster with the highest SSE. If there is a tie, the Clusters instance will not arbitrarily decide between the tied clusters, but will instead split all clusters tied for max SSE. This means there is a small chance you will not be able to split a group of colors into exactly n clusters.\n* delta-e is non-commutative, so delta-e is computed *twice* for each distance (a -> b and b -> a). The maximum of these two is used. This doubles the time of an already slow calculation, but delta-e is only used for distances between clusters, and this module is designed to work with small numbers of clusters (Agglomerative clustering may be a better bet if you want to use small clusters.)\n\nAdvantages:\n* finds big clusters\n* deterministic and non-arbitrary\n* robust to outliers\n* fast for what it is, can easily split a few thousand members into a small number of clusters\n* decisions made early on do not effect the result as much as they would in true hierarchical clustering\n* has strategies to avoid ties or arbitrary (even if deterministic) decisions with small member sets. This is important when dealing with questions like "which of these five colors is most unlike the others?"\n\nDisadvantages:\n* child clusters will not necessarily contain (or only contain) the members of the parent, so this is not hierarchical, though you can "merge" split clusters by regressing to previous states.\n* sloooows down as the number of clusters grows, not the best way to de-cluster all the way back to constituent members.\n* uses Euclidean distance (sum squared error) for many steps. Delta e is used for final splitting criteria.\n\nThis clustering is designed for questions like "what are the five dominant colors in this image (respecting transparency)?"\n\n## Three large steps in the background\n\n### Average colors by n-bit representation\n\n`pool_colors`: reduce 8-bit image colors (potentially 16_777_216 colors) to a maximum of 262_144 by averaging. The ouput of `pool_colors` will also contain a weight axis for each color, representing the combined opacity of all pixels of that color.\n\n### Median cut along longest axis\n\n`cut_colors`: reduce colors to around 512 by recursively splitting along longest axis (longest actual axis. Not constrained to x, y, or, z axes).\n\n### k-medians clustering\n\n`KMedSupercluster`: split and merge (undo split) clusters.\n\n* start with one cluster with 100 members\n* split this cluster recursively into five clusters (30, 30, 20, 10, 10)\n* ask for the largest cluster, and there\'s a tie\n* KMedSupercluster will recursively unsplit clusters until all ties are broken. This will *rarely* be needed.\n\n\n## Installation\n\n    pip install cluster_colors\n\n## Basic usage\n\n~~~python\nfrom cluster_colors import get_image_clusters\n\nclusters = get_image_clusters(image_filename) # one cluster at this point\nclusters.split_to_delta_e(16)\nsplit_clusters = clusters.get_rsorted_clusters()\n\ncolors: list[tuple[float, float, float]] = [c.exemplar for c in split_clusters]\n\n# to save the cluster exemplars as an image file\n\nshow_clusters(split_clusters, "open_file_to_see_clusters")\n~~~\n',
    'author': 'Shay Hill',
    'author_email': 'shay_public@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
