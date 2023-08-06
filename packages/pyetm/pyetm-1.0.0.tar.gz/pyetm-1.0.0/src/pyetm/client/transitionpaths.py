"""transition paths"""
from __future__ import annotations

import math
import pandas as pd

from pyetm.logger import get_modulelogger
from .session import SessionMethods
from .header import HeaderMethods

logger = get_modulelogger(__name__)

# assign additional methods to custom class for mycmodel.
# makes it possible to assign transition path id as well.

class TransitionPathMethods(HeaderMethods, SessionMethods):
    """saved scenario related functions"""

    @property
    def transition_path(self):
        pass

    @property
    def transition_path_id(self):
        pass

    @property
    def my_transition_paths(self):
        """all transition paths connector to account"""

        # set url
        url = 'transition_paths'

        # determine number of pages
        pages = self._get_scenarios(url, page=1, limit=1)
        pages = math.ceil(pages['meta']['total'] / 25)

        if pages == 0:
            return pd.DataFrame()

        # newlist
        scenarios = []
        for page in range(pages):

            # fetch pages and format scenarios
            recs = self._get_scenarios(url, page=page)['data']

            excl = []
            scenarios.extend([
                self._format_scenario(scen, excl) for scen in recs])

        return pd.DataFrame.from_records(scenarios, index='id')

    def create_transition_path(self, title: str, scenario_ids: list[str]):
        """create transition path"""

        # transforms scenario ids to integers
        scenario_ids = [int(sid) for sid in scenario_ids]

        # set data
        data = {
            'title': str(title),
            'scenario_ids': scenario_ids
        }

        # prepare request
        url = 'transition_paths'
        headers = {'content-type': 'application/json'}

        # make request
        resp = self.session.post(
            url, decoder='json', json=data, headers=headers)

        return resp.get('id')

    def delete_transition_path(self, transition_path_id: str | None = None):
        """delete transition path"""

        url = f'transition_paths/{transition_path_id}'
        self.session.delete(url)

    def to_transition_path(self, transition_path_id: str | None = None):
        """update transition path"""
        pass
