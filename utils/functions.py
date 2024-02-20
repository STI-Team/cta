import torch


def collate(samples: list) -> dict:
    """
    TODO
    :param samples:
    :return:
    """
    data = torch.nn.utils.rnn.pad_sequence(
        [sample["data"] for sample in samples]
    )
    labels = torch.cat([sample["labels"] for sample in samples])

    batch = {"data": data.T, "labels": labels}
    return batch


def prepare_device(n_gpu_use):
    """
    TODO
    """
    num_gpu = torch.cuda.device_count()
    if n_gpu_use > 0 and num_gpu == 0:
        print("Warning: No GPU available on this machine, training will be performed on CPU.")
        n_gpu_use = 0
    if n_gpu_use > num_gpu:
        print(f"Warning: The number of GPU configured to use is {n_gpu_use}, but only {num_gpu} are available")
        n_gpu_use = num_gpu
    device = torch.device('cuda:0' if n_gpu_use > 0 else 'cpu')
    list_ids = list(range(n_gpu_use))
    return device, list_ids


def get_token_logits(device, data: torch.Tensor, logits: torch.Tensor, token_id: int) -> torch.Tensor:
    token_indexes = torch.nonzero(data == token_id)
    token_logits = torch.zeros(
        token_indexes.shape[0],
        logits.shape[2]
    ).to(device)

    for i in range(token_indexes.shape[0]):
        j, k = token_indexes[i]
        logit_i = logits[j, k, :]
        token_logits[i] = logit_i
    return token_logits
