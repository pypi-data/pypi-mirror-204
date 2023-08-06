'''Assetto Corsa Grid Class'''

from datetime import datetime
import glob
import logging
import os
import shutil
from typing import Any, List

from ac_websocket_server.debug import DebugTransaction
from ac_websocket_server.entries import EntryList
from ac_websocket_server.error import WebsocketsServerError
from ac_websocket_server.observer import Notifier
from ac_websocket_server.protocol import Protocol

ENTRY_LIST_INI = 'entry_list.ini'
ENTRY_LIST_NEW = 'entry_list_new.ini'
ENTRY_LIST_OLD = 'entry_list_old.ini'


class Grid(Notifier):
    '''Represents grid setup'''

    def __init__(self, server_directory: str, track: str = None, entry_list: EntryList = None):

        self._logger = logging.getLogger('ac-ws.grid')

        self.server_directory = server_directory

        self._debug_transaction = DebugTransaction(self.server_directory)

        self.entry_list = entry_list
        self.track = track

        super().__init__()

    async def consumer(self, message_words: List[str], connection: id = None):
        '''Consume args destined for the server'''

        message_funcs = {'finish': self.__update_finishing,
                         'reverse': self.__update_reversed,
                         'entries': self.__entries,
                         'order': self.__order,
                         'save': self.__save}

        if message_funcs.get(message_words[0]):
            await message_funcs[message_words[0]](connection=connection)

    async def __entries(self, connection: Any = None):
        '''Show original grid order info as a JSON string'''
        await self.put(Protocol.success({'entries': self.entry_list.show_entries()}), observer=connection)

    def __debug_transaction(self, name: str):
        '''Save all grid files in debug transaction'''

        self._debug_transaction.open(name)
        self._debug_transaction.save_file(
            f'{self.server_directory}/cfg/{ENTRY_LIST_INI}')
        self._debug_transaction.save_file(
            f'{self.server_directory}/cfg/{ENTRY_LIST_NEW}')
        self._debug_transaction.save_file(
            f'{self.server_directory}/cfg/{ENTRY_LIST_OLD}')
        self._debug_transaction.close()

    async def __order(self, connection: Any = None):
        '''Show current grid order info as a JSON string'''
        await self.put(Protocol.success({'grid': self.entry_list.show_grid()}), observer=connection)

    def restore(self, connection: Any = None):
        '''Restore updated entry_list.ini file'''

        self.__debug_transaction('grid-restore-pre')

        try:
            if os.path.exists(f'{self.server_directory}/cfg/{ENTRY_LIST_NEW}'):
                os.replace(f'{self.server_directory}/cfg/{ENTRY_LIST_INI}',
                           f'{self.server_directory}/cfg/{ENTRY_LIST_OLD}')
                os.replace(f'{self.server_directory}/cfg/{ENTRY_LIST_NEW}',
                           f'{self.server_directory}/cfg/{ENTRY_LIST_INI}')
        except OSError as error:
            self._logger.error(f'Restore failed: {error}')

        self.__debug_transaction('grid-restore-post')

    async def __save(self, connection: Any = None):
        '''Write updated entry_list.ini file'''

        self.__debug_transaction('grid-save-pre')

        try:
            self.entry_list.write(
                f'{self.server_directory}/cfg/{ENTRY_LIST_NEW}')
            await self.put(Protocol.success(msg='entry_list_new.ini file update SUCCESS'), observer=connection)
        except WebsocketsServerError as error:
            await self.put(Protocol.error(
                msg=f'entry_list.ini file update FAILURE: {error}'), observer=connection)

        self.__debug_transaction('grid-save-post')

    async def update(self, reverse: bool = False, connection: Any = None):
        '''Update grid based on latest results.JSON file and using sorting rule'''

        if reverse:
            self._debug_transaction.open('grid-reverse')
            self.entry_list.set_reversed_order()
        else:
            self._debug_transaction.open('grid-finish')
            self.entry_list.set_standard_order()

        try:
            result_files = glob.glob(
                os.path.join(f'{self.server_directory}/results', "*RACE.json"))
            if len(result_files) > 0:
                result_file = max(result_files, key=os.path.getctime)
                self.entry_list.parse_result_file(
                    result_file, track=self.track)
                self._debug_transaction.save_file(
                    f'{self.server_directory}/cfg/entry_list.ini')
                self._debug_transaction.save_file(result_file)
            else:
                await self.put(Protocol.error(
                    msg='Unable to parse results file - no file exists'), observer=connection)
                return
        except WebsocketsServerError as error:
            await self.put(Protocol.error(
                msg=f'{result_file} parse FAILURE: {error}'), observer=connection)
            return

        await self.put(Protocol.success(
            msg=f'{result_file} parse SUCCESS'), observer=connection)

        await self.__order(connection=connection)

        self._debug_transaction.close()

    async def __update_finishing(self, connection: Any = None):
        '''Update grid in standard finishing order'''
        await self.update(connection=connection)

    async def __update_reversed(self, connection: Any = None):
        '''Update grid in reverse finishing order'''
        await self.update(reverse=True, connection=connection)
