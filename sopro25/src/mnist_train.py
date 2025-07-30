import torch
import torchvision
import torch.nn as nn
from torchvision import transforms
from torch.utils.data import DataLoader

# Data loading function
def get_data_loaders():
    transform = transforms.ToTensor()
    trainset = torchvision.datasets.FashionMNIST('data/', train=True, download=True, transform=transform)
    testset = torchvision.datasets.FashionMNIST('data/', train=False, download=True, transform=transform)
    train_loader = DataLoader(dataset=trainset, batch_size=64, shuffle=True)
    test_loader = DataLoader(dataset=testset, batch_size=64, shuffle=False)
    return train_loader, test_loader

# Base model
class BaseNetwork(nn.Module):
    def __init__(self):
        super(BaseNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.layer1 = nn.Linear(784, 64)
        self.relu1 = nn.ReLU()
        self.layer2 = nn.Linear(64, 32)
        self.relu2 = nn.ReLU()
        self.layer3 = nn.Linear(32, 10)

    def forward(self, x):
        x = self.flatten(x)
        x = self.layer1(x)
        x = self.relu1(x)
        x = self.layer2(x)
        x = self.relu2(x)
        x = self.layer3(x)
        return x

# Batch norm model
class NormNetwork(nn.Module):
    def __init__(self):
        super(NormNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(784, 64)
        self.bn1 = nn.BatchNorm1d(64)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(64, 32)
        self.bn2 = nn.BatchNorm1d(32)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(32, 10)

    def forward(self, x):
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.bn2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x

# Training function
def train_and_evaluate(model, train_loader, test_loader, epochs=5, learning_rate=0.001):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    for epoch in range(epochs):
        model.train()
        for images, labels in train_loader:
            outputs = model(images)
            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        model.eval()
        correct = 0
        total = 0
        test_loss = 0
        with torch.no_grad():
            for images, labels in test_loader:
                outputs = model(images)
                test_loss += criterion(outputs, labels).item()
                _, predicted = torch.max(outputs, 1)
                correct += (predicted == labels).sum().item()
                total += labels.size(0)

        mean_test_loss = test_loss / len(test_loader)
        accuracy = 100 * correct / total
        print(f"Epoch {epoch+1}/{epochs} - Loss: {mean_test_loss:.4f}, Accuracy: {accuracy:.2f}%")

# Main script
if __name__ == "__main__":
    train_loader, test_loader = get_data_loaders()

    print("=== Training Base Model ===")
    baseline_model = BaseNetwork()
    train_and_evaluate(baseline_model, train_loader, test_loader)

    print("=== Training Batch Norm Model ===")
    norm_model = NormNetwork()
    train_and_evaluate(norm_model, train_loader, test_loader)

