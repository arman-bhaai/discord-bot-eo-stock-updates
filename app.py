# discord bot for updating stock information of eorange
import discord
from discord import Embed
from discord.ext import commands, tasks
from discord.ext.commands import command, Cog
import logging
import asyncio
import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

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
    pass
#     def __init__(self, bot_cog, evt_loop, dict_channels, kwargs):
#         self.evt_loop = evt_loop
#         self.dict_channels = dict_channels
#         self.bot_cog = bot_cog
#         self.kwargs = kwargs
        # self.print_log('running ConsoleApp')
        # self.db_dict_smartphones_old = {}
        # self.db_dict_bikes_old = {}
        # self.print_log('requesting eorange data api')
        
        # self.load_all_products_data()

        # while True:
        #     self.loop_all_products()
        # self.bot_cog.dict_futures[3] = self.bot_cog.tp_exec.submit(self.loop_single_products)
        
        # while True:
        #     if self.bot_cog.evt_exit_th2.is_set():
        #         self.bot_cog.evt_exit_th2.clear()
        #         self.print_log('th2 killed')
            
            # self.loop_all_products()

            
    # def loop_all_products(self):
        # # show mass products stocks
        # self.mass_products_stocks(
        #     self.bot_cog.db_dict_smartphones,
        #     self.dict_channels['all_phones_stocks'],
        #     'smartphones'
        # )
        # self.mass_products_stocks(
        #     self.bot_cog.db_dict_bikes,
        #     self.dict_channels['all_bikes_stocks'],
        #     'bikes'
        # )
        # # show mass products stockouts
        # self.mass_products_stock_outs(
        #     self.bot_cog.db_dict_smartphones,
        #     self.dict_channels['all_phones_stock_outs'],
        #     'smartphones'
        # )
        # self.mass_products_stock_outs(
        #     self.bot_cog.db_dict_bikes,
        #     self.dict_channels['all_bikes_stock_outs'],
        #     'bikes'
        # )
        # self.print_log('sleep 5')
        # time.sleep(5)
    
    # def loop_single_products(self):
    #     while True:
    #         # if self.bot_cog.evt_exit_th3.is_set():
    #         #     self.bot_cog.evt_exit_th3.clear()
    #         #     self.print_log('th3 killed')
            
    #         # display single smartphone stocks
    #         db_dict_products_new = self.single_product_stocks(
    #             'smartphone',
    #             self.bot_cog.db_dict_smartphones,
    #             self.db_dict_smartphones_old,
    #             self.dict_channels['single_phone_stocks']
    #         )
    #         self.print_log('substituting old smartphone db with recent db')
    #         self.db_dict_smartphones_old = db_dict_products_new
    #         print('sleep 5 sec sing product stock')

    #         # display single bike stocks
    #         db_dict_products_new = self.single_product_stocks(
    #             'bike',
    #             self.bot_cog.db_dict_bikes,
    #             self.db_dict_bikes_old,
    #             self.dict_channels['single_bike_stocks']
    #         )
    #         self.print_log('substituting old bike db with recent db')
    #         self.db_dict_smartphones_old = db_dict_products_new
    #         print('sleep 20 sec sing product stock')
    #         time.sleep(20)
        
    # def bot_send_embed(self, channel, fields, title='Title', desc='desc', colour=0xFF0000, timestamp=datetime.utcnow(), author_name='BDCG', footer='footer'):
    #     embed = Embed(title=title, description=desc,
    #     colour=colour, timestamp=timestamp)
    #     fields = fields
    #     for name, value, inline in fields:
    #         embed.add_field(name=name, value=value, inline=inline)
    #     embed.set_author(name=author_name)
    #     # embed.set_image(url="https://media.tenor.com/images/cb37de2f54039535426738c62136d0e3/tenor.gif")
    #     embed.set_footer(text=footer)
    #     asyncio.run_coroutine_threadsafe(channel.send(embed=embed), self.evt_loop)

    # def mass_products_stocks(self, db_dict_products, channel, product_name):
    #     self.print_log(f'showing mass {product_name} stocks')
    #     in_stock = []
    #     for product in db_dict_products['products']:
    #         if product['stock'] > 0:
    #             product['name'] = product['name'][:13]+'..'
    #             in_stock.append(product)
    #     return self.dict_to_table(in_stock, channel)

    # def mass_products_stock_outs(self, db_dict_products, channel, product_name):
    #     self.print_log(f'showing mass {product_name} stocks')
    #     out_of_stock = []
    #     for product in db_dict_products['products']:
    #         if product['stock'] <= 0:
    #             product['name'] = product['name'][:13]+'..'
    #             out_of_stock.append(product)
        # return self.dict_to_table(out_of_stock, channel)       
    
    # def single_product_stocks(self, product_name, db_dict_products_new, db_dict_products_old, channel):
    #     self.print_log(f'checking single {product_name} stocks...')
    #     # find out instant stock modification
    #     # load product database
    #     db_dict_products_new = db_dict_products_new
    #     db_dict_products_old = db_dict_products_old

    #     if not db_dict_products_old:
    #         db_dict_products_old = db_dict_products_new

    #     pairs = zip(db_dict_products_old['products'], db_dict_products_new['products'])
    #     # pairs = zip(db_dict_products_old['data'], db_dict_products_new['data'])

    #     for i,j in pairs:
    #         if i['name'] == j['name']:
    #             # product name matched
    #             self.print_log('product name matched')
    #             # fields = [("Stocks", j['stock'], True), ('Price', j['price'], True),]
    #             # self.bot_send_embed(self.dict_channels['single_phone_stocks'], fields, j['name'], author_name='Testtttt', colour=0xFF0000)
    #             if i['stock'] != j['stock']:
    #                 # stock data modified
    #                 self.print_log('stock data modified')
    #                 if j['stock'] == 0:
    #                     # product stocked out
    #                     self.print_log('product stocked out')
    #                     # products_stocked_out.append(j)
    #                     fields = [("Stocks", j['stock'], True), ('Price', j['price'], True),]
    #                     self.bot_send_embed(channel, fields, j['name'], author_name='Stocked Out!', colour=0xFF0000)
    #                 elif j['stock'] != 0 and i['stock'] == 0:
    #                     # product stocked in
    #                     self.print_log('product stocked in')
    #                     # products_stocked_in.append(j)
    #                     fields = [("Stocks", j['stock'], True), ('Price', j['price'], True),]
    #                     self.bot_send_embed(channel, fields, j['name'], author_name='Stocked In!', colour=0x00FF00)
    #             else:
    #                 self.print_log('stock data unmodified')
    #         else:
    #             # product name didn't match
    #             self.print_log('product name did not match')
    #             input('product name did not match')
    #     return db_dict_products_new

    # def single_product_stocks(self, product_name, db_dict_products_new, db_dict_products_old, channel):
    #     self.print_log(f'checking single {product_name} stocks...')
    #     # find out instant stock modification
    #     # load product database
    #     db_dict_products_new = db_dict_products_new
    #     db_dict_products_old = db_dict_products_old

    #     if not db_dict_products_old:
    #         db_dict_products_old = db_dict_products_new

    #     pairs = zip(db_dict_products_old['products'], db_dict_products_new['products'])
    #     # pairs = zip(db_dict_products_old['data'], db_dict_products_new['data'])

    #     for i,j in pairs:
    #         if i['name'] == j['name']:
    #             # product name matched
    #             self.print_log('product name matched')
    #             # fields = [("Stocks", j['stock'], True), ('Price', j['price'], True),]
    #             # self.bot_send_embed(self.dict_channels['single_phone_stocks'], fields, j['name'], author_name='Testtttt', colour=0xFF0000)
    #             if i['stock'] != j['stock']:
    #                 # stock data modified
    #                 self.print_log('stock data modified')
    #                 if j['stock'] == 0:
    #                     # product stocked out
    #                     self.print_log('product stocked out')
    #                     # products_stocked_out.append(j)
    #                     fields = [("Stocks", j['stock'], True), ('Price', j['price'], True),]
    #                     self.bot_send_embed(channel, fields, j['name'], author_name='Stocked Out!', colour=0xFF0000)
    #                 elif j['stock'] != 0 and i['stock'] == 0:
    #                     # product stocked in
    #                     self.print_log('product stocked in')
    #                     # products_stocked_in.append(j)
    #                     fields = [("Stocks", j['stock'], True), ('Price', j['price'], True),]
    #                     self.bot_send_embed(channel, fields, j['name'], author_name='Stocked In!', colour=0x00FF00)
    #             else:
    #                 self.print_log('stock data unmodified')
    #         else:
    #             # product name didn't match
    #             self.print_log('product name did not match')
    #             input('product name did not match')
    #     return db_dict_products_new

    # def dict_to_table(self, dic, channel):
    #     timestamp = f"```\n\n\nUpdated On --> {datetime.now().strftime('%d/%m/%y >> %-I:%M:%S %p')}```"
    #     df=pd.DataFrame(dic, columns=['name', 'stock', 'price'])
    #     df.index += 1
    #     df_idx_len = len(df.index)
    #     if df_idx_len <= 15:
    #         styled_table = '```'+tabulate(df, headers=['Products', 'Stocks', 'Prices'], tablefmt='fancy_grid')+'```'
    #         self.bot_log(timestamp, channel)
    #         self.bot_log(styled_table, channel)
    #         self.bot_log('```List Ended```', channel)
    #     else:
    #         idx_row_start = 0
    #         idx_row_end = 0
    #         # if df_idx_len > 16:
    #         is_first_loop = True
    #         while df_idx_len > 15:
    #             idx_row_end += 15
    #             if is_first_loop:
    #                 styled_table = '```'+tabulate(df.iloc[idx_row_start:idx_row_end], headers=['Products', 'Stocks', 'Prices'], tablefmt='fancy_grid')+'```'
    #                 idx_row_start += 15
    #                 df_idx_len -= 15
    #                 is_first_loop = False
    #                 self.bot_log(timestamp, channel)
    #                 self.bot_log(styled_table, channel)
    #             else:
    #                 time.sleep(3)
    #                 styled_table = '```'+tabulate(df.iloc[idx_row_start:idx_row_end], tablefmt='fancy_grid')+'```'
    #                 idx_row_start += 15
    #                 df_idx_len -= 15
    #                 self.bot_log(styled_table, channel)
    #         styled_table = '```'+tabulate(df.iloc[idx_row_end:], tablefmt='fancy_grid')+'```'
    #         self.bot_log(styled_table, channel)
    #         self.bot_log('```List Ended```', channel)

    # def bot_log(self, msg, channel):
    #     asyncio.run_coroutine_threadsafe(self.bot_cog.send_log(msg, channel), self.evt_loop)

    # def print_log(self, msg):
    #     print(msg)


class MyCog(Cog):
    def __init__(self, bot, bg_task):
        self.bot = bot
        self.bg_task =  bg_task
        self.req = {}
        # thread kill events
        self.evt_exit_th1 = threading.Event()
        self.evt_exit_th2 = threading.Event()
        self.evt_exit_th3 = threading.Event()
        self.evt_exit_th4 = threading.Event()
        self.evt_exit_th5 = threading.Event()

        self.db_dict_smartphones = {'products': [],'total_product_count':''}
        self.db_dict_smartphones_list = []
        self.db_dict_bikes =  {'products':{},'total_product_count':''}
        self.tp_exec = ThreadPoolExecutor()
        self.dict_futures = {}
        
        self.db_dict_smartphones_old = {}
        self.db_dict_bikes_old = {}
        
        self.count = 0
        self.local_db_dict = {}

    @command(name='cmd11')
    async def cmd_load_all_products_data(self, ctx):
        self.print_log('triggered --> cmd_load_all_products_data()')
        
        self.print_log('executing th1')
        self.dict_futures[1.1] = self.tp_exec.submit(self.load_smartphones_db)
        self.dict_futures[1.2] = self.tp_exec.submit(self.load_bikes_db)
        # self.dict_futures[1.3] = self.tp_exec.submit(self.load_test_db) ### test db
        await ctx.send('command granted')

    @command(name='cmd10')
    async def cmd_kill_load_all_products_data(self, ctx):
        self.print_log('triggered --> cmd_kill_load_all_products_data')
        self.evt_exit_th1.set()
        await ctx.send('command granted')

    @command(name='cmd21')
    async def cmd_run_console_app(self, ctx):
        self.print_log('triggered --> cmd_run_console_app()')
        self.dict_futures[2] = self.tp_exec.submit(self.bg_task, self, asyncio.get_event_loop(), self.bot.dict_channels, self.bot.kwargs)
        await ctx.send('command granted')

    @command(name='cmd20')
    async def cmd_kill_console_app(self, ctx):
        self.print_log('triggered --> cmd_kill_console_app')
        self.evt_exit_th2.set()
        await ctx.send('command granted')

    @command(name='cte')
    async def cmd_check_thread_errors(self, ctx):
        for idx, f in enumerate(concurrent.futures.as_completed(self.dict_futures.values())):
            # print(f'thread {idx} result fetched')
            print(idx, f.result())
        # concurrent.futures.wait(self.dict_futures)
        # for fut in self.dict_futures.values():
        #     print(fut.result())

    @command(name='cmd31')
    async def cmd_run_loop_mass_products(self, ctx):
        self.print_log('trigged --> cmd_run_loop_mass_products()')
        self.dict_futures[4] = self.tp_exec.submit(self.loop_mass_products, asyncio.get_event_loop())
        # self.mass_products_stocks(
        #         self.db_dict_smartphones,
        #         self.bot.dict_channels['all_phones_stocks'],
        #         'smartphones'
        #     )

    @command(name='cmd41')
    async def cmd_run_loop_single_products(self, ctx):
        self.print_log('trigged --> cmd_run_loop_single_products()')
        self.dict_futures[3] = self.tp_exec.submit(self.loop_single_products, asyncio.get_event_loop())

    def loop_single_products(self, evt_loop):
        print('started load_single_products(self)')
        while True:
            if self.evt_exit_th3.is_set():
                self.evt_exit_th3.clear()
                self.print_log('th3 killed')
            time.sleep(5)

            # display single smartphone stocks
            db_new = self.single_product_stocks(
                'smartphone', 
                self.db_dict_smartphones, 
                self.db_dict_smartphones_old, 
                self.bot.dict_channels['single_phone_stocks'], 
                evt_loop
            )
            self.print_log('substituting old smartphone db with recent db')
            self.db_dict_smartphones_old = db_new
            

            # display single bike stocks
            db_new = self.single_product_stocks(
                'bike',
                self.db_dict_bikes,
                self.db_dict_bikes_old,
                self.bot.dict_channels['single_bike_stocks'],
                evt_loop
            )
            self.print_log('substituting old bike db with recent db')
            self.db_dict_bikes_old = db_new

            self.print_log('sleeping 5 sec')
            time.sleep(5)
    
    def single_product_stocks(self, product_name, db_list_products_new, db_list_products_old, channel, evt_loop):
        self.print_log(f'checking single {product_name} stocks...')
        # find out instant stock modification
        # load product database
        db_list_products_new = db_list_products_new
        db_list_products_old = db_list_products_old

        if not db_list_products_old:
            db_list_products_old = db_list_products_new


        for i in db_list_products_new:
            for j in db_list_products_old:
                if i['name'] == j['name']:
                    self.print_log('single product name matched')
                    if i['stock'] != j['stock']:
                        print('stock data modified')
                        if i['stock'] > 0:
                            # product stocked in
                            self.print_log('product stocked in')
                            # products_stocked_in.append(j)
                            fields = [("Stocks", i['stock'], True), ('Price', i['price'], True),]
                            self.bot_send_embed(channel, fields, evt_loop, i['name'], author_name='Stocked In!', colour=0x00FF00)
                        else:
                            # product stocked out
                            self.print_log('product stocked out')
                            # products_stocked_out.append(j)
                            fields = [("Stocks", i['stock'], True), ('Price', i['price'], True),]
                            self.bot_send_embed(channel, fields, evt_loop, i['name'], author_name='Stocked Out!', colour=0xFF0000)

        return db_list_products_new
        
    def bot_send_embed(self, channel, fields, evt_loop, title='Title', desc='', colour=0xFF0000, timestamp=datetime.utcnow(), author_name='BDCG', footer=''):
        embed = Embed(title=title, description=desc,
        colour=colour, timestamp=timestamp)
        fields = fields
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_author(name=author_name)
        # embed.set_image(url="https://media.tenor.com/images/cb37de2f54039535426738c62136d0e3/tenor.gif")
        embed.set_footer(text=footer)
        asyncio.run_coroutine_threadsafe(channel.send(embed=embed), evt_loop)

    def loop_mass_products(self, evt_loop):
        while True:
            if self.evt_exit_th2.is_set():
                # self.evt_exit_th2.clear()
                self.print_log('th2 killed')
            # show mass products stocks
            self.mass_products_stocks(
                self.db_dict_smartphones,
                self.bot.dict_channels['all_phones_stocks'],
                'smartphones',
                evt_loop
            )
            self.mass_products_stocks(
                self.db_dict_bikes,
                self.bot.dict_channels['all_bikes_stocks'],
                'bikes',
                evt_loop
            )
            # show mass products stockouts
            self.mass_products_stock_outs(
                self.db_dict_smartphones,
                self.bot.dict_channels['all_phones_stock_outs'],
                'smartphones',
                evt_loop
            )
            self.mass_products_stock_outs(
                self.db_dict_bikes,
                self.bot.dict_channels['all_bikes_stock_outs'],
                'bikes',
                evt_loop
            )
            self.print_log('sleep 5')
            time.sleep(5)

    def mass_products_stocks(self, db_dict_products, channel, product_name, evt_loop):
        self.print_log(f'showing mass {product_name} stocks')
        in_stock = []
        for product in db_dict_products['products']:
            if product['stock'] > 0:
                product['name'] = product['name'][:13]+'..'
                in_stock.append(product)
        return self.dict_to_table2(in_stock, channel, evt_loop)

    def mass_products_stock_outs(self, db_dict_products, channel, product_name, evt_loop):
        self.print_log(f'showing mass {product_name} stocks')
        out_of_stock = []
        for product in db_dict_products['products']:
            if product['stock'] <= 0:
                product['name'] = product['name'][:13]+'..'
                out_of_stock.append(product)
        return self.dict_to_table2(out_of_stock, channel, evt_loop)


    def load_smartphones_db(self):
        while True:
            if self.evt_exit_th1.is_set():
                # self.evt_exit_th1.clear()
                self.print_log('th1.1 killed')
                break
            # load smartphones db
            self.db_dict_smartphones = self.load_product_db(
                'https://eorange.shop/get-products/Smartphone?type=category&page=',
                '&filter=%7B%22short_by%22:%22popularity%22,%22seller_by%22:[],%22brand_by%22:[],%22price%22:%7B%22min%22:0,%22max%22:0%7D%7D',
                'smartphone'
            )
            print('sleeping 5 sec th 1.1')
            time.sleep(5)
    
    def load_bikes_db(self):
        while True:
            if self.evt_exit_th1.is_set():
                # self.evt_exit_th1.clear()
                self.print_log('th1.1 killed')
                break
            # load bikes db
            self.db_dict_bikes = self.load_product_db(
                'https://eorange.shop/get-products/Motorcycle-Scooter?type=category&page=',
                '&filter=%7B%22short_by%22:%22popularity%22,%22seller_by%22:[],%22brand_by%22:[],%22price%22:%7B%22min%22:0,%22max%22:0%7D%7D',
                'bike'
            )
            print('sleeping 5 sec th 1.2')
            time.sleep(5)

    def load_test_db(self):
        print('load_db() started')
        x=0
        while True:
        #     if self.evt_exit_th1.is_set():
        #         # self.evt_exit_th1.clear()
        #         self.print_log('th1.3 killed')
        #         break
        #     # load test db
        #     # self.load_product_db(
        #     #     'https://eorange.shop/get-products/Motorcycle-Scooter?type=category&page=',
        #     #     '&filter=%7B%22short_by%22:%22popularity%22,%22seller_by%22:[],%22brand_by%22:[],%22price%22:%7B%22min%22:0,%22max%22:0%7D%7D',
        #     #     self.db_dict_bikes,
        #     #     'bike'
        #     # )
            

            # load product database function
            page_count = 1
            
            # self.local_db_dict = {'products':[],'total_product_count':''}
            local_db_list = []
            x+=1
            # local_db_dict['products'] = api_dict['data']['products']['data']
            # fetch all product pages
            while True:
                print('reading db file...')
                with open('deldb.json','r') as f:
                    api_dict=json.load(f)
                # self.db_dict_smartphones_list = self.local_db_dict['data']['products']['data']
                # self.db_dict_smartphones = self.db_dict_smartphones_list
        #         self.print_log(f'fetching test db page {page_count}...')
        #         # url_smartphones = 'https://api.jsonbin.io/b/606b29148be464182c591cb7/latest'
        #         # api_dict = requests.get(url_smartphones).json()
        #         # print(api_dict)
                last_page = api_dict['data']['products']['last_page']
                product_list = api_dict['data']['products']['data']

                local_db_list += product_list
                

                if page_count == last_page:
        #             local_db_dict['total_product_count'] = api_dict['data']['products']['total']
                    break
                page_count += 1
            # sort product list
            local_db_list = sorted(local_db_list, key=lambda k: k['name'])
            # saved processed data to main db
            self.db_dict_smartphones =  local_db_list
            # self.db_dict_smartphones['total_product_count'] = local_db_dict['total_product_count']

            print('sleeping 5(30) sec th 1.3')
            time.sleep(5)

        

    def load_product_db(self, api_url_first, api_url_last, product_name):
        # load product database
        page_count = 1
        
        local_db_list = []
        # fetch all product pages
        while True:
            self.print_log(f'fetching {product_name} page {page_count}...')
            url_smartphones = api_url_first+str(page_count)+api_url_last
            api_dict = requests.get(url_smartphones).json()
            last_page = api_dict['data']['products']['last_page']
            product_list = api_dict['data']['products']['data']

            local_db_list += product_list
            

            if page_count == last_page:
                # local_db_dict['total_product_count'] = api_dict['data']['products']['total']
                break
            page_count += 1
        # sort product list
        local_db_list = sorted(local_db_list, key=lambda k: k['name'])
        # saved processed data to main db
        return local_db_list
        # db_dict['total_product_count'] = local_db_dict['total_product_count']

    
    @command()
    async def oy(self, ctx):
        await ctx.send('hello')

    @command(name='arman00')
    async def cmd_test(self, ctx):
        t = threading.Thread(
            target=self.test,
            args=(asyncio.get_event_loop(),)
        )
        t.start()

    def test(self, evt_loop):
        print(self.db_dict_smartphones['products'][0]['name'])
    
    def test_func_sync(self, evt_loop):
        while True:
            if self.evt_exit_thread.is_set():
                self.evt_exit_thread.clear()
                break
            asyncio.run_coroutine_threadsafe(self.send_log('run loop', self.bot.dict_channels['robot_commands']), evt_loop)
            self.req = requests.get('https://api.jsonbin.io/b/606b29148be464182c591cb7/latest').json()
            asyncio.run_coroutine_threadsafe(self.send_log(self.req, self.bot.dict_channels['robot_commands']), evt_loop)
            # await self.bot.dict_channels['robot_commands'].send(self.req)
            # await asyncio.sleep(5)
            asyncio.run_coroutine_threadsafe(self.send_log('end loop', self.bot.dict_channels['robot_commands']), evt_loop)
            time.sleep(10)
    

    @Cog.listener()
    async def on_ready(self):
        print("MyCog is ready")
        # await self.cmd_load_all_products_data(None)
        # input('start func')
        # self.test_run('iphone')
        # input('end func')
    

        
    def send_log_async(self, msg, channel):
        asyncio.run_coroutine_threadsafe(self.send_log(msg, channel), asyncio.get_event_loop())
        # self.send_log(msg, channel)

    def send_log_async2(self, msg, channel, evt_loop): # for threads
        asyncio.run_coroutine_threadsafe(self.send_log(msg, channel), evt_loop)

    async def send_log(self, msg, channel):
        print(msg, datetime.now().isoformat(), '\n\n')
        await channel.send(msg)

    def print_log(self, msg):
        print(msg)

    def bot_log(self, msg, channel):
        # await channel.send('Test') # We can't do this because of the above comment
        self.send_log(msg, channel)
        # asyncio.run_coroutine_threadsafe(self.send_log(msg, channel), self.evt_loop)

    def dict_to_table(self, dic, channel):
        timestamp = f"```\n\n\nUpdated On --> {datetime.now().strftime('%d/%m/%y >> %-I:%M:%S %p')}```"
        df=pd.DataFrame(dic, columns=['name', 'stock', 'price'])
        df.index += 1
        df_idx_len = len(df.index)
        if df_idx_len <= 15:
            styled_table = '```'+tabulate(df, headers=['Products', 'Stocks', 'Prices'], tablefmt='fancy_grid')+'```'
            self.send_log_async2(timestamp, channel)
            self.send_log_async(styled_table, channel)
        else:
            idx_row_start = 0
            idx_row_end = 0
            # if df_idx_len > 16:
            is_first_loop = True
            while df_idx_len > 15:
                idx_row_end += 15
                if is_first_loop:
                    styled_table = '```'+tabulate(df.iloc[idx_row_start:idx_row_end], headers=['Products', 'Stocks', 'Prices'], tablefmt='fancy_grid')+'```'
                    idx_row_start += 15
                    df_idx_len -= 15
                    is_first_loop = False
                    self.send_log_async(timestamp, channel)
                    self.send_log_async(styled_table, channel)
                else:
                    time.sleep(5)
                    styled_table = '```'+tabulate(df.iloc[idx_row_start:idx_row_end], tablefmt='fancy_grid')+'```'
                    idx_row_start += 15
                    df_idx_len -= 15
                    self.send_log_async(styled_table, channel)
            styled_table = '```'+tabulate(df.iloc[idx_row_end:], tablefmt='fancy_grid')+'```'
            self.send_log_async(styled_table, channel)

    def dict_to_table2(self, dic, channel, evt_loop): #for threads
        timestamp = f"```\n\n\nUpdated On --> {datetime.now().strftime('%d/%m/%y >> %-I:%M:%S %p')}```"
        df=pd.DataFrame(dic, columns=['name', 'stock', 'price'])
        df.index += 1
        df_idx_len = len(df.index)
        if df_idx_len <= 15:
            styled_table = '```'+tabulate(df, headers=['Products', 'Stocks', 'Prices'], tablefmt='fancy_grid')+'```'
            self.send_log_async2(timestamp, channel, evt_loop)
            self.send_log_async2(styled_table, channel, evt_loop)
        else:
            idx_row_start = 0
            idx_row_end = 0
            # if df_idx_len > 16:
            is_first_loop = True
            while df_idx_len > 15:
                idx_row_end += 15
                if is_first_loop:
                    styled_table = '```'+tabulate(df.iloc[idx_row_start:idx_row_end], headers=['Products', 'Stocks', 'Prices'], tablefmt='fancy_grid')+'```'
                    idx_row_start += 15
                    df_idx_len -= 15
                    is_first_loop = False
                    self.send_log_async2(timestamp, channel, evt_loop)
                    self.send_log_async2(styled_table, channel, evt_loop)
                else:
                    time.sleep(5)
                    styled_table = '```'+tabulate(df.iloc[idx_row_start:idx_row_end], tablefmt='fancy_grid')+'```'
                    idx_row_start += 15
                    df_idx_len -= 15
                    self.send_log_async2(styled_table, channel, evt_loop)
            styled_table = '```'+tabulate(df.iloc[idx_row_end:], tablefmt='fancy_grid')+'```'
            self.send_log_async2(styled_table, channel, evt_loop)

    ########################################## Commands ##############################################
    ##################################################################################################
    ######################################### Smartphones ############################################

    @command(name='nokia')
    async def cmd_nokia_stock(self, ctx, product_name='nokia'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='onokia')
    async def cmd_nokia_stock_out(self, ctx, product_name='nokia'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='samsung')
    async def cmd_samsung_stock(self, ctx, product_name='samsung'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='osamsung')
    async def cmd_samsung_stock_out(self, ctx, product_name='samsung'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='realme')
    async def cmd_realme_stock(self, ctx, product_name='realme'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='orealme')
    async def cmd_realme_stock_out(self, ctx, product_name='realme'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='xiaomi')
    async def cmd_xiaomi_stock(self, ctx, product_name='xiaomi'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='oxiaomi')
    async def cmd_xiaomi_stock_out(self, ctx, product_name='xiaomi'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='iphone')
    async def cmd_iphone_stock(self, ctx, product_name='iphone'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='oiphone')
    async def cmd_iphone_stock_out(self, ctx, product_name='iphone'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='vivo')
    async def cmd_vivo_stock(self, ctx, product_name='vivo'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='ovivo')
    async def cmd_vivo_stock_out(self, ctx, product_name='vivo'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='oppo')
    async def cmd_oppo_stock(self, ctx, product_name='oppo'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='ooppo')
    async def cmd_oppo_stock_out(self, ctx, product_name='oppo'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='poco')
    async def cmd_poco_stock(self, ctx, product_name='poco'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='opoco')
    async def cmd_poco_stock_out(self, ctx, product_name='poco'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='symphony')
    async def cmd_symphony_stock(self, ctx, product_name='symphony'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='osymphony')
    async def cmd_symphony_stock_out(self, ctx, product_name='symphony'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='huawei')
    async def cmd_huawei_stock(self, ctx, product_name='huawei'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='ohuawei')
    async def cmd_huawei_stock_out(self, ctx, product_name='huawei'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='maximus')
    async def cmd_maximus_stock(self, ctx, product_name='maximus'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='omaximus')
    async def cmd_maximus_stock_out(self, ctx, product_name='maximus'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='walton')
    async def cmd_walton_stock(self, ctx, product_name='walton'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='owalton')
    async def cmd_walton_stock_out(self, ctx, product_name='walton'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='redmi')
    async def cmd_redmi_stock(self, ctx, product_name='redmi'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='oredmi')
    async def cmd_redmi_stock_out(self, ctx, product_name='redmi'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='oneplus')
    async def cmd_oneplus_stock(self, ctx, product_name='oneplus'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='ooneplus')
    async def cmd_oneplus_stock_out(self, ctx, product_name='oneplus'):
        db_product_list = self.db_dict_smartphones['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    #####################################################################################################
    ########################################### bikes ###################################################
    @command(name='bajaj')
    async def cmd_bajaj_stock(self, ctx, product_name='bajaj'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='obajaj')
    async def cmd_bajaj_stock_out(self, ctx, product_name='bajaj'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='yamaha')
    async def cmd_yamaha_stock(self, ctx, product_name='yamaha'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='oyamaha')
    async def cmd_yamaha_stock_out(self, ctx, product_name='yamaha'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='honda')
    async def cmd_honda_stock(self, ctx, product_name='honda'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='ohonda')
    async def cmd_honda_stock_out(self, ctx, product_name='honda'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='tvs')
    async def cmd_tvs_stock(self, ctx, product_name='tvs'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='otvs')
    async def cmd_tvs_stock_out(self, ctx, product_name='tvs'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='hero')
    async def cmd_hero_stock(self, ctx, product_name='hero'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='ohero')
    async def cmd_hero_stock_out(self, ctx, product_name='hero'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='lifan')
    async def cmd_lifan_stock(self, ctx, product_name='lifan'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='olifan')
    async def cmd_lifan_stock_out(self, ctx, product_name='lifan'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    @command(name='runner')
    async def cmd_runner_stock(self, ctx, product_name='runner'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] > 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])
    
    @command(name='orunner')
    async def cmd_runner_stock_out(self, ctx, product_name='runner'):
        db_product_list = self.db_dict_bikes['products']
        products = []
        
        for i in db_product_list:
            if product_name in i['name'].lower() and i['stock'] <= 0:
                i['name'] = i['name'][:13]+'..'
                products.append(i)
        self.dict_to_table(products, self.bot.dict_channels['robot_commands'])

    #####################################################################################################
    #####################################################################################################




class DiscordBot(commands.Bot):
    def __init__(self):
        command_prefix = '..'
        super().__init__(command_prefix=command_prefix)

        self.dict_channels = {}

        # necessary IDs
        self.CH_ID_robot_commands = 826883934750507069
        self.CH_ID_single_phone_stocks = 825526202017775646
        self.CH_ID_single_bike_stocks = 825791268755079178
        self.CH_ID_all_phones_stocks = 825498395400601630
        self.CH_ID_all_bikes_stocks = 826880912225468467
        self.CH_ID_all_phones_stock_outs = 826883287267672135
        self.CH_ID_all_bikes_stock_outs = 826883488036683806
        self.GUILD_ID = 823819408894984262

        # ### test server necessary IDs
        # self.CH_ID_robot_commands = 828202226581372978
        # self.CH_ID_single_phone_stocks = 828201918878187542
        # self.CH_ID_single_bike_stocks = 828201951564267521
        # self.CH_ID_all_phones_stocks = 828202027019665428
        # self.CH_ID_all_bikes_stocks = 828202061924925480
        # self.CH_ID_all_phones_stock_outs = 828202121298968576
        # self.CH_ID_all_bikes_stock_outs = 828202156053758011
        # self.GUILD_ID = 828200839369719819
     
    def run(self):
        DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
        # DISCORD_TOKEN = os.environ['TEST_DISCORD_TOKEN'] ### for test server

        self.print_log('running bot')
        super().run(DISCORD_TOKEN, reconnect=True)

    async def on_connect(self):
        self.print_log('bot connected')

    async def on_disconnect(self):
        self.print_log('bot disconnected')

    # @self.event
    async def on_ready(self):
        self.dict_channels = dict(
            robot_commands = self.get_channel(self.CH_ID_robot_commands),
            single_phone_stocks = self.get_channel(self.CH_ID_single_phone_stocks),
            single_bike_stocks = self.get_channel(self.CH_ID_single_bike_stocks),
            all_phones_stocks = self.get_channel(self.CH_ID_all_phones_stocks),
            all_bikes_stocks = self.get_channel(self.CH_ID_all_bikes_stocks),
            all_phones_stock_outs = self.get_channel(self.CH_ID_all_phones_stock_outs),
            all_bikes_stock_outs = self.get_channel(self.CH_ID_all_bikes_stock_outs),
            )

        self.kwargs = dict(
            guild=self.get_guild(self.GUILD_ID)
            )

        self.print_log('bot is ready')
        self.print_log(f'Guild Name: {self.kwargs["guild"]}')
    
    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

    def print_log(self, msg):
        print(msg)

def main():
    load_dotenv()
    dbot = DiscordBot()
    dbot.add_cog(MyCog(dbot, bg_task=ConsoleApp))
    dbot.run()
    

if __name__ == "__main__":
    main()


### useful links
# concept of sending discord message from background task >> https://stackoverflow.com/a/64370097
# concept of using await object out of async funtion >> https://stackoverflow.com/a/53726266
# concept of killing threads gracefully >> https://blog.miguelgrinberg.com/post/how-to-kill-a-python-thread
# concept of sorting dictionary >> https://towardsdatascience.com/sorting-a-dictionary-in-python-4280451e1637
# concept of using threadpool executor >> https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3