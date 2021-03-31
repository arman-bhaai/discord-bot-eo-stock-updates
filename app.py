# discord bot for updating stock information of eorange
# concept of sending discord message from background task >> https://stackoverflow.com/a/64370097
import discord
from discord import Embed
from discord.ext import commands
import logging
import asyncio
import threading

import requests
import json
import pandas as pd
from tabulate import tabulate
# from operator import itemgetter
import time
from datetime import datetime
import os
from dotenv import load_dotenv



class ConsoleApp:
    def __init__(self, dc_bot, evt_loop, channels_dict, kwargs):
        self.evt_loop = evt_loop
        self.channels_dict = channels_dict
        self.dc_bot = dc_bot
        self.kwargs = kwargs
        self.print_log('running ConsoleApp')
        self.print_log('requesting eorange data api')
        
        self.load_all_products_data()

        while True:
            # self.single_phone_stocks()
            # self.single_bike_stocks()
            self.all_phone_stocks(self.channels_dict['all_phone_stocks'])
            time.sleep(5)

    def load_all_products_data(self):
        # load smartphone database
        page_count_smartphones = 1
        self.db_dict_smartphones = {'products':[],'total_product_count':''}
        # fetch all smartphones pages
        while True:
            url_smartphones = f'https://eorange.shop/get-products/Smartphone?type=category&page={page_count_smartphones}&filter=%7B%22short_by%22:%22popularity%22,%22seller_by%22:[],%22brand_by%22:[],%22price%22:%7B%22min%22:0,%22max%22:0%7D%7D'
            self.print_log(f'fetching smartphone page {page_count_smartphones}...')
            api_dict = requests.get(url_smartphones).json()
            last_page = api_dict['data']['products']['last_page']
            product_list = api_dict['data']['products']['data']

            self.db_dict_smartphones['products'] += product_list

            if page_count_smartphones == last_page:
                self.db_dict_smartphones['total_product_count'] = api_dict['data']['products']['total']
                break
            page_count_smartphones += 1
        # sort product list
        self.db_dict_smartphones['products'] = sorted(self.db_dict_smartphones['products'], key=lambda k: k['name'])


        # # load bike database
        # page_count_bikes = 1
        # self.db_dict_bikes = {'products':[],'total_product_count':''}
        # # fetch all bikes pages
        # while True:
        #     url_bikes = f'https://eorange.shop/get-products/Motorcycle-Scooter?type=category&page={page_count_bikes}&filter=%7B%22short_by%22:%22popularity%22,%22seller_by%22:[],%22brand_by%22:[],%22price%22:%7B%22min%22:0,%22max%22:0%7D%7D'
        #     self.print_log(f'fetching bike page {page_count_bikes}...')
        #     api_dict = requests.get(url_bikes).json()
        #     last_page = api_dict['data']['products']['last_page']
        #     product_list = api_dict['data']['products']['data']

        #     self.db_dict_bikes['products'] += product_list

        #     if page_count_bikes == last_page:
        #         self.db_dict_bikes['total_product_count'] = api_dict['data']['products']['total']
        #         break
        #     page_count_bikes += 1
        # # sort product list
        # self.db_dict_bikes['products'] = sorted(self.db_dict_bikes['products'], key=lambda k: k['name'])


        
        
    def bot_send_embed(self, channel, fields, title='Title', desc='desc', colour=0xFF0000, timestamp=datetime.utcnow(), author_name='BDCG', footer='footer'):
        embed = Embed(title=title, description=desc,
        colour=colour, timestamp=timestamp)
        fields = fields
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_author(name=author_name)
        # embed.set_image(url="https://media.tenor.com/images/cb37de2f54039535426738c62136d0e3/tenor.gif")
        embed.set_footer(text=footer)
        asyncio.run_coroutine_threadsafe(channel.send(embed=embed), self.evt_loop)

    def all_phone_stocks(self, channel):
        in_stock = []
        for product in self.db_dict_smartphones['products']:
            if product['stock'] != 0:
                product['name'] = product['name'][:13]+'..'
                in_stock.append(product)
        retn = f"\n\n\nUpdated On --> {datetime.now().strftime('%d/%m/%y >> %-I:%M%:%S %p')}"
        return self.dic_to_table(in_stock, channel)

    def single_phone_stocks(self):
        self.print_log('checking single phone stocks...')
        # find out instant stock modification
        # load smartphone database
        page_count_smartphones = 1
        db_dict_smartphones_new = {'products':[],'total_product_count':''}
        # fetch all smartphones pages
        while True:
            url_smartphones = f'https://eorange.shop/get-products/Smartphone?type=category&page={page_count_smartphones}&filter=%7B%22short_by%22:%22popularity%22,%22seller_by%22:[],%22brand_by%22:[],%22price%22:%7B%22min%22:0,%22max%22:0%7D%7D'
            self.print_log(f'fetching smartphone page {page_count_smartphones}...')
            api_dict = requests.get(url_smartphones).json()
            last_page = api_dict['data']['products']['last_page']
            product_list = api_dict['data']['products']['data']

            db_dict_smartphones_new['products'] += product_list

            print(page_count_smartphones, last_page)
            input('press')
            if page_count_smartphones == last_page:
                db_dict_smartphones_new['total_product_count'] = api_dict['data']['products']['total']
                break
            page_count_smartphones += 1
        # sort product list
        db_dict_smartphones_new['products'] = sorted(db_dict_smartphones_new['products'], key=lambda k: k['name'])

        # products_stocked_in = [] # not in use
        # products_stocked_out = [] # not in use
        pairs = zip(self.db_dict_smartphones['products'], db_dict_smartphones_new['products'])

        for i,j in pairs:
            if i['name'] == j['name']:
                # product name matched
                self.print_log('product name matched')
                # fields = [("Stocks", j['stock'], True), ('Price', j['price'], True),]
                # self.bot_send_embed(self.channels_dict['single_phone_stocks'], fields, j['name'], author_name='Testtttt', colour=0xFF0000)
                if i['stock'] != j['stock']:
                    # stock data modified
                    self.print_log('stock data modified')
                    if j['stock'] == 0:
                        # product stocked out
                        self.print_log('product stocked out')
                        # products_stocked_out.append(j)
                        fields = [("Stocks", j['stock'], True), ('Price', j['price'], True),]
                        self.bot_send_embed(self.channels_dict['single_phone_stocks'], fields, j['name'], author_name='Stocked Out!', colour=0xFF0000)
                    elif j['stock'] != 0 and i['stock'] == 0:
                        # product stocked in
                        self.print_log('product stocked in')
                        # products_stocked_in.append(j)
                        fields = [("Stocks", j['stock'], True), ('Price', j['price'], True),]
                        self.bot_send_embed(self.channels_dict['single_phone_stocks'], fields, j['name'], author_name='Stocked In!', colour=0x00FF00)
                else:
                    self.print_log('stock data unmodified')
            else:
                # product name didn't match
                self.print_log('product name did not match')
        self.db_dict_smartphones = db_dict_smartphones_new.copy()

    def single_bike_stocks(self):
        self.print_log('checking single bike stocks...')
        # find out instant stock modification
        # load bike database
        page_count_bikes = 1
        db_dict_bikes_new = {'products':[],'total_product_count':''}
        # fetch all bikes pages
        while True:
            url_bikes = f'https://eorange.shop/get-products/Motorcycle-Scooter?type=category&page={page_count_bikes}&filter=%7B%22short_by%22:%22popularity%22,%22seller_by%22:[],%22brand_by%22:[],%22price%22:%7B%22min%22:0,%22max%22:0%7D%7D'
            self.print_log(f'fetching bike page {page_count_bikes}...')
            api_dict = requests.get(url_bikes).json()
            last_page = api_dict['data']['products']['last_page']
            product_list = api_dict['data']['products']['data']

            db_dict_bikes_new['products'] += product_list

            if page_count_bikes == last_page:
                db_dict_bikes_new['total_product_count'] = api_dict['data']['products']['total']
                break
            page_count_bikes += 1
        # sort product list
        db_dict_bikes_new['products'] = sorted(db_dict_bikes_new['products'], key=lambda k: k['name'])

        # products_stocked_in = [] # not in use
        # products_stocked_out = [] # not in use
        pairs = zip(self.db_dict_bikes['products'], db_dict_bikes_new['products'])

        for i,j in pairs:
            if i['name'] == j['name']:
                # product name matched
                self.print_log('product name matched')
                if i['stock'] != j['stock']:
                    # stock data modified
                    self.print_log('stock data modified')
                    if j['stock'] == 0:
                        # product stocked out
                        self.print_log('product stocked out')
                        # products_stocked_out.append(j)
                        fields = [("Stocks", j['stock'], True), ('Price', j['price'], True),]
                        self.bot_send_embed(self.channels_dict['single_bike_stocks'], fields, j['name'], author_name='Stocked Out!', colour=0xFF0000)
                    elif j['stock'] != 0 and i['stock'] == 0:
                        # product stocked in
                        self.print_log('product stocked in')
                        # products_stocked_in.append(j)
                        fields = [("Stocks", j['stock'], True), ('Price', j['price'], True),]
                        self.bot_send_embed(self.channels_dict['single_bike_stocks'], fields, j['name'], author_name='Stocked In!', colour=0x00FF00)
            else:
                # product name didn't match
                self.print_log('product name did not match')
        self.db_dict_bikes = db_dict_bikes.copy()


    def dic_to_table(self, dic, channel):
        df=pd.DataFrame(dic, columns=['name', 'stock', 'price'])
        df_idx_len = len(df.index)
        idx_row_start = 0
        idx_row_end = 0
        # if df_idx_len > 16:
        while df_idx_len > 16:
            idx_row_end += 16
            styled_table = '```'+tabulate(df.iloc[idx_row_start:idx_row_end], headers=['Products', 'Stocks', 'Prices'], tablefmt='fancy_grid')+'```'
            df_idx_len -= 16
            idx_row_start += 16
            self.bot_log(styled_table, channel)
        styled_table = '```'+tabulate(df.iloc[idx_row_end:], headers=['Products', 'Stocks', 'Prices'], tablefmt='fancy_grid')+'```'
        self.bot_log(styled_table, channel)

    def bot_log(self, msg, channel):
        # await channel.send('Test') # We can't do this because of the above comment
        asyncio.run_coroutine_threadsafe(self.dc_bot.send_log(msg, channel), self.evt_loop)

    def print_log(self, msg):
        print(msg)
        



class DiscordBot(commands.Bot):
    def __init__(self, bg_task):
        command_prefix = '..'
        super().__init__(command_prefix=command_prefix)

        self.bg_task = bg_task

        # necessary IDs
        self.CH_ID_all_phone_stocks = 825498395400601630
        self.CH_ID_single_phone_stocks = 825526202017775646
        self.CH_ID_single_bike_stocks = 825791268755079178
        self.GUILD_ID = 823819408894984262
    
    def run(self):
        DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

        self.print_log('running bot')
        super().run(DISCORD_TOKEN, reconnect=True)

    async def on_connect(self):
        self.print_log('bot connected')

    async def on_disconnect(self):
        self.print_log('bot disconnected')

    # @self.event
    async def on_ready(self):
        self.print_log('bot is ready')
        guild = self.get_guild(self.GUILD_ID)
        self.print_log(f'Guild Name: {guild}')

        self.channels_dict = dict(
            all_phone_stocks = self.get_channel(self.CH_ID_all_phone_stocks),
            single_phone_stocks = self.get_channel(self.CH_ID_single_phone_stocks),
            single_bike_stocks = self.get_channel(self.CH_ID_single_bike_stocks),
            )

        self.kwargs = dict(
            guild=guild
            )

        self.blocker_background_task()

    async def send_log(self, msg, channel):
        print(msg, datetime.now().isoformat(), '\n\n')
        msg_ext = msg + '\n\n'
        await channel.send(msg_ext)

    def print_log(self, msg):
        print(msg)

    def blocker_background_task(self):
        threading.Thread(
            target=self.bg_task,
            args=(self, asyncio.get_event_loop(), self.channels_dict, self.kwargs)
        ).start()
    
    async def on_message(self, message):
        pass

def main():
    load_dotenv()
    dbot = DiscordBot(bg_task=ConsoleApp)
    dbot.run()

if __name__ == "__main__":
    main()