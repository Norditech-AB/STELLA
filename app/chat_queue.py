
import queue
import threading

from app.db import db
from app.models.chat import Chat
from app.task_manager import TaskManager, Task


class Worker(threading.Thread):
    def __init__(self, chat_queue, manager, task_manager, socketio):
        threading.Thread.__init__(self)
        self.chat_queue = chat_queue
        self.manager = manager
        self.task_manager = task_manager
        self.socketio = socketio
        self.daemon = True

    def run(self):
        """
        Keep in mind that this function only gets triggered when a user sends a message.
        It is never triggered by the system.
        :return:
        """
        while True:
            chat_id = self.chat_queue.get()

            # Check if chat has been picked up by another worker
            if chat_id in self.manager.active_chats:
                self.chat_queue.task_done()
                continue

            print(f"[ChatQueue] -- Worker {self.name} picked up chat {chat_id}")
            self.manager.active_chats.append(chat_id)

            chat = db.get_chat_by_id(chat_id)

            if chat.busy:
                self.socketio.emit(
                    'chat_information',
                    #json.dumps({"type": "busy", "message": "This chat is processing your previous request, please wait."}),
                    room=chat_id,
                    namespace='/chat'
                )

            chat.busy = True
            db.update_chat(chat)

            task = Task.create_top_level_task(chat)
            self.task_manager.add_task(task.task_id)

            self.chat_queue.task_done()
            print(f"[ChatQueue] ---- Worker {self.name} finished chat {chat_id}")
            self.manager.active_chats.remove(chat_id)


class ChatQueue:
    def __init__(self, num_workers, socketio):
        self.chat_queue = queue.Queue()
        self.task_manager = TaskManager(num_workers=5, socketio=socketio)
        self.workers = [Worker(self.chat_queue, self, task_manager=self.task_manager, socketio=socketio) for _ in range(num_workers)]
        self.active_chats = []
        for worker in self.workers:
            print(f"[ChatQueue] Starting worker {worker}")
            worker.start()

    def add_chat(self, chat_id):
        # Check if chat is already in queue
        if chat_id in self.active_chats:
            print(f"[ChatQueue] Chat already in queue: {chat_id}")
            return
        print(f"[ChatQueue] Chat added to queue: {chat_id}")
        self.chat_queue.put(chat_id)
