import sys
import psutil

if sys.platform != "win32":
    import resource

try:
    import tensorflow as tf
except Exception:  # noqa: BLE001
    tf = None


def configure_resources(
    ram_fraction: float = 0.75,
    gpu_fraction: float = 0.75,
) -> None:
    """Configure process to use all CPUs and limit RAM/GPU usage."""
    try:
        p = psutil.Process()
        p.cpu_affinity(list(range(psutil.cpu_count())))
    except Exception:
        pass

    try:
        total_mem = psutil.virtual_memory().total
        limit = int(total_mem * ram_fraction)
        if sys.platform != "win32":
            resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except Exception:
        pass

    if tf is not None:
        try:
            gpus = tf.config.list_physical_devices("GPU")
            if gpus:
                # Attempt to cap GPU memory
                details = tf.config.experimental.get_device_details(gpus[0])
                total_gpu_mem = details.get("memory_limit")
                if total_gpu_mem:
                    tf.config.experimental.set_virtual_device_configuration(
                        gpus[0],
                        [
                            tf.config.experimental.VirtualDeviceConfiguration(
                                memory_limit=int(total_gpu_mem * gpu_fraction)
                            )
                        ],
                    )
        except Exception:
            pass
