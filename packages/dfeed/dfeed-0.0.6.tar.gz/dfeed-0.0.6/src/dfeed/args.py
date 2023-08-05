#!/usr/bin/env python3


class Args:
    _args_filter_output = ""
    _args_feed = ""
    _args_format = ""
    _args_invert = False
    _args_pick_feeds = False
    _args_pick_filters = False

    @classmethod
    def define_args(cls, args):
        if args.filter_output is not None:
            cls._args_filter_output = args.filter_output
        if args.feed is not None:
            cls._args_feed = args.feed
        if args.format is not None:
            cls._args_format = args.format
        cls._args_invert = args.invert
        cls._args_pick_feeds = args.pick_feeds
        cls._args_pick_filters = args.pick_filters

    @classmethod
    def filter_output(cls) -> str:
        return cls._args_filter_output

    @classmethod
    def add_feed(cls, feed: str):
        if cls._args_feed == "":
            cls._args_feed = feed
        else:
            cls._args_feed = f"{cls._args_feed},{feed}"

    @classmethod
    def feed(cls) -> str:
        return cls._args_feed

    @classmethod
    def format(cls) -> str:
        return cls._args_format

    @classmethod
    def invert(cls) -> bool:
        return cls._args_invert

    @classmethod
    def pick_feeds(cls) -> bool:
        return cls._args_pick_feeds

    @classmethod
    def pick_filters(cls) -> bool:
        return cls._args_pick_filters
