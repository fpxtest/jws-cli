#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
作者：jammny
文件描述： 
"""
from rich.console import Console
from rich.table import Table


def show_table(data):
    """
    表格展示数据
    :param: data
    :return:
    """
    table = Table(title="cdn results", show_lines=False)
    table.add_column("domain", justify="left", style="cyan", no_wrap=True)
    table.add_column("ip", justify="left", style="magenta")
    table.add_column("cdn", justify="left", style="red")
    table.add_column("address", justify="left", style="red")
    for i in data:
        table.add_row(i['domain'], str(i['ip']), i['cdn'], str(i['address']))
    console = Console()
    console.print(table)
