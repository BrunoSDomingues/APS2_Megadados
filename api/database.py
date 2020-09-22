from api.models import Task
import uuid

class DBSession:
    tasks = {}

    def __init__(self):
        self.tasks = DBSession.tasks

    def getAllTasks(self):
        return self.tasks

    def filterTasksByStatus(self, completed: bool):
        return {
            uuid_: item
            for uuid_, item in self.tasks.items()
            if item.completed == completed
        }

    def createNewTask(self, uuid_: uuid.UUID, item: Task):
        self.tasks[uuid_] = item
        return uuid_

    def getTask(self, uuid_: uuid.UUID):
        return self.tasks[uuid_]

    def replaceTask(self, uuid_: uuid.UUID, item: Task):
        self.tasks[uuid_] = item

    def updateTask(self, uuid_: uuid.UUID, item: Task):
        update_data = item.dict(exclude_unset=True)
        self.tasks[uuid_] = self.tasks[uuid_].copy(update=update_data)

    def removeTask(self, uuid_: uuid.UUID):
        del self.tasks[uuid_]


def get_db():
    return DBSession()