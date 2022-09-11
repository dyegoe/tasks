from invoke import Collection
from . import search

# Create Collection
ns = Collection("aws")
ns.add_collection(search)
