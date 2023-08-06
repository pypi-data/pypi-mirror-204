# pool-cue

Tools to make it easier to run and communicate with [arq](https://github.com/samuelcolvin/arq) job queues:

* Reusable config for the workers and queue
* Ability to stop a job from being added to the queue if it's already queued
* Tool to run tasks in sub-threads (with async function support)

For more details on arq, check out the [official documentation](https://arq-docs.helpmanual.io).

## Installation

Install the package:

```shell
pip install pool-cue
# or
poetry add pool-cue
```

## Usage

Configure the worker:

```python
# example/main.py
from pool_cue import QueueSettings, create_worker
from example import tasks  # python module with tasks (functions)

settings = QueueSettings(...)

Worker = create_worker(settings=settings, tasks=tasks)
```

```python
# example/__init__.py
from example.main import Worker
```

Start the worker:

```shell
arq example.Worker
```

And push jobs to the queue:

```python
from pool_cue import Queue
from example.main import settings

async with Queue(settings=settings) as queue:
    await queue.push_job(_func='test_task', extra_keyword_argument="foo")
```

Example worker output:

```
12:28:57: Starting worker for 2 functions: test_child_task, test_task
12:28:57: redis_version=7.0.10 mem_usage=1.46M clients_connected=2 db_keys=0
12:29:07:   0.19s → test_task:test_task(extra_keyword_argument='foo')
12:29:07:   0.00s ← test_task:test_task ●
```
