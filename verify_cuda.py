import torch
print("PyTorch CUDA Available:", torch.cuda.is_available())  # Should be True
print("PyTorch CUDA Version:", torch.version.cuda)  # Should match your installed CUDA
print("PyTorch Built with CUDA:", torch.backends.cudnn.version())  # Should not be None
print("GPU Name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU Found")
