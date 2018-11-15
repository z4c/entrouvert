#!/usr/bin/env python3

__author__ = "Zach D. LAMAZIERE <z@z4c.fr>"
__version__ = "0.1.0"
__license__ = "GNU GPL-3.0"

"""
Dans une idée de prévenir les situations de burnout des développeurs,
on voudrait produire un rapport reprenant par personne un taux de
travail "hors horaires", qu'on définirait comme le part de commits
qui sont réalisés le week-end ou avant 8h / après 20h.

L'exercice est donc l'écriture d'un script Python qui prendrait les
données du dépôt d'une de nos applications (prenons Passerelle :
https://git.entrouvert.org/passerelle.git) et afficherait ces taux.
"""


from logzero import logger
from os import path
from git import Repo
from pandas import DataFrame, to_datetime

GIT_REMOTE_URL = 'http://git.entrouvert.org/passerelle.git'
GIT_LOCAL_DIR = path.join(
    '/tmp',
    path.splitext(
        path.basename(GIT_REMOTE_URL)
    )[0]
)


def get_repo():
    """
    Gets a instance of gitpython
    """
    if path.exists(GIT_LOCAL_DIR):
        repo = Repo(GIT_LOCAL_DIR)
        logger.info("Pulling from %s" % GIT_LOCAL_DIR)
        repo.remotes.origin.pull()
        return repo

    logger.info("Cloning into %s" % GIT_LOCAL_DIR)
    return Repo.clone_from(GIT_REMOTE_URL, GIT_LOCAL_DIR)


def stdn(n):
    """
    Returns a standarized name
    """
    fn, *ln = n.split(' ')
    return "%s %s" % (
        fn.title(),
        ' '.join([_.upper() for _ in ln])
    )


def main():
    """ Main entry point of the app """

    r = get_repo()
    f = '%h;%at;%aN;%ae'
    #  https://git-scm.com/docs/pretty-formats#_pretty_formats

    # importing logs into a raw data frame
    rdf = DataFrame(
        [l.split(';') for l in r.git.log(format=f).split('\n')],
        columns=['hash', 'timestamp', 'name', 'email']
    )
    # parsing unix timestamp into datetime
    rdf['datetime'] = to_datetime(rdf.timestamp, unit='s')

    # Serghei seems to use multiple accounts...
    rdf['name'] = rdf.name.apply(stdn)

    # flag segregated commits:
    # (1) out of work hours or weekend (0) else.
    rdf['off'] = rdf['datetime'].map(
        lambda dt:
            dt.weekday() > 5
            or dt.hour < 8
            or dt.hour > 20
    ).astype(int)

    print(rdf.sort_values(['timestamp']))

    # group commits by theirs authors then aggregate 
    # flagged commits into a new data frame
    adf = rdf.groupby('name')['off'].agg(['sum', 'count'])

    # Remove contributers with less than 10 commits
    adf = adf[adf['count'] > 10]

    # Add taux de travail "hors horaires" as a new column
    adf['rate'] = adf['sum'] / adf['count']

    # Sort and print...
    adf = adf.sort_values(['rate'])
    print(
        adf.tail(10),
        "\n\nAnd our winner ... is ... \n\n",
        adf.iloc[-1]
    )


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
