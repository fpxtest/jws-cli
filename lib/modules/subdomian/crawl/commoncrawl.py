#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
作者：jammny
文件描述：
"""
import time

import cdx_toolkit

from lib.config.logger import logger
from lib.utils.format import match_subdomains


class CommonCrawl:
    def __init__(self, domain):
        self.domain = domain
        self.results = set()

    def get_domain(self):
        """

        :return:
        """
        cdx = cdx_toolkit.CDXFetcher(source='cc')
        url = f'*.{self.domain}/*'
        logger.debug(url, 'size estimate', cdx.get_size_estimate(url))
        for resp in cdx.iter(url, limit=50):
            if resp.data.get('status') not in ['301', '302']:
                # url = resp.data.get('url')
                # print(url + resp.text)
                res = match_subdomains(self.domain, resp.text)
                self.results.update(res)

    def run(self):
        logger.info("Running CommonCrawl...")
        s = time.time()
        self.get_domain()
        results = list(self.results)
        e = time.time()
        if results:
            logger.info(f"CommonCrawl：{len(results)} results found!")
            logger.debug(f"CommonCrawl：{results}")
            logger.debug(f"{e-s}")
        return results


if __name__ == '__main__':
    CommonCrawl("archive-it.org").run()
