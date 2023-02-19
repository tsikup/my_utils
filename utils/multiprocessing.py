import multiprocessing


def determine_num_processes(image_files, num_processes):
    num_tasks = len(image_files)
    if num_processes > num_tasks:
        num_processes = num_tasks
    images_per_process = num_tasks / num_processes
    return num_processes, num_tasks, images_per_process


def create_gpu_array_task(image_files, process_idx, num_processes):
    _, _, images_per_process = determine_num_processes(image_files, num_processes)
    image_files_sublist = subset_tasks(image_files, process_idx, images_per_process)
    return image_files_sublist, process_idx


def subset_tasks(image_files, task_id, images_per_process):
    start_index = task_id * images_per_process + 1
    end_index = (task_id + 1) * images_per_process
    start_index = int(start_index)
    end_index = int(end_index)
    image_files_sublist = image_files[start_index - 1 : end_index]
    return image_files_sublist


def create_pool(image_files, num_processes, *args):
    num_processes = (
        multiprocessing.cpu_count() if num_processes is None else num_processes
    )

    num_processes, num_tasks, _ = determine_num_processes(image_files, num_processes)
    images_per_task = 1

    pool = multiprocessing.Pool(num_processes)

    tasks = []
    for num_task in range(0, num_tasks):
        input_sublist = subset_tasks(image_files, num_task, images_per_task)
        tasks.append((input_sublist, *args))
    print(
        "Number of processes: {}, number of tasks: {}".format(num_processes, len(tasks))
    )
    return pool, tasks, num_processes
