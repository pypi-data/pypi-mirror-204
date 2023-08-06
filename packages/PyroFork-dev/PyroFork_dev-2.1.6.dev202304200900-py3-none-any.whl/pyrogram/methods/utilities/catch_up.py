#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import pyrogram


class CatchUp:
    async def catch_up(
        self: "pyrogram.Client"
    ):
        """'Catches up' on the missed updates while the client was offline.

        You should call this method after registering the event handlers so that the updates it loads can by processed by your script.

        Parameters:

        Returns:
            :obj:`~pyrogram.Client`: The client itself.

        Example:
            .. code-block:: python

                from pyrogram import Client

                app = Client("my_account")


                async def main():
                    await app.start()
                    await app.catch_up()
                    ...
                    await app.stop()

                app.run(main())
        """
        local_pts = await self.storage.pts()
        local_date = await self.storage.date()
        while(True):
            diff = await self.invoke(
                    pyrogram.raw.functions.updates.GetDifference(
                        pts=local_pts,
                        date=local_date,
                        qts=-1
                    )
                )
            if isinstance(diff, pyrogram.raw.types.updates.DifferenceEmpty):
                break
            elif isinstance(diff, pyrogram.raw.types.updates.DifferenceTooLong):
                await self.storage.pts(diff.pts)
                continue
            users = {u.id: u for u in diff.users}
            chats = {c.id: c for c in diff.chats}
            for msg in diff.new_messages:
                self.dispatcher.updates_queue.put_nowait((
                    pyrogram.raw.types.UpdateNewMessage(
                        message=msg,
                        pts=diff.state.pts,
                        pts_count=-1
                    ),
                    users,
                    chats
                ))

            for update in diff.other_updates:
                self.dispatcher.updates_queue.put_nowait((update, users, chats))
            if isinstance(diff, pyrogram.raw.types.updates.Difference):
                break
        return self
