import torch
from transformers import AutoModelForCausalLM
from torch import nn

# Load full model
model_name = "gpt2"
full_model = AutoModelForCausalLM.from_pretrained(model_name)

# Define Part 1
class GPT2Part1(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.wte = model.transformer.wte  # Token embeddings
        self.wpe = model.transformer.wpe  # Positional embeddings
        self.blocks = model.transformer.h[:6]  # First 6 transformer blocks

    def forward(self, input_ids):
        input_embeds = self.wte(input_ids) + self.wpe(torch.arange(input_ids.size(1), device=input_ids.device))
        hidden_states = input_embeds
        for block in self.blocks:
            hidden_states = block(hidden_states)[0]
        
        print(f"Hidden states before final layer: {hidden_states.shape}")

        return hidden_states

# Save Part 1
model_part1 = GPT2Part1(full_model)
torch.save(model_part1.state_dict(), "model_part1.pth")

# Define Part 2
class GPT2Part2(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.blocks = model.transformer.h[6:]  # Remaining transformer blocks
        self.ln_f = model.transformer.ln_f  # Final layer normalization
        self.lm_head = model.lm_head  # Output layer

    def forward(self, hidden_states):
        for block in self.blocks:
            hidden_states = block(hidden_states)[0]
        hidden_states = self.ln_f(hidden_states)
        logits = self.lm_head(hidden_states)
        print(f"Hidden states before final layer: {hidden_states.shape}")
        print(f"Logits shape: {logits.shape}")
        return logits

# Save Part 2
model_part2 = GPT2Part2(full_model)
torch.save(model_part2.state_dict(), "model_part2.pth")

