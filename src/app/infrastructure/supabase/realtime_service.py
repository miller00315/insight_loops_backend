from typing import Callable, Dict, Any
from supabase import Client
import asyncio


class SupabaseRealtimeService:
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.subscriptions: Dict[str, Any] = {}

    async def subscribe_to_table(
        self,
        table: str,
        event: str = "*",
        callback: Callable[[Dict[str, Any]], None] = None,
    ):
        """Subscribe to real-time changes on a table"""
        try:
            channel = self.supabase.channel(f"{table}_changes")

            def handle_change(payload):
                if callback:
                    asyncio.create_task(self._async_callback(callback, payload))
                else:
                    print(f"Real-time event on {table}: {payload}")

            channel.on_postgres_changes(
                event=event, schema="public", table=table, callback=handle_change
            )

            channel.subscribe()
            self.subscriptions[f"{table}_{event}"] = channel

            return channel

        except Exception as e:
            print(f"Failed to subscribe to {table}: {str(e)}")
            return None

    async def _async_callback(self, callback: Callable, payload: Dict[str, Any]):
        """Wrapper to handle async callbacks"""
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(payload)
            else:
                callback(payload)
        except Exception as e:
            print(f"Callback error: {str(e)}")

    def unsubscribe(self, subscription_key: str):
        """Unsubscribe from real-time updates"""
        if subscription_key in self.subscriptions:
            try:
                self.subscriptions[subscription_key].unsubscribe()
                del self.subscriptions[subscription_key]
                return True
            except Exception as e:
                print(f"Failed to unsubscribe: {str(e)}")
                return False
        return False

    def unsubscribe_all(self):
        """Unsubscribe from all real-time updates"""
        for key in list(self.subscriptions.keys()):
            self.unsubscribe(key)
