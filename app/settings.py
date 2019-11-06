"""This module defines the scrapy settings"""

from scrapy.settings import Settings


class WebsiteSettings(Settings):

    """
    Defining the settings for the scraper
    """

    @staticmethod
    def generate_settings_dict(file_location):

        """
        Generating the settings dictionary
        :param file_location: string to temporary file location
        :return: settings_dict: dict detailing settings
        """

        settings_dict = {

            'FEED_FORMAT': 'json',
            'FEED_URI': file_location,
            'DOWNLOAD_MAXSIZE': 100000,
            'COOKIES_ENABLED': False,
            'RETRY_ENABLED': False,
            'DOWNLOAD_TIMEOUT': 15,
            'AUTOTHROTTLE_ENABLED': True,
            'AUTOTHROTTLE_TARGET_CONCURRENCY': 10,
            'LOG_LEVEL': 'CRITICAL',
            'DEPTH_LIMIT': 1,
            'DEPTH_PRIORITY': 1,
            'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
            'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
            'SCHEDULER_PRIORITY_QUEUE': 'scrapy.pqueues.DownloaderAwarePriorityQueue',
            'CLOSESPIDER_ITEMCOUNT': 5

        }

        return settings_dict
