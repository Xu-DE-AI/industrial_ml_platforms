import torch
import torch.distributed as dist
from torch import nn
from torch.utils.data import DataLoader, TensorDataset, DistributedSampler

def main():
    dist.init_process_group("gloo")
    rank = dist.get_rank()

    x = torch.randn(20000, 5)
    y = (x[:, 0] + .3*x[:, 1] - .2*x[:, 4] > 0).long()

    ds = TensorDataset(x, y)
    sampler = DistributedSampler(ds)
    loader = DataLoader(ds, batch_size=256, sampler=sampler)

    model = nn.Sequential(nn.Linear(5, 32), nn.ReLU(), nn.Linear(32, 2))
    model = nn.parallel.DistributedDataParallel(model)

    opt = torch.optim.AdamW(model.parameters(), lr=1e-3)

    for epoch in range(3):
        sampler.set_epoch(epoch)
        for xb, yb in loader:
            opt.zero_grad()
            loss = nn.functional.cross_entropy(model(xb), yb)
            loss.backward()
            opt.step()
        if rank == 0:
            print("epoch", epoch, "loss", float(loss))

    dist.destroy_process_group()

if __name__ == "__main__":
    main()
