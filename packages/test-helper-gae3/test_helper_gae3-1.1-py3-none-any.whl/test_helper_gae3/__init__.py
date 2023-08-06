"""Test helper for GAE Python3 app.

https://cloud.google.com/appengine/docs/standard/python3/reference/services/bundled/google/appengine/ext/testbed/Testbed
"""
from google.appengine.ext import testbed


class TestGae3:
    """Mixing class for GAE testbed use."""

    gae_testbed = None
    blobstore_stub = None
    taskqueue_stub = None

    def set_up(self):
        """Activate GAE testbed for project in given dir."""
        self.gae_testbed = testbed.Testbed()
        self.gae_testbed.activate()
        # self.gae_testbed.setup_env()
        self.gae_testbed.init_datastore_v3_stub()
        self.gae_testbed.init_memcache_stub()

        self.gae_testbed.init_blobstore_stub()
        self.blobstore_stub = self.gae_testbed.get_stub(testbed.BLOBSTORE_SERVICE_NAME)

        self.gae_testbed.init_images_stub()
        self.gae_testbed.init_mail_stub()

        self.gae_testbed.init_taskqueue_stub()
        self.taskqueue_stub = self.gae_testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)

        self.gae_testbed.init_urlfetch_stub()
        self.gae_testbed.init_user_stub()

    def tear_down(self):
        """Deactivate GAE testbed."""
        self.gae_testbed.deactivate()
        self.gae_testbed = None

    def check_db_tables(self, db_state):
        """Check record count in the given GAE ndb Model.

        db_state must be defined as follows:

        db_state = [
          (ModelName, record_count),
        ]
        """
        for table, count in db_state:
            i = len(table.query().fetch(300, keys_only=True))
            assert i == count, "{} items: {} must be {}".format(
              table._get_kind(),  # pylint: disable=protected-access
              i,
              count
            )

    def reread(self, ndbkey):
        """Drop GAE memcash and read db record."""
        return ndbkey.get(use_cache=False, use_memcache=False)

    def assert_tasks_num(self, tasks_number, queue_name='default'):
        """Check task count for given GAE taskqueue."""
        tasks = self.gae_tasks(queue_name=queue_name, flush_queue=False)
        count = len(tasks)
        assert count == tasks_number, "task count: %d (must be %d) %s" % (
          count, tasks_number, [task['url'] for task in tasks]
        )

    def gae_tasks(self, queue_name='default', flush_queue=True):
        """Return all tasks for given GAE taskqueue."""
        tasks = self.taskqueue_stub.GetTasks(queue_name)
        if flush_queue:
            self.taskqueue_stub.FlushQueue(queue_name)

        return tasks

    def gae_queue_dump(self, queue_name='default', fields=None):
        """Print queue tasks."""
        tasks = self.gae_tasks(queue_name=queue_name, flush_queue=False)
        print()
        print("queue", queue_name, "tasks:", len(tasks))
        for task in tasks:
            if not fields:
                print(task)
            else:
                print(' '.join(["{}: {}".format(i, task[i]) for i in fields]))

    def gae_tasks_dict(self, queue_name='default'):
        """Return all tasks for given GAE taskqueue as dict."""
        return {task['name']: task for task in self.gae_tasks(queue_name=queue_name, flush_queue=False)}

    def gae_task_flask_execute(
      self, task, flask_app_test_client, is_delete=True, is_debug_print=False, status_code=200
    ):  # pylint: disable=too-many-arguments
        """Execute given task in fask app context."""
        method = task['method']
        assert method in ['PUT', 'PULL', 'POST']

        if is_debug_print:
            print("#task->", task['method'], task['url'], task['body'])

        # response = flask_app_test_client.get(task['url'])
        response = flask_app_test_client.post(task['url'], data=task['body'])

        if is_delete:
            self.taskqueue_stub.DeleteTask(task['queue_name'], task['name'])

        assert response.status_code == status_code

    def gae_queue_flask_execute(
      self, flask_test_client, queue_name='default', is_debug_print=False, status_code=200
    ):
        """Run all tasks for GAE taskqueue in fask app context."""
        for task in self.gae_tasks(queue_name=queue_name, flush_queue=True):
            self.gae_task_flask_execute(
              task,
              flask_test_client,
              is_delete=False,
              is_debug_print=is_debug_print,
              status_code=status_code
            )
