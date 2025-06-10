from api.utils import executor


def kill_executor():
    """
    Shutdown the executor gracefully.
    """
    print("Shutting down executor...")
    executor.shutdown(wait=False, cancel_futures=True)


def shutdown():
    """
    Shutdown the application gracefully.
    """
    kill_executor()
    print("Executor shutdown complete. Application is shutting down.")
    # Additional cleanup can be added here if needed
