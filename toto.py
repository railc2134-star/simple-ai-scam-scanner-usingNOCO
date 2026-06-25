import torch.nn
import torch.nn as ty
import re
import requests
URL = "http://localhost:8080/api/v1/db/data/v1/pftjft4txscifxd/m24mnqwwkissrsh?limit=1000"
HEADERS = {
    "xc-token": "your_api_token_here"
}
response = requests.get(URL, headers=HEADERS)
if response.status_code == 200:
    # Convert the raw web data into a Python dictionary
    full_data = response.json()
    
    # NocoDB stores the rows inside a key called 'list'
    my_messages = full_data.get("list", [])
    
    print(f" Found {len(my_messages)} messages.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
def translate_to_numbers(text):
    text_lower = text.lower()
    
    # 1. Smarter URL check (catches hxxp, spaced dots, etc.)
    f1 = 1 if re.search(r"https?|www|\.com|\.dz|link", text_lower) else 0
    
    # 2. Scam intent (using regex to catch things like n1tro or f r e e)
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
    
    
    f5 = len(text) / 200  # Normalized
    
    return torch.tensor([[f1, f2, f3, f4, f5]], dtype=torch.float32)
all_tensors = []
all_labels = []

for row in my_messages:
    # 1. Get the text and label from the row
    text = row.get("message", "")
    label = row.get("label")
    
    # 2. Convert text to numbers using your function
    features = translate_to_numbers(text)
    
    # 3. Store them
    all_tensors.append(features)
    all_labels.append(label)

print(f"Prepared {len(all_tensors)} items for the PyTorch model!")
X = torch.cat(all_tensors, dim=0)

# 2. Convert labels to float and reshape to [25, 1]
# We use .view(-1, 1) because PyTorch expects a column for labels
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