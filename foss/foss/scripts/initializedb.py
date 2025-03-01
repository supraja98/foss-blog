import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import MyModel
from ..models import User
from ..models import Comment
from ..models import Count
from ..models import Total

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
       # model = Count(name='supraja@gmail.com', count=0 , topic='')
       # dbsession.add(model)

       # model = MyModel(name='one', value=1)
       # dbsession.add(model)
       # model = Comment(email = 'supraja@gmail.com', topic = 'Linux Distributions' , comment = 'Good!' , datetime = '2017-08-24 20:30:45')
       # dbsession.add(model)
      
       

