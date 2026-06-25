import torch.nn
import torch.nn as ty
import re
import requests
URL = "server url"
HEADERS = {
    "xc-token": "your_api_token_here"
}
response = requests.get(URL, headers=HEADERS)
if response.status_code == 200:
    full_data = response.json()
    
    my_messages = full_data.get("list", [])
    
    print(f" Found {len(my_messages)} messages.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
def translate_to_numbers(text):
    text_lower = text.lower()
    
    f1 = 1 if re.search(r"https?|www|\.com|\.dz|link", text_lower) else 0
    
    scam_patterns = [
        r"fr[e3]{2}",
        r"n[1i]tro",
        r"fl[1i]xy",
        r"g[ir]atuit",
        r"cl[1i]ck",
    ]
    f2 = (
        1
        if any(re.search(pattern, text_lower) for pattern in scam_patterns)
        else 0
    )
    f3 = (
        sum(1 for c in text if c.isupper()) / len(text) if len(text) > 0 else 0
    )
    
    f4 = sum(1 for c in text if not c.isalnum() and not c.isspace())
    
    
    f5 = len(text) / 200  
    
    return torch.tensor([[f1, f2, f3, f4, f5]], dtype=torch.float32)
all_tensors = []
all_labels = []

for row in my_messages:
    text = row.get("message", "")
    label = row.get("label")
    
    features = translate_to_numbers(text)
    
    all_tensors.append(features)
    all_labels.append(label)

print(f"Prepared {len(all_tensors)} items for the PyTorch model!")
X = torch.cat(all_tensors, dim=0)

Y = torch.tensor([float(l) for l in all_labels]).view(-1, 1)

print("--- Final Check ---")
print(f"X_train Shape: {X.shape}")  
print(f"y_train Shape: {Y.shape}") 
class Brain(ty.Module):
    def __init__(self):
        super().__init__()
        self.agent = ty.Linear(5, 2)
        self.boss= ty.Linear(2 , 1)
    def forward(self, x):
        x = torch.sigmoid(self.agent(x))
        y = torch.sigmoid(self.boss(x))  
        return y

cola = Brain()  
creation =ty.BCELoss()
edit = torch.optim.SGD(kola.parameters(),lr=0.5)
for epoch in range(10000):
    edit.zero_grad() 
    output=kola(X)
    loss=creation(output , Y)
    loss.backward()
    edit.step()
    if epoch % 100 == 0:
        print(f"Epoch {epoch} Loss: {loss.item():.4f}")
torch.save(kola.state_dict(), 'brain.pth')
kola.eval()
