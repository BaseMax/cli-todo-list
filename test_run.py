import lTCT

# Prepare sample tasks
lTCT.tasks.clear()
lTCT.tasks.extend([
    {"title": "Task A", "done": False, "priority": 2},
    {"title": "task b", "done": True, "priority": 1},
    {"title": "Task C", "done": False, "priority": 1},
])

print('title_exists("Task A") ->', lTCT.title_exists('Task A'))
print('title_exists("task a") ->', lTCT.title_exists('task a'))
print('build_display_mapping() ->', lTCT.build_display_mapping())
print('\nprint_grouped_tasks():')
lTCT.print_grouped_tasks()
print('\nfind_matching_tasks("task") ->', lTCT.find_matching_tasks('task'))
print('\nsearch_tasks output:')
# call search_tasks but monkeypatch input by temporarily replacing builtins.input
import builtins
orig_input = builtins.input
builtins.input = lambda prompt='': 'task'
try:
    lTCT.search_tasks()
finally:
    builtins.input = orig_input
